#!/usr/bin/python3

import csv
from pprint import pprint

import requests
import us

PROXY_URL = "http://lum-customer-c_cecd546c-zone-zone_serp:3rrzr9ft4t3k@zproxy.lum-superproxy.io:22225"

FIELDNAMES = ["link", "title", "description", "state"]


def main():
    proxies = {"http": PROXY_URL, "https": PROXY_URL}

    out_f = open("serp_tableau.csv", "w", encoding="utf-8")
    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for state in us.STATES:
        q = 'site:public.tableau.com inurl:views (inmate OR jail OR prison) AND population AND ({} or {}) -"Category Management" -Killing -PoliceViolencebyState -Funding -NVWT -"Police Violence" -Netflix'.format(
            state.name, state.abbr
        )

        params = {"q": q, "lum_json": 1}

        resp = requests.get(
            "http://www.google.com/search", params=params, proxies=proxies
        )
        print(resp.url)

        json_dict = resp.json()

        for organic_hit in json_dict.get("organic"):
            row = {
                "link": organic_hit.get("link"),
                "title": organic_hit.get("title"),
                "description": organic_hit.get("description"),
                "state": state.abbr,
            }

            pprint(row)

            csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()
