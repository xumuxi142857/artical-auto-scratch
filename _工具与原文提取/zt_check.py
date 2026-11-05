import sqlite3
con = sqlite3.connect(r"file:C:\Users\32531\Zotero\zotero.sqlite?mode=ro", uri=True, timeout=5)
c = con.cursor()
print("items:", c.execute("select count(*) from items").fetchone()[0])
print("deleted:", c.execute("select count(*) from deletedItems").fetchone()[0])
rows = c.execute("""select i.itemID, it.typeName from items i join itemTypes it on it.itemTypeID=i.itemTypeID order by i.itemID desc limit 8""").fetchall()
print(rows)
for iid, t in rows:
    t = c.execute("""select v.value from itemData d join itemDataValues v on v.valueID=d.valueID join fields f on f.fieldID=d.fieldID where d.itemID=? and f.fieldName='title'""", (iid,)).fetchone()
    a = c.execute("select count(*) from itemAttachments where parentItemID=?", (iid,)).fetchone()[0]
    print(iid, t, "atts=", a)
