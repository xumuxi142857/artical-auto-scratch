#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把工作区里的论文文件夹导入正在运行的 Zotero（7/10 均可）。

原理：Zotero 启动时会在 127.0.0.1:23119 开一个 connector 服务（浏览器插件用的那个）。
  POST /connector/saveItems      -> 建条目（带元数据）
  POST /connector/saveAttachment -> 把本地 PDF 字节直接传给 Zotero，成为该条目的附件
两步用同一个 sessionID，条目的 "id" 字段作为 parentItemID 关联。

用法：
  python zotero_import.py                 # 导入所有还没导过的论文文件夹
  python zotero_import.py --date 2026-11-04
  python zotero_import.py --dry-run       # 只打印将要导入什么
  python zotero_import.py --force         # 忽略已导入记录，再导一遍
  python zotero_import.py --list          # 列出所有论文文件夹与导入状态
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT, "_zotero")
STATE_FILE = os.path.join(STATE_DIR, "imported.json")
DEFAULT_ENDPOINT = "http://127.0.0.1:23119"

ITEM_TYPES = {
    "inproceedings": "conferencePaper",
    "conference": "conferencePaper",
    "article": "journalArticle",
    "book": "book",
    "misc": "preprint",
    "techreport": "report",
}


# ---------------------------------------------------------------- helpers
def post_json(endpoint, path, payload, timeout=120):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint + path,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Zotero-Connector-API-Version": "3",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def post_bytes(endpoint, path, blob, metadata, content_type="application/pdf", timeout=300):
    req = urllib.request.Request(
        endpoint + path,
        data=blob,
        method="POST",
        headers={
            "Content-Type": content_type,
            "Content-Length": str(len(blob)),
            "X-Metadata": json.dumps(metadata),
            "X-Zotero-Connector-API-Version": "3",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def zotero_alive(endpoint):
    try:
        with urllib.request.urlopen(endpoint + "/connector/ping", timeout=5) as resp:
            return b"Zotero is running" in resp.read()
    except Exception:
        return False


def read_text(path):
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as fh:
                return fh.read()
        except UnicodeDecodeError:
            continue
    return ""


def parse_bibtex(text):
    """抓 README 里第一个 @xxx{...} 条目，返回 {字段小写: 值}。支持嵌套花括号。"""
    m = re.search(r"@(\w+)\s*\{", text)
    if not m:
        return None
    entry_type = m.group(1).lower()
    i = m.end()
    fields = {}
    depth = 1
    name = None
    while i < len(text) and depth > 0:
        ch = text[i]
        if ch == "{":
            depth += 1
            i += 1
            continue
        if ch == "}":
            depth -= 1
            i += 1
            continue
        # try to read a field name at this position
        fm = re.match(r"\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*\{", text[i:])
        if fm:
            fname = fm.group(1).lower()
            j = i + fm.end()
            val = []
            d = 1
            while j < len(text) and d > 0:
                c = text[j]
                if c == "{":
                    d += 1
                elif c == "}":
                    d -= 1
                    if d == 0:
                        break
                val.append(c)
                j += 1
            fields[fname] = "".join(val).strip()
            i = j + 1
            continue
        i += 1
    if not fields:
        return None
    fields["_type"] = entry_type
    return fields


def strip_braces(value):
    """BibTeX 里 {LLMs} 这种保护性花括号要去掉，否则标题会带字面量括号。"""
    if not value:
        return value
    prev = None
    while prev != value:
        prev = value
        value = re.sub(r"\{([^{}]*)\}", r"\1", value)
    return value.strip()


def split_creators(author):
    if not author:
        return []
    out = []
    for chunk in re.split(r"\s+and\s+", strip_braces(author)):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "," in chunk:
            last, first = chunk.split(",", 1)
            out.append({"lastName": last.strip(), "firstName": first.strip(), "creatorType": "author"})
        else:
            parts = chunk.split()
            if len(parts) == 1:
                out.append({"lastName": parts[0], "creatorType": "author"})
            else:
                out.append({"lastName": parts[-1], "firstName": " ".join(parts[:-1]), "creatorType": "author"})
    return out


def clean_pages(pages):
    if not pages:
        return ""
    return re.sub(r"\s*-{1,3}\s*", "-", pages.strip())


def section_text(md, heading_prefix):
    """取 '## xxx' 到下一个 '## ' 之间的正文。"""
    lines = md.splitlines()
    out, on = [], False
    for line in lines:
        if line.startswith("## "):
            if on:
                break
            if line[3:].strip().startswith(heading_prefix):
                on = True
                continue
        if on:
            out.append(line)
    return "\n".join(out).strip()


def pick_pdf(folder):
    pdfs = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    if not pdfs:
        return None
    for tag in ("正式版",):
        for f in pdfs:
            if tag in f:
                return os.path.join(folder, f)
    for f in pdfs:
        if "arxiv" in f.lower():
            return os.path.join(folder, f)
    return os.path.join(folder, pdfs[0])


def venue_label(folder_name, fields):
    m = re.match(r"\d+_([A-Za-z]+)(\d{4})_", folder_name or "")
    if m:
        return "%s %s" % (m.group(1).upper(), m.group(2))
    year = fields.get("year", "")
    return year


def build_tags(md, venue, fields, hay=""):
    tags = []
    if venue:
        tags.append(venue)
    if "CCF-A" in md:
        tags.append("CCF-A")
    elif "CCF-B" in md:
        tags.append("CCF-B")
    hay = (fields.get("title", "") + " " + hay).lower()
    if "theory of mind" in hay or "theory-of-mind" in hay or re.search(r"\btom\b", hay):
        tags.append("ToM")
    if "grpo" in hay:
        tags.append("GRPO")
    if "心智" in hay:
        tags.append("心智推理")
    tags.append("DSH-auto")
    seen, out = set(), []
    for t in tags:
        if t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return out


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.loads(read_text(STATE_FILE) or "{}")
        except Exception:
            return {}
    return {}


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)


def find_papers(date=None):
    out = []
    for name in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, name)
        if not os.path.isdir(d) or not re.match(r"^\d{4}-\d{2}-\d{2}$", name):
            continue
        if date and name != date:
            continue
        for sub in sorted(os.listdir(d)):
            p = os.path.join(d, sub)
            if os.path.isdir(p) and re.match(r"^\d+_", sub):
                out.append((name, sub, p))
    return out


