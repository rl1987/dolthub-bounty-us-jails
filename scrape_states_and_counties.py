#!/usr/bin/python3

import pandas as pd

def main():
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents")[0]

    print(df)

    out_f = open("counties.txt", "w", encoding="utf-8")
    
    for county in list(df['County or equivalent']):
        if "City" in county:
            continue

        if "Municipality" in county:
            continue

        if "Town" in county:
            continue

        if "Parish" in county:
            continue

        if "Island" in county:
            continue
        
        out_f.write(county + "\n")

    out_f.close()
    
    out_f = open("states.txt", "w", encoding="utf-8")

    for state in set(df['State or equivalent']):
        out_f.write(state + "\n")

    out_f.close()

if __name__ == "__main__":
    main()

