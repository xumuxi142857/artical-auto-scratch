# -*- coding: utf-8 -*-
"""Convert the translated Markdown into a readable DOCX (Chinese academic report style)."""
import re, sys, os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def set_cn_font(run, name="宋体", size=None, bold=None, color=None):
    run.font.name = "Times New Roman"
    r = run._element.rPr.rFonts
    r.set(qn("w:eastAsia"), name)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = color


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`|\$[^$]+?\$)")


def add_inline(p, text, size=10.5, cit=None):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            run = p.add_run(part[2:-2]); set_cn_font(run, size=size, bold=True)
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            run = p.add_run(part[1:-1]); set_cn_font(run, name="Consolas", size=size - 0.5)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            run = p.add_run(part[1:-1]); set_cn_font(run, size=size); run.italic = True
        else:
            run = p.add_run(part); set_cn_font(run, size=size)


def build(md_path, docx_path, title_fallback="论文中文翻译"):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.4)
        s.top_margin = s.bottom_margin = Cm(2.2)

    i = 0
    n = len(lines)
    in_math = False
    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        # display-math block: render LaTeX source centered, verbatim
        if line.strip() in ("$$", "\\["):
            in_math = not in_math
            i += 1
            continue
        if in_math:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(line.strip())
            set_cn_font(run, name="Times New Roman", size=10)
            run.italic = True
            i += 1
            continue
        # tables
        if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                raw = lines[i].strip().strip("|")
                if not re.match(r"^[\s:\-|]+$", raw):
                    rows.append([c.strip() for c in raw.split("|")])
                i += 1
            if rows:
                cols = max(len(r) for r in rows)
                t = doc.add_table(rows=0, cols=cols)
                t.style = "Table Grid"
                for ri, row in enumerate(rows):
                    cells = t.add_row().cells
                    for ci in range(cols):
                        txt = row[ci] if ci < len(row) else ""
                        p = cells[ci].paragraphs[0]
                        add_inline(p, txt, size=9)
                        if ri == 0:
                            for run in p.runs:
                                run.bold = True
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(text)
                set_cn_font(run, name="黑体", size=18, bold=True)
                p.paragraph_format.space_after = Pt(6)
            else:
                h = doc.add_heading(level=min(level, 3))
                run = h.add_run(text)
                set_cn_font(run, name="黑体", size={2: 14, 3: 12, 4: 11}.get(level, 11), bold=True)
                run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
            i += 1
            continue
        if line.startswith(">"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.space_after = Pt(4)
            add_inline(p, line.lstrip("> ").strip(), size=9.5)
            for run in p.runs:
                run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            i += 1
            continue
        mb = re.match(r"^(\s*)([-*+])\s+(.*)$", line)
        if mb:
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, mb.group(3).strip())
            i += 1
            continue
        mn = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", line)
        if mn:
            p = doc.add_paragraph(style="List Number")
            add_inline(p, mn.group(3).strip())
            i += 1
            continue
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.25
        add_inline(p, line.strip())
        i += 1

    doc.save(docx_path)
    print("saved:", docx_path)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