def build_item(folder_name, folder):
    readme = os.path.join(folder, "README.md")
    md = read_text(readme) if os.path.exists(readme) else ""
    fields = parse_bibtex(md) or {}
    venue = venue_label(folder_name, fields)
    item_type = ITEM_TYPES.get(fields.get("_type", "inproceedings"), "conferencePaper")
    title = strip_braces(fields.get("title") or folder_name)
    one = section_text(md, "一句话概括")
    res = section_text(md, "主要结果")
    item = {
        "id": folder_name,
        "itemType": item_type,
        "title": title,
        "creators": split_creators(fields.get("author", "")),
        "date": fields.get("year", ""),
        "url": fields.get("url", ""),
        "DOI": fields.get("doi", ""),
        "pages": clean_pages(fields.get("pages", "")),
        "volume": fields.get("volume", ""),
        "publisher": fields.get("publisher", ""),
        "tags": [{"tag": t} for t in build_tags(md, venue, fields, one + " " + res)],
        "attachments": [],
    }
    book = strip_braces(fields.get("booktitle") or fields.get("journal") or "")
    if item_type == "conferencePaper":
        item["proceedingsTitle"] = book
        item["conferenceName"] = venue
    elif item_type == "journalArticle":
        item["publicationTitle"] = book
    elif item_type == "preprint":
        item["repository"] = "arXiv"
        item["archiveID"] = "arXiv:" + folder_name
    if not item["url"]:
        for line in md.splitlines():
            m = re.search(r"https?://\S+", line)
            if m:
                item["url"] = m.group(0).rstrip(")")
                break
    # 摘要字段优先取 BibTeX 的 abstract
    if fields.get("abstract"):
        item["abstractNote"] = re.sub(r"\s+", " ", fields["abstract"]).strip()

    one = section_text(md, "一句话概括")
    res = section_text(md, "主要结果")
    note_bits = []
    if one:
        note_bits.append(("一句话概括", one))
    if res:
        note_bits.append(("主要结果", res))
    if note_bits:
        html = ['<div class="zotero-note znv1">']
        html.append("<p><strong>本地文件夹：</strong>%s</p>" % folder.replace("&", "&amp;"))
        for head, body in note_bits:
            html.append("<h2>%s</h2>" % head)
            for para in body.split("\n"):
                para = para.strip()
                if not para:
                    continue
                if para.startswith(("- ", "* ")):
                    para = "• " + para[2:]
                html.append("<p>%s</p>" % para.replace("&", "&amp;").replace("<", "&lt;"))
        html.append("</div>")
        item["notes"] = [{"note": "\n".join(html)}]
    return item, title, venue


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="只导入某个日期文件夹，如 2026-11-04")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    args = ap.parse_args()

    state = load_state()
    papers = find_papers(args.date)
    if args.list:
        for date, folder_name, path in papers:
            mark = "已导入" if state.get(folder_name) else "未导入"
            print("%s  %-6s  %s" % (date, mark, folder_name))
        return 0

    pending = [(d, n, p) for d, n, p in papers if args.force or not state.get(n)]
    if args.limit:
        pending = pending[: args.limit]
    if not pending:
        print("没有需要导入的论文（全部已导入）。用 --force 可重导。")
        return 0

    if not zotero_alive(args.endpoint):
        print("连不上 Zotero（%s/connector/ping）。请先打开 Zotero 再跑。" % args.endpoint)
        return 2

    ok = fail = 0
    for date, folder_name, folder in pending:
        item, title, venue = build_item(folder_name, folder)
        pdf = pick_pdf(folder)
        if args.dry_run:
            print("[dry] %s | %s | pdf=%s | tags=%s" % (
                folder_name, title[:60], os.path.basename(pdf) if pdf else "无",
                ",".join(t["tag"] for t in item["tags"])))
            continue
        sid = str(uuid.uuid4())
        payload = {"sessionID": sid, "uri": item.get("url") or "file:///" + folder.replace("\\", "/"),
                   "items": [item]}
        try:
            status, _ = post_json(args.endpoint, "/connector/saveItems", payload)
            if status != 201:
                raise RuntimeError("saveItems HTTP %s" % status)
            if pdf:
                blob = open(pdf, "rb").read()
                meta = {"sessionID": sid, "parentItemID": folder_name,
                        "title": "Full Text PDF", "url": item.get("url") or ""}
                st2, _ = post_bytes(args.endpoint, "/connector/saveAttachment", blob, meta)
                if st2 != 201:
                    raise RuntimeError("saveAttachment HTTP %s" % st2)
            state[folder_name] = {
                "title": title,
                "venue": venue,
                "pdf": os.path.basename(pdf) if pdf else None,
                "imported_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "date": date,
            }
            save_state(state)
            ok += 1
            print("OK   %s  %s" % (folder_name, title[:70]))
        except urllib.error.HTTPError as e:
            fail += 1
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:200]
            except Exception:
                pass
            print("FAIL %s  HTTP %s %s" % (folder_name, e.code, body))
        except Exception as e:
            fail += 1
            print("FAIL %s  %s" % (folder_name, e))
        time.sleep(1.2)

    print("---- 完成：成功 %d，失败 %d ----" % (ok, fail))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
