#### Data Source: https://catalog.data.gov/dataset/monthly-rates-of-laboratory-confirmed-covid-19-hospitalizations-from-the-covid-net-surveil

import pandas as pd

df = pd.read_csv('Monthly_Rates_of_Laboratory-Confirmed_COVID-19_Hospitalizations_from_the_COVID-NET_Surveillance_System.csv')

# Create separate 'Year' and 'Month' columnss
df['_YearMonth'] = df['_YearMonth'].astype(int)
df['Year'] = df['_YearMonth'] // 100
df['Month'] = df['_YearMonth'] % 100

# Remove unnecessary columns
df = df.drop(['_YearMonth'], axis=1)

df.to_csv('Monthly_Rates_of_Laboratory-Confirmed_COVID-19_Hospitalizations_from_the_COVID-NET_Surveillance_System_Cleaned.csv', index=False)