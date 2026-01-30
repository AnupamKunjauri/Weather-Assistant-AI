from datetime import datetime
from collections import defaultdict

# -------------------------------------------------
# FORMAT UNIX TIME
# -------------------------------------------------
def format_time(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M")

# -------------------------------------------------
# 5-DAY FORECAST (MIN / MAX) – FREE API
# -------------------------------------------------
def daily_forecast_table(forecast_list):
    """
    Converts 3-hour forecast data into daily
    min/max temperature summary.
    """

    daily_data = defaultdict(lambda: {
        "min": float("inf"),
        "max": float("-inf"),
        "condition": None
    })

    for entry in forecast_list:
        date = datetime.fromtimestamp(entry["dt"]).strftime("%A")

        temp = entry["main"]["temp"]
        condition = entry["weather"][0]["main"]

        daily_data[date]["min"] = min(daily_data[date]["min"], temp)
        daily_data[date]["max"] = max(daily_data[date]["max"], temp)

        # store first condition of the day
        if daily_data[date]["condition"] is None:
            daily_data[date]["condition"] = condition

    table = []
    for day, values in list(daily_data.items())[:5]:
        table.append({
            "Day": day,
            "Min Temp (°C)": round(values["min"], 1),
            "Max Temp (°C)": round(values["max"], 1),
            "Condition": values["condition"]
        })

    return table
