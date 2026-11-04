import re, sys

num_re = re.compile(r"\d+(?:\.\d+)?%?")

def nums(path, start=1, end=None):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    text = "".join(lines[start-1:end])
    return [m.group(0) for m in num_re.finditer(text)]

if __name__ == "__main__":
    src, tr = sys.argv[1], sys.argv[2]
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    end = int(sys.argv[4]) if len(sys.argv) > 4 else None
    s = nums(src, start, end)
    t = nums(tr)
    ss, tt = set(s), set(t)
    extra = sorted(tt - ss, key=lambda x: (len(x), x))
    print("source numeric tokens:", len(s), "unique:", len(ss))
    print("translation numeric tokens:", len(t), "unique:", len(tt))
    print("numbers in translation but not in source body:", len(extra))
    print(extra[:200])
