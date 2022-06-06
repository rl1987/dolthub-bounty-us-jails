#!/usr/bin/python3

import requests
import pandas as pd

def scrape_snapshot(url):
    print(url)

    # TODO

def try_scraping_at_month(year, month):
    print(year, month)

    url = "http://archive.org/wayback/available"

    request_timestamp = "{}{:02d}".format(year, month)

    params = {
        "url": "https://doc.iowa.gov/daily-statistics",
        "timestamp": request_timestamp + "15", # HACK
    }

    resp = requests.get(url, params=params)
    print(resp.url)

    json_dict = resp.json()

    closest = json_dict.get("archived_snapshots", dict()).get("closest")

    if closest is None:
        return None

    url = closest.get("url")
    timestamp = closest.get("timestamp")

    if not timestamp.startswith(request_timestamp):
        return None

    return scrape_snapshot(url)

def main():
    for year in range(2017, 2023):
        for month in range(1, 13):
            try_scraping_at_month(year, month)

if __name__ == "__main__":
    main()

