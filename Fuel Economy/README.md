# Fuel Economy

`fuel_economy_2025.csv` holds EPA fuel economy ratings for model year 2025
vehicles that run on gasoline alone (626 rows). Each row is a vehicle
configuration EPA tested, meaning one make and model with one engine,
transmission and drive. A row is not a car sold, so the table is not weighted
by sales. Some rows share a model, engine and transmission and differ in
details not kept here, such as the engine code.

Electric, hybrid, plug-in hybrid, diesel, flex-fuel and fuel cell vehicles
are not included.

| Column | Meaning |
|---|---|
| `id` | EPA record id in the fueleconomy.gov vehicle file |
| `make`, `model` | Manufacturer brand and model name |
| `vehicle_class` | EPA size class (e.g. `Compact Cars`, `Small Sport Utility Vehicle 4WD`, `Standard Pickup Trucks 4WD`) |
| `drive` | `Front-Wheel Drive`, `Rear-Wheel Drive`, `All-Wheel Drive`, `4-Wheel Drive` or `Part-time 4-Wheel Drive` |
| `transmission` | EPA transmission code, e.g. `Automatic (S8)` or `Manual 6-spd` |
| `transmission_type` | `Automatic`, `Manual` or `CVT` (continuously variable) |
| `gears` | Number of gears; missing for CVTs, which have no fixed number |
| `cylinders` | Engine cylinders |
| `displacement` | Engine displacement in liters |
| `turbo`, `supercharged` | `Yes` if the engine is turbocharged or supercharged |
| `fuel` | Fuel the vehicle uses: `Regular`, `Premium` or `Midgrade` |
| `start_stop` | `Yes` if the engine shuts off when the vehicle stops |
| `gas_guzzler` | `Yes` if the vehicle is subject to the gas guzzler tax |
| `city_mpg`, `highway_mpg`, `combined_mpg` | EPA city, highway and combined miles per gallon |
| `co2` | Tailpipe CO2, grams per mile, from EPA tests |
| `annual_fuel_cost` | EPA's estimated yearly fuel cost in dollars, for 15,000 miles with 55% city driving at the price of the vehicle's fuel |
| `fe_score` | EPA fuel economy score, 1 (worst) to 10 (best) |

## Source

US Department of Energy and US Environmental Protection Agency,
[fueleconomy.gov](https://www.fueleconomy.gov/feg/download.shtml), vehicle
data file `vehicles.csv`. Column definitions are on the [web services
page](https://www.fueleconomy.gov/feg/ws/index.shtml#vehicle). Retrieved
2026-10-30.

The site says its documents "may be freely distributed and used for
non-commercial, scientific and educational purposes"
([disclaimer](https://www.fueleconomy.gov/feg/ORNL-disclaimer.htm)).

## Refreshing

```bash
python fuel_economy_cleaning.py
```

EPA revises the vehicle file over time, so a refresh can change values. The
committed CSV is the version the Fall 2026 Module 4 project uses.
