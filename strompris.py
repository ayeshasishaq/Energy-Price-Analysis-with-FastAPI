#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""
from __future__ import annotations

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache
from datetime import datetime, timedelta


# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """
    Fetches electricity prices for a specified date and location from the API.

    Args:
        date (datetime.date, optional): The date for which to fetch the prices. Defaults to the current date.
        location (str, optional): The location code for which to fetch prices.

    Returns:
        pd.DataFrame: A DataFrame containing electricity prices for the specified date and location. Includes columns such as 'time_start' and 'NOK_per_kWh'.
    """
    if date is None:
        date = datetime.now().date()

    #print(f"Fetching prices for date: {date}, location: {location}")

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{date.month:02d}-{date.day:02d}_{location}.json"

    #print(f"Constructed URL: {url}")
    
    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")


    data = response.json()

    df = pd.DataFrame(data)
    #df["time_start"] = pd.to_datetime(df["time_start"]).dt.tz_localize(None)
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert("Europe/Oslo")

    return df

LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen"}



def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """
    Fetches electricity prices for multiple days and locations, compiling them into a single DataFrame.

    Args:
        end_date (datetime.date, optional): The end date for the data fetching period. Defaults to today.
        days (int, optional): Number of days to include in the data fetching period, counting backwards from the end date. Defaults to 7.
        locations (list[str], optional): List of location codes for which to fetch data. If None, fetches data for all available locations.

    Returns:
        pd.DataFrame: A DataFrame containing the combined electricity prices data for the specified period and locations.
    """
    if end_date is None:
        end_date = datetime.now().date()
    start_date = end_date - timedelta(days - 1)
    print(f"Fetching prices from {start_date} to {end_date} for locations: {locations}")

    all_data = []
    for single_date in (start_date + timedelta(n) for n in range(days)):
        for location in locations:
            daily_data = fetch_day_prices(single_date, location)
            print(f"Sample data for {single_date} at {location}: {daily_data.head()}")
            daily_data["location_code"] = location
            daily_data["location"] = LOCATION_CODES[location]
            all_data.append(daily_data)
    #print(f"Fetching prices from {start_date} to {end_date} for locations: {locations}")
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """
    Generates a line chart of electricity prices over time for different locations.

    Args:
        df (pd.DataFrame): A DataFrame containing electricity prices data.

    Returns:
        alt.Chart: An Altair Chart representing the line chart.
    """
    aggregated_df = df.groupby(['time_start', 'location']).agg({'NOK_per_kWh': 'mean'}).reset_index()

    chart = alt.Chart(df).mark_line().encode(
        x='time_start:T',
        y='NOK_per_kWh:Q',
        color='location:N',
        tooltip=['location', 'NOK_per_kWh', 'time_start']
    ).properties(
        title='Energy Prices Over Time by Location'
    )
    return chart



# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis: time_start 
    y-axis: cost in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...


# Task 5.6
ACTIVITIES = {
    "shower": 2.5,
    "cooking": 3.0,
    "watch_tv": 1.0,
    "baking": 2.0,  
    "heat": 1.5,    
}

def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity,

    Args:
        df (pd.DataFrame): DataFrame containing energy prices.
        activity (str): Name of the activity.
        minutes (float): Duration of the activity in minutes.

    Returns:
        alt.Chart: Altair chart displaying energy prices for an activity.
    """
    if activity not in ACTIVITIES:
        raise ValueError(f"Invalid activity: {activity}. Available activities: {', '.join(ACTIVITIES.keys())}")

    df['activity'] = activity

    # Filter data for specified activity
    data_for_activity = df[df['activity'] == activity]

    # Calculate cost for the activity 
    activity_rate_kW = ACTIVITIES[activity]  
    price_per_kWh = data_for_activity['NOK_per_kWh']  
    duration_hours = minutes / 60 

    # Calculate the cost
    data_for_activity['cost'] = price_per_kWh * activity_rate_kW * duration_hours

    # Creating altair chart
    chart = alt.Chart(data_for_activity).mark_line().encode(
        x=alt.X('time_start:T', title='Time in hour'),
        y=alt.Y('cost:Q', title='Cost(NOK)'),
        color='location:N',
        tooltip=['location', 'cost', 'time_start']
    ).properties(
        title=f'Cost of {activity} over time'
    )
    return chart



def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
