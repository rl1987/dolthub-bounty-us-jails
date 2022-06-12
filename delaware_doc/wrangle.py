#!/usr/bin/python3

import csv

import pandas as pd

#CSV file has to be downloaded from: https://data.delaware.gov/Public-Safety/Inmate-Population/vnau-c4rn

# INSERT INTO jails (id, county, facility_name, facility_address, facility_city, facility_state, facility_zip, is_private, in_urban_area, holds_greater_than_72_hours, holds_less_than_1_yr, felonies_greater_than_1_yr, hold_less_than_72_hours, facility_gender, num_inmates_rated_for)  VALUES ("DE_BWCI", "New Castle County", "Baylor Women's Correctional Institution
# INSERT INTO jails (id, county, facility_name, facility_address, facility_city, facility_state, facility_zip, is_private, in_urban_area, holds_greater_than_72_hours, holds_less_than_1_yr, felonies_greater_than_1_yr, hold_less_than_72_hours, facility_gender, num_inmates_rated_for)  VALUES ("DE_HRYCI", "New Castle County", "Howard R. Young Correctional Institution",  "1301 E 12th St", "Wilminton", "DE", "19802", 0, 1, -9, -9, -9, -9, 0, 1180);
# INSERT INTO jails (id, county, facility_name, facility_address, facility_city, facility_state, facility_zip, is_private, in_urban_area, holds_greater_than_72_hours, holds_less_than_1_yr, felonies_greater_than_1_yr, hold_less_than_72_hours, facility_gender, num_inmates_rated_for)  VALUES ("DE_JTVCC", "New Castle County", "James T. Vaughn Correctional Center",  "1181 Paddock Rd", "Smyrna", "DE", "19977", 0, 0, -9, -9, -9, -9, 1, 2600);
# INSERT INTO jails (id, county, facility_name, facility_address, facility_city, facility_state, facility_zip, is_private, in_urban_area, holds_greater_than_72_hours, holds_less_than_1_yr, felonies_greater_than_1_yr, hold_less_than_72_hours, facility_gender, num_inmates_rated_for)  VALUES ("DE_SCI", "Sussex County", "Sussex Correctional Institution",  "23203 Dupont Blvd", "Georgetown", "DE", "19947", 0, 0, -9, -9, -9, -9, 1, 1206);
# INSERT INTO jails (id, county, facility_name, facility_address, facility_city, facility_state, facility_zip, is_private, in_urban_area, holds_greater_than_72_hours, holds_less_than_1_yr, felonies_greater_than_1_yr, hold_less_than_72_hours, facility_gender, num_inmates_rated_for)  VALUES ("DE_CVOP", "New Castle County", "Central Violation of Probation Center",  "875 Smyrna Landing Rd", "Smyrna", "DE", "19977", 0, 0, -9, -9, -9, -9, 3, 250);
# INSERT INTO jails (id, county, facility_name, facility_address, facility_city, facility_state, facility_zip, is_private, in_urban_area, holds_greater_than_72_hours, holds_less_than_1_yr, felonies_greater_than_1_yr, hold_less_than_72_hours, facility_gender, num_inmates_rated_for)  VALUES ("DE_HDP", "New Castle County", "Hazel D. Plant Women's Treatment Facility",  "620 Baylor Blvd", "New Castle", "DE", "19720", 0, 0, -9, -9, -9, -9, 2, 0);

MAPPING = {
    "BWCI": "DE_BWCI",
    "CVOP": "DE_CVOP",
    "HDP": "DE_HDP",
    "HRYCI": "DE_HRYCI",
    "JTVCC": "DE_JTVCC",
    "SCCC": "DE_SCCC",
    "SCI": "DE_SCI",
}

def main():
    df = pd.read_csv("Inmate_Population.csv")

    df['Month'] = df['Month'].apply(lambda m: int(m.split(" - ")[0]))

    df['date'] = df.apply(lambda row: date(year=row['Year'], month=row['Month'], day=1), axis=1)
    del df['Year']
    del df['Month']
    df = df.drop( df[df['Type of Institution'] != "Prison"].index )

    del df['County Name']
    del df['Sentence Type']

    out_df = df[['Institution', 'date']]

    males = df[df['Gender'] == "Male"].groupby(['Institution', 'date']).sum('Offender Count')
    males = males.reset_index()


    return

    in_f = open("Inmate_Population.csv", "r")

    csv_reader = csv.DictReader(in_f)

    rows_by_id = dict()

    out_f = open("inmate_population_snapshots.csv", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=['id', 'snapshot_date', 'total', 'white', 'black', 'hispanic', 'asian', 'american_indian', 'male', 'female', 'source_url'], linterminator="\n")

    for in_row in csv_reader:
        facility_id = in_row.get("Institution")
        facility_id = MAPPING.get(facility_id)

        if facility_id is None:
            continue

    in_f.close()
    out_f.close()


if __name__ == "__main__":
    main()

