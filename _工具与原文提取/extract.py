import sys, os, re
from pypdf import PdfReader

def extract(path, out):
    r = PdfReader(path)
    pages = []
    for i, p in enumerate(r.pages):
        t = p.extract_text() or ""
        pages.append(f"\n\n===== PAGE {i+1} =====\n" + t)
    txt = "".join(pages)
    with open(out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(path, "pages:", len(r.pages), "chars:", len(txt), "->", out)

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    for i in (1, 2, 3):
        extract(os.path.join(base, "arx", f"p{i}.pdf"), os.path.join(base, f"p{i}.txt"))
