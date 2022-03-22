"""

fix_data.py

Reads original raw data from CSV file and
prepares data for use in the Hamilton model.


Olvar Bergland, NMBU, May 2020

"""

#
# import libraries
#

import pandas as pd
import numpy  as np
import datetime
import sys

#
# GDP data
# ----------------------

#
# read csv file
dgdp = pd.read_csv('../data_raw/GDPC1.csv', header=0, parse_dates=[0])

#
# rename variables
dgdp = dgdp.rename(columns={'GDPC1': 'gdp'})

#
# quarterly data
dgdp['date'] = dgdp['DATE'].dt.to_period('Q')
dgdp = dgdp.drop(columns=['DATE'])

#
# create index and sort
dgdp = dgdp.set_index('date').sort_index()

#
# Hamilton's GDP and GDP change variables
#
dgdp[ 'jgdp'] = 100*np.log(dgdp['gdp'])
dgdp['djgdp'] = dgdp['jgdp'] - dgdp['jgdp'].shift(1)



#
# Oil price data
# ----------------------

#
# read local CSV file
#
roil = pd.read_csv('../data_raw/WPU0561.csv', header=0, parse_dates=[0])

#
# rename variables
#
roil = roil.rename(columns={'WPU0561': 'oil'})

#
# convert monthly to quarterly data
roil['date'] = roil['DATE'].dt.to_period('M')
roil = roil.drop(columns=['DATE'])
roil = roil.set_index('date').sort_index()
doil = roil.resample('Q').last()

#
# Hamilton's oil price and oil price change variables
doil[ 'joil'] = 100*np.log(doil['oil'])
doil['djoil'] = doil['joil'] - doil['joil'].shift(1)
doil['djoil'] = doil['djoil'].fillna(0)

#
# cumulative change in oil price
doil['cdop'] = doil['djoil'].cumsum()
#
# maximum oil price change last three years
doil['maxp'] = doil['cdop'].rolling(window=12,min_periods=1).max()
doil['maxp'] = doil['maxp'].fillna(0)
#
# Hamilton's oil price measure
doil['jpmax'] = doil['cdop'] - doil['maxp'].shift(1)
doil.loc[doil['jpmax'] < 0,'jpmax'] = 0


#
# merge datasets
#

df = dgdp.join(doil)

print(doil.info())
print(doil.head())

# save to new CSV file
df.to_csv('../data/hamilton_data.csv')
