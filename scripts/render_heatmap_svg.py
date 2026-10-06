import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

# GitHub-like green palette
COLORS = [
    "#161b22",  # 0
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
    "#69f0a0",  # 5
]

CELL = 13
GAP = 4
STEP = CELL + GAP

WEEKS = 53
DAYS = 7

LEFT = 42
TOP = 65

WIDTH = LEFT + WEEKS * STEP + 25
HEIGHT = TOP + DAYS * STEP + 70


def get_color(level):
    level = max(0, min(int(level), 5))
    return COLORS[level]


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        days = data.get("days", [])
    else:
        days = data

    result = {}

    for item in days:
        date = item.get("date")

        if not date:
            continue

        # Support different formats in our JSON
        if "level" in item:
            value = item["level"]
        elif "count" in item:
            value = item["count"]
        elif "contributions" in item:
            value = item["contributions"]
        else:
            value = 0

        result[date] = int(value)

    return result


def get_week_start(date_obj):
    """
    GitHub-style weeks start on Sunday.
    Python weekday():
    Monday = 0
    Sunday = 6
    """
    days_since_sunday = (date_obj.weekday() + 1) % 7
    return date_obj - timedelta(days=days_since_sunday)


def build_svg(days):
    if not days:
        raise ValueError("No contribution data found.")

    # Convert date strings to datetime objects
    parsed = {}

    for date_str, level in days.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        parsed[date_obj] = level

    # Find all calendar weeks
    week_starts = sorted(
        set(get_week_start(date_obj) for date_obj in parsed)
    )

    # Keep latest 53 weeks
    week_starts = week_starts[-WEEKS:]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

    <rect
        width="100%"
        height="100%"
        rx="14"
        fill="#0d1117"/>

    <text
        x="20"
        y="32"
        fill="#f0f6fc"
        font-family="Arial, sans-serif"
        font-size="16"
        font-weight="600">
        GitHub Contributions
    </text>
'''

    # Month labels
    last_month = None

    for week_index, week_start in enumerate(week_starts):

        month_name = week_start.strftime("%b")

        if month_name != last_month:

            x = LEFT + week_index * STEP

            svg += f'''
    <text
        x="{x}"
        y="52"
        fill="#8b949e"
        font-family="Arial, sans-serif"
        font-size="10">
        {month_name}
    </text>
'''

            last_month = month_name

    # Contribution grid
    for week_index, week_start in enumerate(week_starts):

        for day_index in range(DAYS):

            current_date = week_start + timedelta(days=day_index)

            level = parsed.get(current_date, 0)

            x = LEFT + week_index * STEP
            y = TOP + day_index * STEP

            color = get_color(level)

            delay = (week_index * DAYS + day_index) * 0.008

            svg += f'''
    <rect
        x="{x}"
        y="{y}"
        width="{CELL}"
        height="{CELL}"
        rx="3"
        fill="{color}"
        opacity="0">

        <animate
            attributeName="opacity"
            from="0"
            to="1"
            begin="{delay:.3f}s"
            dur="0.25s"
            fill="freeze"/>
    </rect>
'''

    # Legend
    legend_y = TOP + DAYS * STEP + 30

    svg += f'''
    <text
        x="20"
        y="{legend_y}"
        fill="#8b949e"
        font-family="Arial, sans-serif"
        font-size="11">
        Less
    </text>
'''

    for i in range(1, 6):

        x = 55 + (i - 1) * 18

        svg += f'''
    <rect
        x="{x}"
        y="{legend_y - 11}"
        width="13"
        height="13"
        rx="3"
        fill="{COLORS[i]}"/>
'''

    svg += f'''
    <text
        x="155"
        y="{legend_y}"
        fill="#8b949e"
        font-family="Arial, sans-serif"
        font-size="11">
        More
    </text>

    </svg>
'''

    return svg


def main():

    days = load_data()

    svg = build_svg(days)

    OUTPUT_FILE.write_text(svg, encoding="utf-8")

    print("Created contrib-heatmap.svg")


if __name__ == "__main__":
    main()