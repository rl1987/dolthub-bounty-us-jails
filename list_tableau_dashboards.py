#!/usr/bin/python3

import csv
from pprint import pprint

import requests

FIELDNAMES = ["title", "description", "author_name", "url"]


def main():
    out_f = open("tableau.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    headers = {
        "authority": "public.tableau.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    }

    count = 20
    start = 0
    max_idx = 350

    while True:
        params = {
            "count": count,
            "language": "en-us",
            "query": "jail population",
            "start": start,
            "type": "vizzes",
        }

        response = requests.get(
            "https://public.tableau.com/profile/api/search/query",
            params=params,
            headers=headers,
        )
        print(response.url)

        json_dict = response.json()

        if json_dict.get("results") is None or len(json_dict.get("results")) == 0:
            break

        for result_dict in json_dict.get("results", []):
            workbook_dict = result_dict.get("workbook")

            title = workbook_dict.get("title")
            description = workbook_dict.get("description")
            author_name = result_dict.get("workbookMeta", dict()).get("authorName")
            url = "https://public.tableau.com/app/profile/{}/viz/{}".format(
                workbook_dict.get("authorProfileName"),
                workbook_dict.get("defaultViewRepoUrl"),
            )

            row = {
                "title": title,
                "description": description,
                "author_name": author_name,
                "url": url,
            }

            pprint(row)

            csv_writer.writerow(row)

        start += count
        if start >= max_idx:
            break

    out_f.close()


if __name__ == "__main__":
    main()
