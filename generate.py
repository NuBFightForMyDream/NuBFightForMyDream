import argparse, datetime, html, random, urllib.request
from html.parser import HTMLParser
from pathlib import Path

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__(); self.days = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-date' in a and 'data-level' in a:
            self.days[a['data-date']] = int(a['data-level'])

p = argparse.ArgumentParser()
p.add_argument('--demo', action='store_true')
args = p.parse_args()
user = 'NuBFightForMyDream'
if args.demo:
    rng = random.Random(8)
    start = datetime.date.today() - datetime.timedelta(days=364)
    days = {(start + datetime.timedelta(days=i)).isoformat(): rng.choices(range(5), [5,3,2,1,1])[0] for i in range(365)}
else:
    req = urllib.request.Request(f'https://github.com/users/{user}/contributions', headers={'User-Agent':'Powerpuff-Profile'})
    parser = Calendar()
    with urllib.request.urlopen(req, timeout=30) as response:
        parser.feed(response.read().decode())
    days = parser.days
    if len(days) < 300:
        raise RuntimeError('Calendar unavailable: keeping existing SVG unchanged')
first = datetime.date.fromisoformat(min(days))
start = first - datetime.timedelta(days=(first.weekday()+1)%7)
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="340" viewBox="0 0 920 340" role="img" aria-label="Powerpuff themed contribution calendar">', '<rect width="920" height="340" rx="24" fill="#fff2f8"/>', '<path d="M0 280H920V340H0Z" fill="#291c46"/>']
for i in range(24):
    h = 20 + (i * 17 % 52)
    svg.append(f'<rect x="{i*40}" y="{280-h}" width="30" height="{h}" fill="#291c46"/>')
svg += ['<text x="35" y="47" font-family="Verdana,sans-serif" font-size="27" font-weight="bold" fill="#291c46">SUGAR, SPICE &amp; CODE</text>',f'<text x="35" y="74" font-family="Verdana,sans-serif" font-size="13" fill="#715c85">@{user} · '+('DEMO DATA — layout preview' if args.demo else 'GitHub contribution activity')+'</text>']
colors = ['#eadfe9', '#f68ab9', '#66c9ee', '#72d58c', '#bd4389']
for date, level in sorted(days.items()):
    delta = (datetime.date.fromisoformat(date)-start).days
    x,y = 42 + (delta//7)*15, 106 + (delta%7)*16
    svg.append(f'<rect x="{x}" y="{y}" width="11" height="12" rx="3" fill="{colors[level]}"><title>{date}: contribution intensity {level}/4</title></rect>')
for x,color,name in [(42,'#f68ab9','BLOSSOM'),(235,'#66c9ee','BUBBLES'),(428,'#72d58c','BUTTERCUP')]:
    svg.append(f'<circle cx="{x+7}" cy="306" r="7" fill="{color}"/><text x="{x+23}" y="311" font-family="Verdana,sans-serif" font-size="12" font-weight="bold" fill="white">{name}</text>')
svg.append('<text x="650" y="311" font-family="Verdana,sans-serif" font-size="11" fill="#ffdaeb">A little code saves the day.</text></svg>')
Path('assets').mkdir(exist_ok=True)
Path('assets/powerpuff-contributions.svg').write_text('\n'.join(svg))
