import os
import numpy as np
from datetime import date
import matplotlib.pyplot as plt

import seaborn as sns

from astropy.table import Table
import pyvo as vo

# Set plotting style:
sns.set_style('ticks')

def get_data(input_filename = None):

    if input_filename is None:
        # Define filename to which we'll save the NASA Exoplanet Archive data:
        data_output = 'all_small_warm_worlds_'+date.today().strftime('%d-%m-%Y')+'.txt'

    else:
        data_output = input_filename

    # First, if data not already in the CWD, query data from all transiting exoplanets smaller than 4 REarth, 
    # with equilibrium temperatures smaller than 1000 K from the NASA exoplanet archive (if this is the first time 
    # this is done, this will take a sec or two):
    if not os.path.exists(data_output):

        service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

        # List of column names: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
        sql_query = "SELECT pl_name,disc_facility,tic_id,pl_rade,pl_bmasse,pl_orbper,pl_eqt,pl_dens,pl_trandep,pl_trandur,sy_jmag,sy_tmag,st_teff,st_rad "+\
                    "FROM ps "+\
                    "WHERE tran_flag=1 and pl_eqt<1000 and pl_rade<4"

        results = service.search(sql_query)

        # Save to table:
        table = results.to_table()
        table.write(data_output, format = 'ascii')

    else:

        table = Table.read(data_output, format = 'ascii')

    return table

def get_tsm(rp, mp, teq, rstar, J):

    idx1 = np.where(rp < 1.5)[0]
    idx2 = np.where((rp >= 1.5) & (rp < 2.75))[0]
    idx3 = np.where((rp > 2.75) & (rp < 4.0))[0]

    scale_factors = np.ones(len(rp))
    scale_factors[idx1] = 0.190
    scale_factors[idx2] = 1.26
    scale_factors[idx3] = 1.28

    return scale_factors * (((rp**3)*(teq))/(mp * (rstar**2))) * 10**(-J/5.)

plt.figure(figsize=(8,6))

# Planet(s) to highlight in the plot:
plt.text(455, 3.2, 'TOI-1759b', fontsize=11, zorder = 2)
plt.plot(443, 3.16, 'o', ms = 80.855296/8, mfc = 'cornflowerblue', mec = 'blue', zorder = 2)

# Define planets where atmospheric characterization has been already performed:
atm_characterized = ['GJ 1214 b', 'K2-18 b', 'HD 3167 c', 'HD 97658 b', 'LHS 1140 b', 'Kepler-51 b', 'Kepler-51 d', 'GJ 436 b', \
                     'GJ 3470 b', 'HAT-P-11 b', 'GJ 1132 b', 'TRAPPIST-1 d', 'TRAPPIST-1 e', 'TRAPPIST-1 f', 'TRAPPIST-1 g']

# Get data for all planets:
table = get_data()

# All right, first, plot Teq v/s Radius, along with TSM. First, compute TSM:
tsms = get_tsm(table[:]['pl_rade'], table[:]['pl_bmasse'], table[:]['pl_eqt'], table[:]['st_rad'], table[:]['sy_jmag'])

# Put to-be-used tables in some easy-to-write variables:
names, teqs, rplanets, jmags = table[:]['pl_name'], table[:]['pl_eqt'], table[:]['pl_rade'], table[:]['sy_jmag']
mplanets, rstar = table[:]['pl_bmasse'], table[:]['st_rad']
discovery_facility = table[:]['disc_facility']

# Sort by TSM:
idx = np.argsort(tsms)[::-1]

current_planets = []
for i in idx:

    if (type(tsms[i]) is np.float64) and (names[i] not in current_planets):
        current_planets.append(names[i])

        if teqs[i] < 600:
            print('** name:', names[i],'teq:', teqs[i],'jmag:', jmags[i],'rp:', rplanets[i],'tsm:', tsms[i], 'mass:', mplanets[i], 'stellar radius:', rstar[i])
        else:
            print('name:', names[i],'teq:', teqs[i],'jmag:', jmags[i],'rp:', rplanets[i],'tsm:', tsms[i], 'mass:', mplanets[i], 'stellar radius:', rstar[i])

        if names[i] in atm_characterized:
            print('^^^ atm charact')
            plt.plot(teqs[i], rplanets[i], 'o', ms = tsms[i]/8, mec = 'orangered', mfc = 'None', zorder = 2)

        else:

            plt.plot(teqs[i], rplanets[i], 'o', ms = tsms[i]/8, mfc = 'white', mec = 'black', zorder = 2, alpha = 0.1)

        if 'TESS' in discovery_facility[i]:

            plt.plot(teqs[i], rplanets[i], 'o', ms = tsms[i]/8, mfc = 'white', mec = 'black', zorder = 2, alpha = 0.5)

#plt.ylim(0.9, 4.1)
plt.ylim(0.3, 4.)
plt.fill_between([270, 600], [0.0, 0.0], [4.2, 4.2], color = 'grey', zorder = 1, alpha = 0.2)
plt.text(280, 0.5, 'Hazy zone?', fontsize = 20, zorder = 1, color = 'grey')
plt.xlim(100,850)
plt.xlabel('Equilibrium temperature (K)', fontsize = 14)
plt.ylabel('Planetary radius ($R_\oplus$)', fontsize = 14)

# Plot TSM legend:
for TSM, R in [(10, 2.9), (50, 3.3), (100, 3.7)]:

    if TSM == 10:
        plt.text(140,R+0.05, str(TSM), fontsize = 10)
    if TSM == 50:
        plt.text(141,R+0.06, str(TSM), fontsize = 10)
    if TSM == 100:
        plt.text(134,R+0.1, str(TSM), fontsize = 10)

    plt.plot(np.array([150]), np.array([R]), 'o', ms = TSM/8, mfc = 'white', mec = 'black', zorder = 3)

plt.plot(np.array([180, 180]), np.array([3.9, 2.9]), 'k-', lw=1)
plt.text(188, 2.95, 'TSM', fontsize = 12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Plot radius gap:
#plt.text(120, 1.78, 'Radius gap')
#plt.plot(np.array([0,1000]), np.array([1.7, 1.7]), 'k--', lw=1, alpha = 0.5)

plt.savefig('teq_rp.pdf')
