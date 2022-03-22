# ----------------------------------------------------------
# -- plot_data.py                                         --
# --     Create plots of Norwegian GDP data               --
# --     Olvar Bergland, sept 2018                        --
# ----------------------------------------------------------

import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt


#
# read data from csv file
df = pd.read_csv('../data/hamilton_data.csv',header=[0],parse_dates=[0],index_col=[0])


#
# plot log GDP and oil price series
fig, ax = plt.subplots(2,1,figsize=(9,6))
fig.suptitle('US Real GDP and Oil Prices')

ax[0].plot(df['jgdp'],label="Real GDP", color="red")
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Log GDP')
ax[0].legend(loc="upper left")
ax[0].grid()

ax[1].plot(df['joil'],label="Oil Price Index", color="blue")
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Log Oil Price Index')
ax[1].legend(loc="upper left")
ax[1].grid()

fig.tight_layout()
fig.savefig('../figs/hamilton_data.png')
plt.close()


#
# plot change in log GDP and oil price series
fig, ax = plt.subplots(2,1,figsize=(9,6))
fig.suptitle('US Growth in Real GDP and Oil Prices')

ax[0].plot(df['djgdp'],label="Change in Real GDP", color="red")
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Growth in GDP (%)')
ax[0].legend(loc="upper left")
ax[0].grid()

ax[1].plot(df['jpmax'],label="Oil Price Change Index", color="blue")
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Oil Price Change')
ax[1].legend(loc="upper left")
ax[1].grid()

fig.tight_layout()
fig.savefig('../figs/hamilton_change.png')
plt.close()
