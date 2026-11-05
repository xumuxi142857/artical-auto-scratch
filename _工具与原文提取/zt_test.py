import json, urllib.request, sys
body = {
 "sessionID": "dsh-test-0001",
 "uri": "https://proceedings.mlr.press/v306/zhong26i.html",
 "items": [{
   "itemType": "conferencePaper",
   "title": "[TEST] From Shortcuts to Reasoning: Robust Post-Training of Theory of Mind with Reinforcement Learning",
   "creators": [{"firstName":"Jike","lastName":"Zhong","creatorType":"author"}],
   "date": "2026",
   "proceedingsTitle": "Proceedings of the 43rd International Conference on Machine Learning",
   "conferenceName": "ICML 2026",
   "publisher": "PMLR",
   "volume": "306",
   "pages": "164397-164419",
   "url": "https://proceedings.mlr.press/v306/zhong26i.html",
   "abstractNote": "dsh connector test",
   "tags": [{"tag":"ToM"},{"tag":"dsh-test"}],
   "attachments": [{"title":"Full Text PDF (test)","url":"http://127.0.0.1:8765/%E5%8E%9F%E6%96%87_ICML2026%E6%AD%A3%E5%BC%8F%E7%89%88_PMLR306.pdf","mimeType":"application/pdf"}]
 }]
}
req = urllib.request.Request("http://127.0.0.1:23119/connector/saveItems",
    data=json.dumps(body).encode(), method="POST",
    headers={"Content-Type":"application/json","X-Zotero-Connector-API-Version":"3"})
try:
    r = urllib.request.urlopen(req, timeout=60)
    print("status", r.status); print(r.read().decode()[:800])
except Exception as e:
    print("ERR", e)
    try: print(e.read().decode()[:800])
    except Exception: pass
