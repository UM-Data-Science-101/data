"""
cancer_deaths_cleaning.py

Build two cancer death rate tables for the Module 3 project.

cancer_deaths_by_county.csv
    One row per US county (50 states and DC), all cancer sites, 2020-2024,
    from the National Cancer Institute and CDC's State Cancer Profiles
    death rate report (https://statecancerprofiles.cancer.gov/deathrates/).
    The national row and Puerto Rico are dropped. Suppressed values ("*",
    fewer than 16 deaths in the period) and "3 or fewer" counts become
    missing values.

cancer_deaths_us_by_year.csv
    The US age-adjusted cancer death rate for each year 1900-2018, from
    NCHS, "Age-adjusted Death Rates for Selected Major Causes of Death"
    (https://data.cdc.gov/d/6rkc-nb2q).

Both sources are US government works in the public domain.

Requires: pandas
Output:   cancer_deaths_by_county.csv, cancer_deaths_us_by_year.csv
"""
import urllib.request
from io import StringIO

import numpy as np
import pandas as pd

SCP_URL = ("https://statecancerprofiles.cancer.gov/deathrates/index.php?"
           "stateFIPS=00&areatype=county&cancer=001&race=00&sex=0&age=001"
           "&year=0&type=death&sortVariableName=rate&sortOrder=default"
           "&output=1")
NCHS_URL = ("https://data.cdc.gov/resource/6rkc-nb2q.csv?"
            "$limit=500&leading_causes=Cancer")


def fetch(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (DATASCI101 course data prep)"})
    return urllib.request.urlopen(req, timeout=120).read().decode("utf-8")


def clean_counties(text):
    # The report has eight lines of title above the header and notes below
    # the data. Data rows are the ones whose second field is a 5-digit FIPS.
    raw = pd.read_csv(StringIO(text), skiprows=8, dtype=str)
    raw = raw.loc[raw.iloc[:, 1].fillna("").str.fullmatch(r"\d{5}")]
    raw.columns = ["name", "fips", "rural_urban", "met_objective",
                   "death_rate", "rate_lower", "rate_upper", "rank",
                   "rank_lower", "rank_upper", "annual_deaths", "trend",
                   "aapc", "aapc_lower", "aapc_upper"]
    raw = raw.apply(lambda c: c.str.strip())
    raw = raw.loc[~raw["fips"].isin(["00000", "72001"])]

    counties = pd.DataFrame({
        "county": raw["name"].str.rsplit(", ", n=1).str[0],
        "state": raw["name"].str.rsplit(", ", n=1).str[1],
        "fips": raw["fips"],
        "rural_urban": raw["rural_urban"],
    })
    # District of Columbia has no ", State" part
    counties["state"] = counties["state"].fillna(counties["county"])
    for col in ["death_rate", "rate_lower", "rate_upper", "annual_deaths",
                "aapc", "aapc_lower", "aapc_upper"]:
        counties[col] = pd.to_numeric(raw[col], errors="coerce")
    counties["met_objective"] = raw["met_objective"].replace("*", np.nan)
    counties["trend"] = raw["trend"].replace("*", np.nan)
    columns = ["county", "state", "fips", "rural_urban", "death_rate",
               "rate_lower", "rate_upper", "met_objective", "annual_deaths",
               "trend", "aapc", "aapc_lower", "aapc_upper"]
    return counties[columns].sort_values("fips").reset_index(drop=True)


def clean_us(text):
    nchs = pd.read_csv(StringIO(text))
    us = pd.DataFrame({"year": nchs["year"].astype(int),
                       "death_rate": nchs["age_adjusted_death_rate"]})
    return us.sort_values("year").reset_index(drop=True)


if __name__ == "__main__":
    clean_counties(fetch(SCP_URL)).to_csv("cancer_deaths_by_county.csv",
                                          index=False)
    clean_us(fetch(NCHS_URL)).to_csv("cancer_deaths_us_by_year.csv",
                                     index=False)
