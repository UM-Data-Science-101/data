"""
movies_cleaning.py

Build a small, teaching-friendly dataset of the highest-grossing films from
Wikipedia's "List of highest-grossing films".

Source: Wikipedia, "List of highest-grossing films"
(https://en.wikipedia.org/wiki/List_of_highest-grossing_films). Text is
available under CC BY-SA 4.0. Box-office figures are nominal (not adjusted
for inflation).

Re-run each semester to refresh the list to the current top 50.

Requires: pandas, lxml   (pip install pandas lxml)
Output:   movies.csv
Columns:  rank, title, year, worldwide_gross
"""
import re
import urllib.request
from io import StringIO

import pandas as pd

URL = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
WANTED = {"Rank", "Title", "Worldwide gross", "Year"}


def fetch_tables(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (DATASCI101 course data prep)"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    return pd.read_html(StringIO(html))


def clean_gross(value):
    """'T$2,257,906,828' or 'A1$4,157,000,000' -> integer dollars.

    Footnote markers get merged in front of the '$', so take the digits
    after the last '$'.
    """
    digits = re.sub(r"[^\d]", "", str(value).split("$")[-1])
    return int(digits) if digits else None


def clean_title(value):
    """Strip footnote daggers/markers (e.g. a trailing '†')."""
    return re.sub(r"[†‡*]", "", str(value)).strip()


def first_int(value):
    """Leading integer of a cell, ignoring merged footnote letters ('43JP')."""
    m = re.match(r"\d+", str(value))
    return int(m.group()) if m else None


def first_year(value):
    """First 4-digit run in a cell."""
    m = re.search(r"\d{4}", str(value))
    return int(m.group()) if m else None


def main():
    tables = fetch_tables(URL)
    table = next(t for t in tables if WANTED.issubset(set(t.columns)))

    df = pd.DataFrame({
        "rank": table["Rank"].map(first_int),
        "title": table["Title"].map(clean_title),
        "year": table["Year"].map(first_year),
        "worldwide_gross": table["Worldwide gross"].map(clean_gross),
    }).dropna()

    df = (df.astype({"rank": int, "year": int, "worldwide_gross": int})
            .sort_values("rank")
            .reset_index(drop=True))

    df.to_csv("movies.csv", index=False)
    return df


if __name__ == "__main__":
    result = main()
    print(f"Wrote movies.csv: {result.shape[0]} rows x {result.shape[1]} cols")
    print(result.head(10).to_string(index=False))
