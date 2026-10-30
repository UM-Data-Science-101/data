"""
fuel_economy_cleaning.py

Build the model year 2025 gasoline vehicle table for the Module 4 project.

fuel_economy_2025.csv
    One row per vehicle configuration that EPA tested for model year 2025
    and that runs on gasoline alone, from the fueleconomy.gov vehicle file
    (https://www.fueleconomy.gov/feg/download.shtml). Electric, hybrid,
    plug-in hybrid, diesel, flex-fuel and fuel cell vehicles are dropped
    (any row with an `atvType`). Columns are renamed and recoded; see
    README.md.

fueleconomy.gov states that its documents "may be freely distributed and
used for non-commercial, scientific and educational purposes"
(https://www.fueleconomy.gov/feg/ORNL-disclaimer.htm).

EPA revises the vehicle file over time, so rerunning this script can give
slightly different values than the committed CSV.

Requires: pandas
Output:   fuel_economy_2025.csv
"""
import io
import urllib.request
import zipfile

import numpy as np
import pandas as pd

URL = "https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip"
YEAR = 2025


def fetch(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (DATASCI101 course data prep)"})
    return urllib.request.urlopen(req, timeout=120).read()


def yes_no(flag):
    return np.where(flag, "Yes", "No")


def clean(raw):
    gas = raw.loc[(raw["year"] == YEAR)
                  & raw["atvType"].isna()
                  & raw["fuelType1"].str.contains("Gasoline")]

    # "Automatic (variable gear ratios)" and the "AV-S" codes are
    # continuously variable transmissions, which have no fixed gear count
    trany = gas["trany"]
    cvt = trany.str.contains("variable") | trany.str.contains("AV-")
    transmission_type = np.where(
        cvt, "CVT", np.where(trany.str.startswith("Manual"), "Manual", "Automatic"))
    gears = pd.to_numeric(trany.str.extract(r"(\d+)")[0], errors="coerce")
    gears = gears.where(~cvt)

    cars = pd.DataFrame({
        "id": gas["id"],
        "make": gas["make"],
        "model": gas["model"],
        "vehicle_class": gas["VClass"],
        "drive": gas["drive"],
        "transmission": trany,
        "transmission_type": transmission_type,
        "gears": gears,
        "cylinders": gas["cylinders"].astype(int),
        "displacement": gas["displ"],
        "turbo": yes_no(gas["tCharger"] == "T"),
        "supercharged": yes_no(gas["sCharger"] == "S"),
        "fuel": gas["fuelType1"].str.replace(" Gasoline", ""),
        "start_stop": yes_no(gas["startStop"] == "Y"),
        "gas_guzzler": yes_no(gas["guzzler"].notna()),
        "city_mpg": gas["city08"],
        "highway_mpg": gas["highway08"],
        "combined_mpg": gas["comb08"],
        "co2": gas["co2TailpipeGpm"].round(1),
        "annual_fuel_cost": gas["fuelCost08"],
        # ghgScore is dropped: for 2025 it equals feScore in all but one row
        "fe_score": gas["feScore"].replace(-1, np.nan),
    })
    return cars.sort_values(["make", "model", "id"]).reset_index(drop=True)


if __name__ == "__main__":
    archive = zipfile.ZipFile(io.BytesIO(fetch(URL)))
    raw = pd.read_csv(archive.open("vehicles.csv"), low_memory=False)
    cars = clean(raw)
    cars.to_csv("fuel_economy_2025.csv", index=False)
    print(f"fuel_economy_2025.csv: {len(cars)} rows")
