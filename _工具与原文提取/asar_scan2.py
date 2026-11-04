import re, sys

path = r"D:\dsHarness\resources\app.asar"
data = open(path, "rb").read()

def show(needle, before=1500, after=2500, limit=2):
    nd = needle.encode()
    idxs = [m.start() for m in re.finditer(re.escape(nd), data)]
    print("==", needle, "hits:", len(idxs), idxs[:8])
    for i in idxs[:limit]:
        seg = data[max(0, i - before): i + after].decode("utf-8", "replace")
        print("----- @", i)
        print(seg.replace("\x00", " "))

show("resolveToken", 800, 1800, 3)
show("resolveAccountOptions", 600, 1200, 2)
