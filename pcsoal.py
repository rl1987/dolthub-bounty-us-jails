#!/usr/bin/python3

from datetime import date
from urllib.parse import urljoin

import requests
from lxml import html

def main():
    url = "https://www.pcsoal.org/roster.php"

    while url is not None:
        resp = requests.get(url)
        print(resp.url)

        tree = html.fromstring(resp.text)

        for profile_link in tree.xpath('//a[./strong[text() = "View Profile >>>"]]'):
            profile_url = profile_link.get('href')
            profile_url = urljoin(resp.url, profile_url)

            resp2 = requests.get(profile_url)
            print(resp2.url)

        url = None

        next_page_link = tree.xpath('//a[@class="page_num" and text()=">"]')

        if len(next_page_link) == 0:
            break

        next_page_link = next_page_link[-1]
        next_page_link = next_page_link.get('href')

        if next_page_link is not None:
            url = urljoin(resp.url, next_page_link)

if __name__ == "__main__":
    main()
