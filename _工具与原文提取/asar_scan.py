import sys, re

path = r"D:\dsHarness\resources\app.asar"
needles = [b"must allow account authentication", b"ACCOUNT_SIGN_IN_REQUIRED", b"allowAccountAuth"]
data = open(path, "rb").read()  # 174MB, fine
for nd in needles:
    idxs = [m.start() for m in re.finditer(re.escape(nd), data)]
    print(nd.decode(), "hits:", len(idxs), idxs[:8])
    for i in idxs[:2]:
        seg = data[max(0, i - 1200): i + 1200]
        text = seg.decode("utf-8", "replace")
        print("  --- ctx @", i)
        print(text.replace("\x00", " ")[:2400])
