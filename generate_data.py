import json
import random
from datetime import datetime, timedelta

data = {
    "stat_for_day": {
        "date": "17.12.2025",
        "habits": {
            "good_habits": {
                "73": {"ended": random.choice([True, False])},
                "75": {"ended": random.choice([True, False])}
            },
            "bad_habits": {
                str(i): {"ended": random.choice([True, False])}
                for i in range(74, 89)
            }
        }
    },
    "habits": {
        "last_id": 88,
        "good_habits": {
            "73": {"name": "asd", "points": 0},
            "75": {"name": "asdsss", "points": 0}
        },
        "bad_habits": {
            str(i): {"name": "asd", "points": 0}
            for i in range(74, 80)
        }
    }
}

data["habits"]["bad_habits"].update({
    "80": {"name": "aaaa", "points": 0},
    "81": {"name": "ssssssssss", "points": 0},
    "82": {"name": "ssssssssssssdddddddddd", "points": 0},
    "83": {"name": "aaaaaaaaaaaaaaaaaaa", "points": 0},
    "84": {"name": "sadasd", "points": 0},
    "85": {"name": "asd", "points": 0},
    "86": {"name": "asdsad", "points": 0},
    "87": {"name": "asdasd", "points": 0},
    "88": {"name": "asdasd", "points": 0}
})

# Генерация stats на 180 дней
start_date = datetime.strptime("21.06.2025", "%d.%m.%Y")
stats = []
for i in range(180):
    date = (start_date + timedelta(days=i)).strftime("%d.%m.%Y")
    good = round(random.uniform(0, 1), 2)
    bad = round(random.uniform(0, 1), 2)
    stats.append({
        "date": date,
        "good_habit_percents": good,
        "bad_habit_percents": bad
    })

data["stats"] = stats

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)