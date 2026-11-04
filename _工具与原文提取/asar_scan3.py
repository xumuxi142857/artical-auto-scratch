import re

path = r"D:\dsHarness\resources\app.asar"
data = open(path, "rb").read()
out = []

def show(needle, before=1500, after=3000, limit=1, label=""):
    nd = needle.encode()
    idxs = [m.start() for m in re.finditer(re.escape(nd), data)]
    out.append(f"== {label or needle} hits: {len(idxs)} {idxs[:8]}")
    for i in idxs[:limit]:
        seg = data[max(0, i - before): i + after].decode("utf-8", "replace")
        out.append(f"----- @{i}")
        out.append(seg.replace("\x00", " "))

show("allowAuthentication", 2500, 3500, 2)
show("destinations", 1500, 3000, 2)
open(r"E:\01科研之路\a.有价值的文章\_工具与原文提取\asar_ctx.txt", "w", encoding="utf-8").write("\n".join(out))
print("ok", sum(len(x) for x in out))
