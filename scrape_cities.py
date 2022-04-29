#!/usr/bin/python3

import pandas as pd

def main():
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population")[4]
    
    print(df)

    out_f = open("cities.txt", "w", encoding="utf-8")

    for city in list(df['City']):
        city = city.split("[")[0]

        out_f.write(city + "\n")

    out_f.close()

if __name__ == "__main__":
    main()

