import radvel
import paths_and_files as pf
import pandas as pd
import numpy as np

redmine_id = 2908
starname = 'ID2908'
nplanets = 3
instnames = ['foces']
ntels = 1
fitting_basis = 'per tc e w k'
bjd0 = 0
planet_letters = {}
for n in range(nplanets):
    planet_letters.update({n + 1: chr(98 + n)})
anybasis_params = radvel.Parameters(nplanets, basis='per tc e w k', planet_letters=planet_letters)
lit_params = []
with open(pf.lit_planet_params.format(redmine_id)) as paramfile:
    for line in paramfile:
        line = line.strip()
        line = line.split()
        for entry in range(len(line)):
            line[entry] = float(line[entry])
        lit_params.append(line)
for n in range(nplanets):
    anybasis_params['per{}'.format(str(n+1))] = radvel.Parameter(value=float(lit_params[n][0]))
    anybasis_params['tc{}'.format(str(n+1))] = radvel.Parameter(value=lit_params[n][1])
    anybasis_params['e{}'.format(str(n+1))] = radvel.Parameter(value=lit_params[n][2])
    anybasis_params['w{}'.format(str(n+1))] = radvel.Parameter(value=(2.0 * np.pi * lit_params[n][3] / 360.0))
    anybasis_params['k{}'.format(str(n+1))] = radvel.Parameter(value=lit_params[n][4])
time_base = 2456778
anybasis_params['dvdt'] = radvel.Parameter(value=0.0)
anybasis_params['curv'] = radvel.Parameter(value=0.0)
for inst in instnames:
    anybasis_params['gamma_{}'.format(inst)] = radvel.Parameter(value=0.0)
    anybasis_params['jit_{}'.format(inst)] = radvel.Parameter(value=2.6)
params = anybasis_params.basis.to_any_basis(anybasis_params, fitting_basis)
params['dvdt'].vary = False
params['curv'].vary = False
for n in range(nplanets):
    params['per{}'.format(str(n+1))].vary = False
    params['tc{}'.format(str(n+1))].vary = True
    params['e{}'.format(str(n+1))].vary = False
    params['w{}'.format(str(n+1))].vary = True
    params['k{}'.format(str(n+1))].vary = False
data = pd.read_csv(pf.out_RVs_compare.format(redmine_id), sep=' ')
priors = [
    radvel.prior.EccentricityPrior(nplanets),
    radvel.prior.Gaussian('tc1', params['tc1'].value, 300.0)
]
for inst in instnames:
    priors.append(radvel.prior.HardBounds('jit_{}'.format(inst), 0.0, 10.0))
stellar = dict(mstar=1.12, mstar_err=0.06)
