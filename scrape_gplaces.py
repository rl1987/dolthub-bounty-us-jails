#!/usr/bin/python3

import csv
from pprint import pprint

import googlemaps

API_KEY = "AIzaSyDc_6DfkpFdeQJX-KK7t_2k26aOdi-4aqU"

def main():
    gmaps = googlemaps.Client(key=API_KEY)

    out_f = open("jails.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=["name", "website", "formatted_address"])
    csv_writer.writeheader()

    in_f = open("counties.txt", "r")

    for county in in_f:
        county = county.strip()
        print(county)

        resp = gmaps.find_place("{} county jail".format(county), "textquery")
        if resp.get("candidates") is None or len(resp.get("candidates")) == 0:
            continue

        place_id = resp["candidates"][0]["place_id"]

        resp2 = gmaps.place(place_id)

        result = resp2.get("result")
        if result is None:
            continue

        row = {
            "name": result.get("name"),
            "website": result.get("website"),
            "formatted_address": result.get("formatted_address")
        }

        pprint(row)
        csv_writer.writerow(row)

    in_f.close()

    in_f = open("cities.txt", "r")

    for city in in_f:
        city = city.strip()
        print(city)

        resp = gmaps.find_place("{} city jail".format(city), "textquery")
        if resp.get("candidates") is None or len(resp.get("candidates")) == 0:
            continue

        place_id = resp["candidates"][0]["place_id"]

        resp2 = gmaps.place(place_id)

        result = resp2.get("result")
        if result is None:
            continue

        row = {
            "name": result.get("name"),
            "website": result.get("website"),
            "formatted_address": result.get("formatted_address")
        }

        pprint(row)
        csv_writer.writerow(row)

    out_f.close()

if __name__ == "__main__":
    main()

