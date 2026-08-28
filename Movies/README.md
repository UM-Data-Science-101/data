# Movies — Highest-Grossing Films

`movies.csv` — the all-time highest-grossing films (nominal, not adjusted for
inflation).

| Column | Meaning |
|---|---|
| `rank` | Rank by worldwide gross |
| `title` | Film title |
| `year` | Release year |
| `worldwide_gross` | Worldwide box-office gross, in US dollars |

## Source & license

Data derived from Wikipedia, ["List of highest-grossing
films"](https://en.wikipedia.org/wiki/List_of_highest-grossing_films),
available under [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0/). Box-office figures are
nominal.

## Refreshing

Re-run `movies_cleaning.py` (requires `pandas` and `lxml`) to regenerate
`movies.csv` from the current Wikipedia page:

```bash
python movies_cleaning.py
```
