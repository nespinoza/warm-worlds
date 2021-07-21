Warm-worlds query to the NASA Exoplanet Archive
--------------------------

This repository stores codes to reproduce the equilibrium temperature versus radius plot (`teq_rp_plot.py`) and mass-radius diagrams (`mp_rp_plot.py`) presented in Espinoza et al. (2021). 

Both of these codes perform SQL queries to the NASA Exoplanet Archive through `pyvo`, and generate plots using a combination of `matplotlib` and `seaborn`. Mass-radius models are 
under `data` and were obtained from the paper of [Zeng et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [here](https://lweb.cfa.harvard.edu/~lzeng/planetmodels.html). 
The Transmission Spectroscopy Metric (TSM) is calculated following [Kempton et al., (2018)](https://ui.adsabs.harvard.edu/abs/2018PASP..130k4401K/abstract).

In addition, the file `warm_worlds.svg` contains the [Inkscape](https://inkscape.org/)-editable file to generate a figure exactly like the one in the paper (i.e., with text markers).

If you make use of these codes or files for your research, please cite Espinoza et al. (2021), the NASA Exoplanet Archive and credit [Zeng et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract) 
for the mass-radius models and [Kempton et al., (2018)](https://ui.adsabs.harvard.edu/abs/2018PASP..130k4401K/abstract) for the TSM. 

## Dependencies

To run the codes you need the following libraries:

- `numpy` 
- `matplotlib`
- `seaborn`
- `astropy`
- `pyvo`

All of them are pip-installable.
