
import pandas as pd
import random
import re
# Get data
hh_data = pd.read_csv('..\\data\\opt_msna22_data_raw.csv', low_memory = False)

# Crete random numbers
random_list = []
# Set a length of the list to 10
for i in range(0, 400):
    # any random numbers from 0 to 1000
    random_list.append(random.randint(50, 5000))
print(random_list)

# Create sample data frame
df = pd.DataFrame({
    "id": range(0,100),
  "boys-0_18" : random_list[0:100],
  "girls-0_18":  random_list[100:200],
  "men-18_99":  random_list[200:300],
  "women-18_99":  random_list[300:400]
})

# Extract var names
vars = list(df.columns[1:len(df.columns)])
# Split var name string  to get groups
groups = [re.sub("^(.+)\-(.+)$", "\\1", v) for v in vars]

# Pivot and keep age values in columns
pd.wide_to_long(
  df, stubnames = list(set(groups)), i = 'id', j = 'age',
  sep='-', suffix='.+'
)

# Pivot to get gender and age as separate columns
(pd.wide_to_long(
  df, stubnames = list(set(groups)), i = 'id', j = 'age',
  sep='-', suffix='.+'
)
.stack()
.reset_index(name='num')
.rename(columns={'index':'cat', 'level_2':'gender'})
#.astype({'i':int, 'u':int})
#.sort_values(['u','i','cat'])
)