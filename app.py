"""
strompris fastapi app entrypoint
"""
from __future__ import annotations

import datetime
import os
from typing import List, Optional
import pandas as pd


import altair as alt
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
if os.path.exists("docs/_build/html"):
    app.mount("/help", StaticFiles(directory="docs/_build/html", html = True), name="help")







# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("strompris.html", {
        "request": request,
        "location_codes": LOCATION_CODES,
        "today": datetime.date.today()
    })




# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)


@app.get("/plot_prices.json")
async def plot_prices_json(
    locations: Optional[List[str]] = Query(None),
    end: Optional[str] = None,
    days: Optional[int] = 7
):

    if not locations:
        locations = list(LOCATION_CODES.keys())

    if end:
        end_date = datetime.date.fromisoformat(end)
    else:
        end_date = datetime.date.today()

    df = fetch_prices(end_date=end_date, days=days, locations=locations)
    chart = plot_prices(df)
    return chart.to_dict()



# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date

@app.get("/activity")
async def activity(request: Request):
    return templates.TemplateResponse("activity.html", {
        "request": request,
        "location_codes": LOCATION_CODES,
        "activities": ACTIVITIES,
        "today": datetime.date.today()
    })

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)

@app.get("/plot_activity.json")
async def plot_activity_json(
    location: str = "NO1",
    activity: str = "shower",
    minutes: int = 10
):
    # Fetch prices for the current day
    end_date = datetime.date.today()
    df = fetch_prices(end_date=end_date, days=1, locations=[location])

    chart = plot_activity_prices(df, activity, minutes)
    return chart.to_dict()


...


# mount your docs directory as static files at `/help`

...


def main():
    """Launches the application on port 5000 with uvicorn"""
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    """
    Main function to run the module as a script. Fetches price data and displays a chart.
    """
    main()
