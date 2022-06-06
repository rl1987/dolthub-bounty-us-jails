#!/usr/bin/python3

import csv
from pprint import pprint

from dateutil.parser import parse
import requests
import pandas as pd
from lxml import html

def scrape_snapshot(url):
    print(url)

    resp = requests.get(url)

    tree = html.fromstring(resp.text)

    snapshot_date = tree.xpath("//h2/text()")[-1]
    snapshot_date = parse(snapshot_date)
    snapshot_date = snapshot_date.isoformat().split("T")[0]

    dfs = pd.read_html(url)
    if len(dfs) == 3:
        df = dfs[0]
    else:
        df = dfs[1]
    df = df[:-2]
    df.set_index('Institution', inplace=True)
    df.drop(columns=['Capacity', 'Medical/Segregation'], inplace=True)

    print(df)

    rows = []

    rows.append({
        'id': "IA_ANAMOSA",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Anamosa']['Current Count'].replace(",", "")),
        'source_url': url
    })

    rows.append({
        'id': "IA_CLARINDA",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Clarinda']['Current Count'].replace(",", "")),
        'source_url': url
    })

    rows.append({
        'id': "IA_FORTDODGE",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Fort Dodge']['Current Count'].replace(",", "")),
        'source_url': url
    })

    rows.append({
        'id': "IA_MTPLEASANT",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Mount Pleasant']['Current Count'].replace(",", "")),
        'source_url': url
    })

    rows.append({
        'id': "IA_NEWTON",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Newton-Medium']['Current Count'].replace(",", "")) + int(df.loc['Minimum']['Current Count'].replace(",", "")),
        'source_url': url
    })

    rows.append({
        'id': "IA_ROCKWELL",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Rockwell City']['Current Count'].replace(",", "")),
        'source_url': url
    })

    rows.append({
        'id': "IA_STATE",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Fort Madison']['Current Count'].replace(",", "")),
        'source_url': url
    })

    rows.append({
        'id': "IA_WOMEN",
        'snapshot_date': snapshot_date,
        'total': int(df.loc['Mitchellville']['Current Count'].replace(",", "")) + int(df.loc['Minimum Live-Out']['Current Count'].replace(",", "")),
        'source_url': url
    })

    pprint(rows)

    return rows

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
    out_f = open("inmate_population_snapshots.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=["id", "snapshot_date", "total", "source_url"], lineterminator="\n")
    csv_writer.writeheader()

    for year in range(2017, 2023):
        for month in range(1, 13):
            rows = try_scraping_at_month(year, month)
            
            if rows is None:
                continue

            for row in rows:
                csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()

