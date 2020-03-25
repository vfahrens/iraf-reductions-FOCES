import paths_and_files as pf

redmine_id = '2864'
nplanets = 3
lit_params = []
with open(pf.lit_planet_params.format(redmine_id)) as paramfile:
    for line in paramfile:
        line = line.strip()
        line = line.split()
        for entry in range(len(line)):
            line[entry] = float(line[entry])
        lit_params.append(line)
    print(lit_params)
for n in range(nplanets):
    print('per{}'.format(str(n + 1)), lit_params[n][0])
    print('e{}'.format(str(n + 1)), lit_params[n][2])
    print(type(lit_params[n][3]))
    # anybasis_params['per{}'.format(str(n + 1))] = radvel.Parameter(value=4.230785)  # period of 1st planet
    # anybasis_params['tc{}'.format(str(n + 1))] = radvel.Parameter(
    #     value=2450001.51)  # time of inferior conjunction of 1st planet
    # anybasis_params['e{}'.format(str(n + 1))] = radvel.Parameter(value=0.013)  # eccentricity of 1st planet
    # anybasis_params['w{}'.format(str(n + 1))] = radvel.Parameter(
    #     value=2.0 * np.pi * 58.0 / 360.0)  # argument of periastron of the star's orbit for 1st planet
    # anybasis_params['k{}'.format(str(n + 1))] = radvel.Parameter(value=55.94)  # velocity semi-amplitude for 1st planet
