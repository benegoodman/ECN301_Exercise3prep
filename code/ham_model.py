# ----------------------------------------------------------
# -- ham_model.py                                         --
# --     Reproducing Hamilton (2003) and (2009) results   --
# --     Using updated data from Fed Reserve St Louis     --
# --     Exact reproduction is not possible               --
# --                                                      --
# --     Olvar Bergland, sept 2018                        --
# ----------------------------------------------------------

import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import datetime as datetime

#
# read data from csv file
df = pd.read_csv('../data/hamilton_data.csv',header=[0],parse_dates=[0],index_col=[0])



with open('./ham_model.txt','w') as f:

    #
    # write some info
    f.write('+---------------------------------------------------------------+\n')
    f.write('| Reproducing Hamilton (2003) and (2009) results                +\n')
    f.write('| Using updated data from Fed Reserve, no exact reproduction    +\n')
    f.write('+---------------------------------------------------------------+\n')
    f.write('\n\n')



    # -----------------------------------------------------------------
    # -- Hamilton (2003) model, equation (3.8)                       --
    # -----------------------------------------------------------------

    #
    # create lagged variables
    df['djgdp1'] = df['djgdp'].shift(1)
    df['djgdp2'] = df['djgdp'].shift(2)
    df['djgdp3'] = df['djgdp'].shift(3)
    df['djgdp4'] = df['djgdp'].shift(4)
    df['jpmax1'] = df['jpmax'].shift(1)
    df['jpmax2'] = df['jpmax'].shift(2)
    df['jpmax3'] = df['jpmax'].shift(3)
    df['jpmax4'] = df['jpmax'].shift(4)

    #
    # data from same period as Hamilton
    dh = df[(df.index >= '1949.04.01') & (df.index <= '2001.07.01')].copy()

    f.write('Estimation period: %s-%s\n\n' % (dh.index[ 0].strftime('%Y-%m-%d'),
                                              dh.index[-1].strftime('%Y-%m-%d')))

    #
    # estimate Hamilton AR(4) model
    hmod = smf.ols('djgdp ~ djgdp1 + djgdp2 + djgdp3 + djgdp4 + jpmax1 + jpmax2 + jpmax3 + jpmax4',
                   data=dh).fit()
    f.write(hmod.summary().as_text())
    f.write('\n\n')


    #
    # estimate plain AR(4) model
    ar4m = smf.ols('djgdp ~ djgdp1 + djgdp2 + djgdp3 + djgdp4',
                   data=dh).fit()
    f.write(ar4m.summary().as_text())
    f.write('\n\n')


    # -----------------------------------------------------------------
    # -- Dynamic forecast starting 2007Q3                            --
    # -----------------------------------------------------------------

    sdate = datetime.datetime.strptime('2007-10-01', '%Y-%m-%d')

    #
    # Forecast with AR(4) model
    #

    #
    # keep forecast here
    ghat4 = np.zeros(len(df))
    dghat = np.zeros(len(df))

    #
    # loop over observations
    i = 0
    for t, v in df.iterrows():
        if t < sdate:
            ghat4[i] = v['jgdp' ]
            dghat[i] = v['djgdp']
        else:
            dghat[i] = (ar4m.params[0] +
                        ar4m.params[1]*dghat[i-1] +
                        ar4m.params[2]*dghat[i-2] +
                        ar4m.params[3]*dghat[i-3] +
                        ar4m.params[4]*dghat[i-4])
            ghat4[i] = ghat4[i-1] + dghat[i]

        i += 1

    #
    # keep prediction
    df['ghat4'] = ghat4


    #
    # Forecast with Hamilton's model
    #

    #
    # keep forecast here
    jghat = np.zeros(len(df))
    dghat = np.zeros(len(df))

    #
    # loop over observations
    i = 0
    for t, v in df.iterrows():
        if t < sdate:
            jghat[i] = v['jgdp']
            dghat[i] = v['djgdp']
        else:
            dghat[i] = (hmod.params[0] +
                        hmod.params[1]*dghat[i-1] +
                        hmod.params[2]*dghat[i-2] +
                        hmod.params[3]*dghat[i-3] +
                        hmod.params[4]*dghat[i-4] +
                        hmod.params[5]*v['jpmax1'] +
                        hmod.params[6]*v['jpmax2'] +
                        hmod.params[7]*v['jpmax3'] +
                        hmod.params[8]*v['jpmax4'])
            jghat[i] = jghat[i-1] + dghat[i]

        i += 1

    #
    # keep prediction
    df['jghat'] = jghat


    # -----------------------------------------------------------------
    # -- Plot actual GDP and forecast GDP                            --
    # -----------------------------------------------------------------

    #
    # only plot a short time period
    dp = df[(df.index >= '2007.01.01') & (df.index <= '2010.01.01')]

    fig, ax = plt.subplots(figsize=(9,6))
    fig.suptitle('Predicted Real US GDP')
    ax.plot(dp['jgdp' ],c='b',label='Observed GDP')
    ax.plot(dp['jghat'],c='r',label='Dynamic conditional forecast')
    ax.plot(dp['ghat4'],c='g',label='Dynamic AR(4) forecast')
    ax.set_ylabel('Log of Real GDP')
    ax.set_xlabel('Time')
    ax.set_ylim([960,978])
    ax.legend(loc='upper left')
    ax.grid()
    fig.tight_layout()
    fig.savefig('../figs/hamilton_fcast.png')
    plt.close()


    # -----------------------------------------------------------------
    # -- Print observed and forecasted values                        --
    # -----------------------------------------------------------------

    f.write('\n')
    f.write('   Date Observed Cond fc  Dynami fc\n')
    f.write('-----------------------------------\n')
    for t, v in dp.iterrows():
        f.write('%12s %12.2f %12.2f %12.2f\n' %
                (t.strftime('%Y-%m-%d'), v['jgdp'], v['jghat'], v['ghat4']))

