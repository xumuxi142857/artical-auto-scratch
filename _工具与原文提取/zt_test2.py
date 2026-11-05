import json, urllib.request, uuid, os
PDF = r"E:\01科研之路\a.有价值的文章\2026-11-04\01_ICML2026_From-Shortcuts-to-Reasoning-ToM-with-RL\原文_ICML2026正式版_PMLR306.pdf"
sid = str(uuid.uuid4())
key = "dsh-smoke-001"
body = {"sessionID": sid, "uri": "https://proceedings.mlr.press/v306/zhong26i.html",
        "items": [{"id": key, "itemType": "conferencePaper",
          "title": "[TEST2] From Shortcuts to Reasoning",
          "creators": [{"firstName":"Jike","lastName":"Zhong","creatorType":"author"}],
          "date":"2026","proceedingsTitle":"Proceedings of ICML 2026","pages":"164397-164419",
          "url":"https://proceedings.mlr.press/v306/zhong26i.html","tags":[{"tag":"dsh-test"}]}]}
req = urllib.request.Request("http://127.0.0.1:23119/connector/saveItems", data=json.dumps(body).encode(),
    method="POST", headers={"Content-Type":"application/json","X-Zotero-Connector-API-Version":"3"})
r = urllib.request.urlopen(req, timeout=60); print("saveItems", r.status, r.read()[:200])
data = open(PDF,"rb").read()
meta = json.dumps({"sessionID": sid, "parentItemID": key, "title": "Full Text PDF", "url": "https://proceedings.mlr.press/v306/zhong26i.pdf"})
req2 = urllib.request.Request("http://127.0.0.1:23119/connector/saveAttachment", data=data, method="POST",
    headers={"Content-Type":"application/pdf","Content-Length":str(len(data)),"X-Metadata":meta})
try:
    r2 = urllib.request.urlopen(req2, timeout=120); print("saveAttachment", r2.status, r2.read()[:200])
except Exception as e:
    print("attach ERR", e, getattr(e,'read',lambda:b'')()[:300])
