import json
import random
from datetime import date, timedelta

log = {}
today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    day_str = str(day)
    log[day_str] = random.randint(0, 9)

with open("activity_log.json", "w") as file:
    json.dump(log, file)

print("Generated test activity data for the last 90 days.")