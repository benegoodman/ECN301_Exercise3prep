"""

get_data.py

Retrieve US GDP and oil price data from the FRED data service.

Data used to replicate Hamilton (1992).

Note: The series used by Hamilton are discontinued.
      Newer series for the same concept retrieved here.

GDP:
     U.S. Bureau of Economic Analysis, Real Gross Domestic Product [GDPC1],
     retrieved from FRED, Federal Reserve Bank of St. Louis;
     https://fred.stlouisfed.org/series/GDPC1

     Units:  Billions of Chained 2012 Dollars, Seasonally Adjusted Annual Rate

     Frequency:  Quarterly

     BEA Account Code: A191RX


Oil Price:
     U.S. Bureau of Labor Statistics,
     Producer Price Index by Commodity for Fuels and Related Products and Power:
     Crude Petroleum (Domestic Production) [WPU0561],
     retrieved from FRED, Federal Reserve Bank of St. Louis;
     https://fred.stlouisfed.org/series/WPU0561

     Units:  Index 1982=100, Not Seasonally Adjusted

     Frequency:  Monthly


Olvar Bergland, NMBU, May 2020

"""


#
# import pandas datareader for FRED
#
import pandas as pd
import pandas_datareader as pdr
import datetime


#
# set start and end dates
#
fdate = datetime.datetime(1947, 1, 1)
ldate = datetime.date.today()


#
# GDP:  GDPC1
#

#
# get remote dataseries
#
df = pdr.get_data_fred('GDPC1',fdate,ldate)

print(df.head())

#
# save raw data to local csv file
#
df.to_csv('../data_raw/GDPC1.csv')


#
# Oil Price: WPU0561
#

#
# get remote dataseries
#
df = pdr.get_data_fred('WPU0561',fdate,ldate)

print(df.head())

#
# save raw data to local csv file
#
df.to_csv('../data_raw/WPU0561.csv')
