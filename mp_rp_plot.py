import os
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

import seaborn as sns

from astropy.table import Table
import pyvo as vo

# Set plotting style:
sns.set_style('ticks')

def get_data(input_filename = None):

    if input_filename is None:
        # Define filename to which we'll save the NASA Exoplanet Archive data:
        data_output = 'all_small_warm_worlds_werr_'+date.today().strftime('%d-%m-%Y')+'.txt'

    else:
        data_output = input_filename

    # First, if data not already in the CWD, query data from all transiting exoplanets smaller than 4 REarth, 
    # with equilibrium temperatures smaller than 1000 K from the NASA exoplanet archive (if this is the first time 
    # this is done, this will take a sec or two):
    if not os.path.exists(data_output):

        service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

        # List of column names: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
        sql_query = "SELECT pl_name,disc_facility,tic_id,pl_rade,pl_radeerr1, pl_radeerr2,pl_bmasse,pl_bmasseerr1, pl_bmasseerr2,pl_orbper,pl_eqt,pl_dens,pl_trandep,pl_trandur,sy_jmag,sy_tmag,st_teff,st_rad "+\
                    "FROM ps "+\
                    "WHERE tran_flag=1 and pl_eqt<1000 and pl_rade<4"

        results = service.search(sql_query)

        # Save to table:
        table = results.to_table()
        table.write(data_output, format = 'ascii')

    else:

        table = Table.read(data_output, format = 'ascii')

    return table

plt.figure(figsize=(8,6))

# Planet(s) to highlight in the plot:
plt.errorbar(np.array([10.84]), np.array([3.16]), xerr = np.array([1.95]), yerr = np.array([0.11]), fmt = 'o', ms = 10, \
             mfc = 'cornflowerblue', mec = 'cornflowerblue', ecolor = 'cornflowerblue', elinewidth=1, zorder = 2)

# Get data for all planets:
table = get_data()

# Put to-be-used tables in some easy-to-write variables:
names, rplanets, mplanets = table[:]['pl_name'], table[:]['pl_rade'], table[:]['pl_bmasse']
discovery_facility = table[:]['disc_facility']
mp_errup, mp_errdown = table[:]['pl_bmasseerr1'], np.abs(table[:]['pl_bmasseerr2'])
rp_errup, rp_errdown = table[:]['pl_radeerr1'], np.abs(table[:]['pl_radeerr2'])

current_planets = []
for i in range(len(names)):

    if (type(mplanets[i]) is np.float64) and (names[i] not in current_planets):
        current_planets.append(names[i])

        plt.errorbar( np.array([mplanets[i]]), np.array([rplanets[i]]), \
                      xerr = (np.array([mp_errdown[i]]), np.array([mp_errup[i]])), \
                      yerr = (np.array([rp_errdown[i]]), np.array([rp_errup[i]])), \
                      fmt = 'o', ms = 4, color='grey', zorder = 2, alpha = 0.2, elinewidth = 1)

        plt.plot(mplanets[i], rplanets[i], 'o', ms = 7, color='grey', zorder = 2)

plt.ylim(0.3, 4.)
plt.xlim(0.5, 30.)
#plt.fill_between([270, 600], [0.9, 0.9], [4.2, 4.2], color = 'grey', zorder = 1, alpha = 0.2)
#plt.text(280, 3.8, 'Hazy zone', fontsize = 20, zorder = 1, color = 'grey')
#plt.xlim(100,850)
plt.xlabel('Planetary mass ($M_\oplus$)', fontsize = 14)
plt.ylabel('Planetary radius ($R_\oplus$)', fontsize = 14)

# Plot radius gap:
#plt.text(120, 1.78, 'Radius gap')
#plt.plot(np.array([0.5,1000]), np.array([1.7, 1.7]), 'k--', lw=1, alpha = 0.5)

# Plot models:
for (model,color,text) in [('Fe', 'grey', r'100\% Fe'), ('Earth','peru',r'100\% MgSiO$_3$'), ('RockWater', 'royalblue', '100\% H$_2$O'), \
                           ('H2', 'seagreen', r'2\% $H_2$'), ('H2-5', 'seagreen', r'5\% $H_2$')]:

    mm, rm = np.loadtxt('data/'+model+'.txt', unpack=True)
    f = interp1d(mm, rm, fill_value = 'extrapolate')

    mmodel = np.logspace(np.log10(np.min(mm)), np.log10(np.max(mm)), 10000)
    plt.plot(mmodel, gaussian_filter1d(f(mmodel),300), color = color, lw = 2, alpha = 0.7)
    #plt.plot(mmodel, f(mmodel), color = color, lw = 3)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xscale('log')

plt.savefig('mp_rp.pdf')
