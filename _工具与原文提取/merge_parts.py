import os, sys, glob, re

# usage: python merge_parts.py <folder> <outname>
folder, outname = sys.argv[1], sys.argv[2]
parts = sorted(glob.glob(os.path.join(folder, "part*.md")))
if not parts:
    print("NO PARTS FOUND in", folder)
    sys.exit(1)
buf = []
for p in parts:
    with open(p, encoding="utf-8") as f:
        t = f.read().strip()
    buf.append(t)
txt = "\n\n".join(buf) + "\n"
out = os.path.join(folder, outname)
with open(out, "w", encoding="utf-8") as f:
    f.write(txt)
print("merged", len(parts), "parts ->", out)
print("chars:", len(txt), "lines:", txt.count("\n"))
