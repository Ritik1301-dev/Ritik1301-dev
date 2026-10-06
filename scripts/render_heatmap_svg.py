import json
from pathlib import Path

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

data = data[-371:]

while len(data) < 371:
    data.insert(0, {"date": "", "level": 0})

BOX = 12
GAP = 3
WIDTH = 860
HEIGHT = 220

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect width="100%" height="100%" fill="#0d1117"/>

<text x="20" y="25"
fill="#c9d1d9"
font-family="Arial"
font-size="16"
font-weight="bold">
GitHub Contributions
</text>
'''

for i, item in enumerate(data):
    col = i // 7
    row = i % 7

    x = 20 + col * (BOX + GAP)
    y = 45 + row * (BOX + GAP)

    level = int(item.get("level", 0))
    level = max(0, min(level, 5))

    svg += f'''
<rect
x="{x}"
y="{y}"
width="{BOX}"
height="{BOX}"
rx="3"
fill="{COLORS[level]}"/>
'''

svg += '''
<text x="20" y="190"
fill="#8b949e"
font-family="Arial"
font-size="12">
Less
</text>
'''

for i in range(6):
    x = 55 + i * 18

    svg += f'''
<rect x="{x}" y="181"
width="12" height="12"
rx="3"
fill="{COLORS[i]}"/>
'''

svg += '''
<text x="175" y="190"
fill="#8b949e"
font-family="Arial"
font-size="12">
More
</text>

</svg>
'''

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg)

print("Created contrib-heatmap.svg")