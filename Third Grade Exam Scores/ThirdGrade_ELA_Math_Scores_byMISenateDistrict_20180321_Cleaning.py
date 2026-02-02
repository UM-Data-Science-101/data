#### Data Source: https://catalog.data.gov/dataset/thirdgrade-ela-math-scores-bytract-08032017-eca07

import pandas as pd

df = pd.read_csv('ThirdGrade_ELA_Math_Scores_byMISenateDistrict_20180321.csv')

# Remove unnecessary columns
df = df.drop(['OBJECTID', 'SenateName', 'Shape__Area', 'Shape__Length'], axis=1)

df.to_csv('ThirdGrade_ELA_Math_Scores_byMISenateDistrict_20180321_Cleaned.csv', index=False)