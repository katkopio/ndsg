# DS7-1-0420
# DS7-2-0421
# DS7-3-0422
# DS7-4-0424
# DS7-5-0425
# DS7-6-0426
# AK-04561-Details (6)

import pandas as pd 

filename = 'AK-04561-Details (6)'
df = pd.read_excel(f'Excel/{filename}.xlsx', sheet_name=0, skiprows=2, usecols=[0,1,2,3,4,5,6])
df.to_csv(f'CSV/{filename}.csv', index=False)