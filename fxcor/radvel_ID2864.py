# Keplerian fit configuration file

# Required packages for setup
import os
import pandas as pd
import numpy as np
# radvel is available via Ubuntu, but not in the Windows anaconda environments
import radvel
import paths_and_files as pf


def make_radvel_fit(redmine_id, n_cand, inst_list):
    # Define global planetary system and dataset parameters
    starname = 'ID{}'.format(redmine_id)  # '51Peg'
    nplanets = int(n_cand)  # 1    # number of planets in the system
    instnames = list(inst_list)  # ['foces', 'lick', 'elodie']    # list of instrument names. Can be whatever you like (no spaces) but should match 'tel' column in the input file.
    ntels = len(instnames)       # number of instruments with unique velocity zero-points
    fitting_basis = 'per tc e w k'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
    bjd0 = 0   # reference epoch for RV timestamps (i.e. this number has been subtracted off your timestamps)
    planet_letters = {}  # map the numbers in the Parameters keys to planet letters (for plotting and tables)
    for n in range(nplanets):
        planet_letters.update({n + 1: chr(98 + n)})

    # Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
    anybasis_params = radvel.Parameters(nplanets, basis='per tc e w k', planet_letters=planet_letters)    # initialize Parameters object

    lit_params = []
    with open(pf.lit_planet_params.format(redmine_id)) as paramfile:
        for line in paramfile:
            line = line.strip()
            line = line.split()
            for entry in range(len(line)):
                line[entry] = float(line[entry])
            lit_params.append(line)
    for n in range(nplanets):
        anybasis_params['per{}'.format(str(n+1))] = radvel.Parameter(value=float(lit_params[n][0]))  # period of 1st planet
        anybasis_params['tc{}'.format(str(n+1))] = radvel.Parameter(value=lit_params[n][1])  # time of inferior conjunction of 1st planet
        anybasis_params['e{}'.format(str(n+1))] = radvel.Parameter(value=lit_params[n][2])  # eccentricity of 1st planet
        anybasis_params['w{}'.format(str(n+1))] = radvel.Parameter(
            value=(2.0 * np.pi * lit_params[n][3] / 360.0))  # argument of periastron of the star's orbit for 1st planet
        anybasis_params['k{}'.format(str(n+1))] = radvel.Parameter(value=lit_params[n][4])  # velocity semi-amplitude for 1st planet

##############################

    time_base = 2456778          # abscissa for slope and curvature terms (should be near mid-point of time baseline)
    anybasis_params['dvdt'] = radvel.Parameter(value=0.0)         # slope: (If rv is m/s and time is days then [dvdt] is m/s/day)
    anybasis_params['curv'] = radvel.Parameter(value=0.0)        # curvature: (If rv is m/s and time is days then [curv] is m/s/day^2)

    # analytically calculate gamma if vary=False and linear=True
    for inst in instnames:
        anybasis_params['gamma_{}'.format(inst)] = radvel.Parameter(value=0.0)  # velocity zero-point for each instrument
        anybasis_params['jit_{}'.format(inst)] = radvel.Parameter(value=2.6)  # jitter for each instrument

    # Convert input orbital parameters into the fitting basis
    params = anybasis_params.basis.to_any_basis(anybasis_params, fitting_basis)

    # Set the 'vary' attributes of each of the parameters in the fitting basis. A parameter's 'vary' attribute should
    # be set to False if you wish to hold it fixed during the fitting process. By default, all 'vary' parameters
    # are set to True.
    params['dvdt'].vary = False
    params['curv'].vary = False
    params['per1'].vary = False
    params['tc1'].vary = True
    params['e1'].vary = False
    params['w1'].vary = False
    params['k1'].vary = False

    # Load radial velocity data, in this example the data is contained in
    # an ASCII file, must have 'time', 'mnvel', 'errvel', and 'tel' keys
    # the velocities are expected to be in m/s
    data = pd.read_csv(pf.out_RVs_compare.format('2864'), sep=' ')

    # Define prior shapes and widths here.
    priors = [
        radvel.prior.EccentricityPrior( nplanets ),           # Keeps eccentricity < 1
        radvel.prior.Gaussian('tc1', params['tc1'].value, 300.0),    # Gaussian prior on tc1 with center at tc1 and width 300 days
        radvel.prior.HardBounds('jit_foces', 0.0, 10.0),
        radvel.prior.HardBounds('jit_lick', 0.0, 10.0),
        radvel.prior.HardBounds('jit_elodie', 0.0, 10.0)
    ]

    # optional argument that can contain stellar mass in solar units (mstar) and
    # uncertainty (mstar_err). If not set, mstar will be set to nan.
    stellar = dict(mstar=1.12, mstar_err=0.06)

    return


make_radvel_fit(2864, 3, ['foces', 'lick', 'elodie'])