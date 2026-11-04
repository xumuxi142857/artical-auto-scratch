path = r"D:\dsHarness\resources\app.asar"
data = open(path, "rb").read()
start, end = 50_900_000, 51_340_000
seg = data[start:end].decode("utf-8", "replace")
open(r"E:\01科研之路\a.有价值的文章\_工具与原文提取\account_region.txt", "w", encoding="utf-8").write(seg)
print(len(seg))
