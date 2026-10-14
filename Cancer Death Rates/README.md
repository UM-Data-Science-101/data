# Cancer Death Rates

Two tables of cancer death rates, all cancer sites combined. Rates are
deaths per 100,000 people per year, age-adjusted to the 2000 US standard
population.

## `cancer_deaths_by_county.csv`

One row per county in the 50 states and DC (3,142 rows), for 2020–2024.

| Column | Meaning |
|---|---|
| `county`, `state`, `fips` | County name, state name and 5-digit county FIPS code |
| `rural_urban` | `Rural` or `Urban`, from the 2023 USDA Rural–Urban Continuum Codes |
| `death_rate` | Age-adjusted cancer death rate, 2020–2024 |
| `rate_lower`, `rate_upper` | 95% confidence interval for `death_rate` |
| `met_objective` | `Yes` if `death_rate` is at most 122.7, the Healthy People 2030 target |
| `annual_deaths` | Average number of cancer deaths per year |
| `trend` | `falling`, `stable` or `rising` (see below) |
| `aapc` | Recent 5-year trend: average annual percent change in the death rate |
| `aapc_lower`, `aapc_upper` | 95% confidence interval for `aapc` |

`trend` is `falling` when the confidence interval for `aapc` is below 0,
`rising` when it is above 0 and `stable` when it includes 0.

Missing values: 58 counties have fewer than 16 cancer deaths in the period,
and their rate columns are suppressed. 80 counties have no trend.

## `cancer_deaths_us_by_year.csv`

The US age-adjusted cancer death rate for each year from 1900 to 2018
(`year`, `death_rate`). NCHS takes the years before 1999 from its
historical data. Revisions to the International Classification of Diseases
(the latest in 1999) can make the trend jump between revisions.

## Sources

- National Cancer Institute and Centers for Disease Control and Prevention,
  [State Cancer Profiles](https://statecancerprofiles.cancer.gov/deathrates/),
  death rate report for US counties, all cancer sites, all races, both
  sexes, all ages. Death data from the National Vital Statistics System.
  Retrieved 2026-10-13.
- National Center for Health Statistics, [Age-adjusted Death Rates for
  Selected Major Causes of Death](https://data.cdc.gov/d/6rkc-nb2q).
  Retrieved 2026-10-13.

Both are US government works in the public domain.

## Refreshing

```bash
python cancer_deaths_cleaning.py
```
