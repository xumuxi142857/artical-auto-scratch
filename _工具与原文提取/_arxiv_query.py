import urllib.request, urllib.parse, re, time
qs = ['MovieGraph-ToM', 'CoSToM Causal-oriented Steering Theory-of-Mind', 'From Stimuli to Minds Bilateral Reinforcement Learning']
for q in qs:
    url = 'http://export.arxiv.org/api/query?search_query=' + urllib.parse.quote('all:"%s"' % q) + '&max_results=5'
    print('QUERY:', q)
    try:
        data = urllib.request.urlopen(url, timeout=60).read().decode('utf-8')
        for m in re.finditer(r'<entry>(.*?)</entry>', data, re.S):
            e = m.group(1)
            t = re.search(r'<title>(.*?)</title>', e, re.S).group(1).strip().replace('\n',' ')
            i = re.search(r'<id>(.*?)</id>', e, re.S).group(1).strip()
            p = re.search(r'<published>(.*?)</published>', e, re.S).group(1).strip()
            print(' -', i, '|', p, '|', t[:160])
    except Exception as ex:
        print('ERR', ex)
    time.sleep(3)
