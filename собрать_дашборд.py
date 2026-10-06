# Собирает дашборд.html из данные/*.json и шаблон_дашборда.html
import json, glob, datetime, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rows = []
for f in sorted(glob.glob('данные/*.json')):
    rows += json.load(open(f, encoding='utf-8'))
seen, uniq = set(), []
for r in rows:
    if r['id'] in seen: continue
    seen.add(r['id']); uniq.append(r)
regions = sorted({r['region'] for r in uniq})
meta = {'updated': datetime.date.today().strftime('%d.%m.%Y'), 'regions': regions, 'found': len(uniq)}
dump = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
html = open('шаблон_дашборда.html', encoding='utf-8').read()
html = html.replace('__DATA__', dump(uniq)).replace('__META__', dump(meta))
open('дашборд.html', 'w', encoding='utf-8').write(html)
head = '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="robots" content="noindex">\n'
body_start = html.index('<div class="wrap">')
site = head + html[:body_start] + '</head>\n<body>\n' + html[body_start:] + '\n</body>\n</html>\n'
open('index.html', 'w', encoding='utf-8').write(site)
print('дашборд.html:', len(uniq), 'машин,', ', '.join(regions))
