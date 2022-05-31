#!/usr/bin/python3

import csv
from urllib.parse import urljoin
from pprint import pprint

import requests
from lxml import html


def main():
    resp = requests.get(
        "https://en.wikipedia.org/wiki/List_of_United_States_state_correction_agencies"
    )
    print(resp.url)

    tree = html.fromstring(resp.text)

    out_f = open("state_level.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(
        out_f,
        fieldnames=["name", "wikipedia_url", "official_site_url"],
        lineterminator="\n",
    )
    csv_writer.writeheader()

    for link in tree.xpath('//a[contains(text(), "Department")]/@href'):
        url = urljoin(resp.url, link)

        resp2 = requests.get(url)
        print(resp2.url)

        tree2 = html.fromstring(resp2.text)

        official_site_url = tree2.xpath(
            '//a[contains(@href, ".us") or contains(@href, ".gov")]/@href'
        )
        if len(official_site_url) > 0:
            official_site_url = official_site_url[0]
        else:
            continue

        title = tree2.xpath("//title/text()")[0].split(" - ")[0]

        row = {
            "name": title,
            "wikipedia_url": resp2.url,
            "official_site_url": official_site_url,
        }

        pprint(row)

        csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()
