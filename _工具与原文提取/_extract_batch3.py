import sys, os
sys.path.insert(0, r"E:\01科研之路\a.有价值的文章\_工具与原文提取")
from extract import extract
base = r"E:\01科研之路\a.有价值的文章\2026-11-04"
items = [
 ("07_AAAI2026_MovieGraph-ToM", "原文_AAAI2026正式版.pdf"),
 ("08_ACL2026_CoSToM-Causal-Steering", "原文_ACL2026正式版.pdf"),
 ("09_AAAI2026_From-Stimuli-to-Minds-BRL", "原文_AAAI2026正式版.pdf"),
]
for d, f in items:
    p = os.path.join(base, d, f)
    out = os.path.join(base, d, "_原文提取.txt")
    extract(p, out)
