#### Data Source: https://www.zillow.com/research/data/
#### Use the 'Home Values' data with the fields:
#### 	Data Type: ZHVI All Homes (SFR, Condo/Co-op) Time Series, Smoothed, Seasonally Adjusted($)
#### 	Geography: Metro & U.S.

import pandas as pd

df = pd.read_csv('County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')

# Remove unnecessary columns
df = df[['RegionID', 'SizeRank', 'RegionName', 'State', 'Metro', 'MunicipalCodeFIPS', '2016-05-31']]

# Filter to include only Michigan counties
df = df[df['State'] == 'MI']

# Rename the 'RegionName' column to 'CountyName' for compatible merge with GraduationRates dataset and rename column with home value
df = df.rename(columns={'RegionName': 'CountyName', '2016-05-31': 'HomeValue'})

# Rename 'Saint' to 'St.' in CountyNames for compatible merge with GraduationRates dataset
df['CountyName'] = df['CountyName'].str.replace('Saint', 'St.', regex=False)

# Reset the 'SizeRank' column to reflect size with respect to other Michigan counties
df = df.sort_values(by='SizeRank').reset_index(drop=True)
df['SizeRank'] = range(1, df.shape[0]+1)

df.to_csv('Michigan_Zillow_Home_Values_2016_Cleaned.csv', index=False)