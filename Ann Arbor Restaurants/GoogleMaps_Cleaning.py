#### Data Source: https://apify.com/compass/crawler-google-places
#### Click 'Try for Free'
#### Sign in to your Google account to gain $5 of free credit
#### Fill in the following fields:
####    Search Term(s): restaurant
####    Location: Ann Arbor, MI
####    Number of places to extract: 200

import json
import pandas as pd

# REPLACE THIS WITH YOUR FILENAME
filename = 'dataset_google-maps-extractor_2025-07-08_17-45-49-850.json'

with open(filename) as f:
    data = json.load(f)

# Flatten the nested structure
df = pd.json_normalize(data)

# Retrieve nested columns
nested_cols = [col for col in df.columns if col.startswith('additionalInfo.') or col.startswith('additionalOpeningHours.')]

# Unpack nested columns
from collections import defaultdict

expanded_features = defaultdict(list)

# Expands the nested columns
for col in nested_cols:
    for index, row in df[col].items():
        # Skip if not a list
        if not isinstance(row, list):
            continue
        for entry in row:
            if isinstance(entry, dict):
                for key, value in entry.items():
                    col_name = f"{col}.{key}".replace(" ", "_").replace("-", "_")
                    expanded_features[col_name].append((index, value))

# Create each new column
for new_col, values in expanded_features.items():
    # Create a column filled with NaNs
    df[new_col] = False
    for index, value in values:
        df.at[index, new_col] = value

df.to_csv('GoogleMaps_Cleaned.csv', index=False)