import zipfile
z = zipfile.ZipFile(r"D:\zotero\app\omni.ja")
s = z.read("chrome/content/zotero/xpcom/server/saveSession.js").decode("utf-8","replace")
open(r"E:\01科研之路\a.有价值的文章\_工具与原文提取\saveSession.js","w",encoding="utf-8").write(s)
print(len(s))
