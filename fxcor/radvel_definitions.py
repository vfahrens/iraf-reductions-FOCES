import numpy as np
import matplotlib
# matplotlib.use('agg')
from matplotlib import pyplot as pl
# from matplotlib.cm import nipy_spectral
from matplotlib import rcParams
from matplotlib.offsetbox import AnchoredText
import os
import sys
from decimal import Decimal
from contextlib import contextmanager
import warnings
from datetime import datetime, timedelta
from astropy import constants as c
from astropy import units as u
from scipy.optimize import root

import radvel_basis
import radvel_model
import radvel_likelihood
import radvel_posterior

# Normalization.
# RV m/s of a 1.0 Jupiter mass planet tugging on a 1.0
# solar mass star on a 1.0 year orbital period
K_0 = 28.4329

latex = {
    'ms': r'm s$^{\mathregular{-1}}$',
    'BJDTDB': r'BJD$_{\mathregular{TDB}}$'
}

telfmts_default = {
    'j': dict(color='k', marker=u'o', label='HIRES', mew=1),
    'k': dict(color='k', fmt='s', mfc='none', label='HIRES pre 2004', mew=1),
    'a': dict(color='g', fmt='d', label='APF'),
    'pfs': dict(color='magenta', fmt='p', label='PFS'),
    'h': dict(color='firebrick', fmt="s", label='HARPS'),
    'harps-n': dict(color='firebrick', fmt='^', label='HARPS-N'),
    'l': dict(color='g', fmt='*', label='LICK'),
}
telfmts_default['lick'] = telfmts_default['l']
telfmts_default['hires_rj'] = telfmts_default['j']
telfmts_default['hires'] = telfmts_default['j']
telfmts_default['hires_rk'] = telfmts_default['k']
telfmts_default['apf'] = telfmts_default['a']
telfmts_default['harps'] = telfmts_default['h']
telfmts_default['LICK'] = telfmts_default['l']
telfmts_default['HIRES_RJ'] = telfmts_default['j']
telfmts_default['HIRES'] = telfmts_default['j']
telfmts_default['HIRES_RK'] = telfmts_default['k']
telfmts_default['APF'] = telfmts_default['a']
telfmts_default['HARPS'] = telfmts_default['h']
telfmts_default['HARPS-N'] = telfmts_default['harps-n']
telfmts_default['PFS'] = telfmts_default['pfs']

# cmap = nipy_spectral
rcParams['font.size'] = 9
rcParams['lines.markersize'] = 5
rcParams['axes.grid'] = False
default_colors = ['orange', 'purple', 'magenta', 'pink', 'green', 'grey', 'red', 'blue', 'yellow']

highlight_format = dict(marker='o', ms=16, mfc='none', mew=2, mec='gold', zorder=99)


def telplot(x, y, e, tel, ax, lw=1., telfmt={}, rms=0):
    """Plot data from from a single telescope

    x (array): Either time or phase
    y (array): RV
    e (array): RV error
    tel (string): telecsope string key
    ax (matplotlib.axes.Axes): current Axes object
    lw (float): line-width for error bars
    telfmt (dict): dictionary corresponding to kwargs
        passed to errorbar. Example:

        telfmt = dict(fmt='o',label='HIRES',color='red')
    """

    # Default formatting
    kw = dict(
        fmt='o', capsize=0, mew=0,
        ecolor='0.6', lw=lw, color='orange',
    )

    # If not explicit format set, look among default formats
    if not telfmt and tel in telfmts_default:
        telfmt = telfmts_default[tel]

    for k in telfmt:
        kw[k] = telfmt[k]

    if not 'label' in kw.keys():
        if tel in telfmts_default:
            kw['label'] = telfmts_default[tel]['label']
        else:
            kw['label'] = tel

    if rms:
        kw['label'] += '\nRMS={:.2f} {:s}'.format(rms, latex['ms'])

    pl.errorbar(x, y, yerr=e, **kw)


def mtelplot(x, y, e, tel, ax, lw=1., telfmts={}, **kwargs):
    """
    Overplot data from from multiple telescopes.

    x (array): Either time or phase
    y (array): RV
    e (array): RV error
    tel (array): array of telecsope string keys
    ax (matplotlib.axes.Axes): current Axes object
    telfmts (dict): dictionary of dictionaries corresponding to kwargs
        passed to errorbar. Example:

        telfmts = {
             'hires': dict(fmt='o',label='HIRES'),
             'harps-n' dict(fmt='s')
        }
    """

    rms_values = kwargs.pop('rms_values', False)

    utel = np.unique(tel)

    ci = 0
    for t in utel:
        xt = x[tel == t]
        yt = y[tel == t]
        et = e[tel == t]

        telfmt = {}

        if t in telfmts:
            telfmt = telfmts[t]
            if 'color' not in telfmt:
                telfmt['color'] = default_colors[ci]
                ci += 1
        elif t not in telfmts and t not in telfmts_default:
            telfmt = dict(color=default_colors[ci])
            ci += 1
        else:
            telfmt = {}

        if rms_values:
            rms = rms_values[t]
        else:
            rms = 0

        telplot(xt, yt, et, t, ax, lw=1., telfmt=telfmt, rms=rms)

    ax.yaxis.set_major_formatter(
        matplotlib.ticker.ScalarFormatter(useOffset=False)
    )
    ax.xaxis.set_major_formatter(
        matplotlib.ticker.ScalarFormatter(useOffset=False)
    )


def add_anchored(*args, **kwargs):
    """
    Add text at a particular location in the current Axes

    Args:
        s (string): text
        loc (string): location code
        pad (float [optional]): pad between the text and the frame
            as fraction of the font size
        borderpad (float [optional]): pad between the frame and the axes (or *bbox_to_anchor*)
        prop (matplotlib.font_manager.FontProperties): font properties
    """

    bbox = {}
    if 'bbox' in kwargs:
        bbox = kwargs.pop('bbox')
    at = AnchoredText(*args, **kwargs)
    if len(bbox.keys()) > 0:
        pl.setp(at.patch, **bbox)

    ax = pl.gca()
    ax.add_artist(at)


def labelfig(letter):
    """
    Add a letter in the top left corner in the current Axes

    Args:
        letter (int): integer representation of letter to be printed.
            Ex: ord("a") gives 97, so the input should be 97.
    """
    text = "{})".format(chr(letter))
    add_anchored(
        text, loc=2, prop=dict(fontweight='bold', size='large'),
        frameon=False
    )


def load_module_from_file(module_name, module_path):
    """Loads a python module from the path of the corresponding file.

    Args:
        module_name (str): namespace where the python module will be loaded,
            e.g. ``foo.bar``
        module_path (str): path of the python file containing the module
    Returns:
        A valid module object
    Raises:
        ImportError: when the module can't be loaded
        FileNotFoundError: when module_path doesn't exist
    """
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    elif sys.version_info[0] == 3 and sys.version_info[1] < 5:
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader(module_name, module_path)
        module = loader.load_module()
    elif sys.version_info[0] == 2:
        import imp
        module = imp.load_source(module_name, module_path)

    return module


def initialize_posterior(config_file, decorr=False):
    """Initialize Posterior object

    Parse a setup file and initialize the RVModel, Likelihood, Posterior and priors.

    Args:
        config_file (string): path to config file
        decorr (bool): (optional) decorrelate RVs against columns defined in the decorr_vars list

    Returns:
        tuple: (object representation of config file, radvel.Posterior object)
    """

    system_name = os.path.basename(config_file).split('.')[0]
    P = load_module_from_file(system_name, os.path.abspath(config_file))

    params = P.params
    assert str(params.basis) == "Basis Object <{}>".format(P.fitting_basis), """
Parameters in config file must be converted to fitting basis.
"""

    if decorr:
        try:
            decorr_vars = P.decorr_vars
        except:
            raise Exception("--decorr option selected,\
 but decorr_vars is not found in your setup file.")
    else:
        decorr_vars = []

    for key in params.keys():
        if key.startswith('logjit'):
            msg = """
Fitting log(jitter) is depreciated. Please convert your config
files to initialize 'jit' instead of 'logjit' parameters.
Converting 'logjit' to 'jit' for you now.
"""
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            newkey = key.replace('logjit', 'jit')
            params[newkey] = radvel_model.Parameter(value=np.exp(params[key].value), vary=params[key].vary)
            del params[key]

    iparams = radvel_basis._copy_params(params)

    # Make sure we don't have duplicate indicies in the DataFrame
    P.data = P.data.reset_index(drop=True)

    # initialize RVmodel object
    mod = radvel_model.RVModel(params, time_base=P.time_base)

    # initialize Likelihood objects for each instrument
    telgrps = P.data.groupby('tel').groups
    likes = {}
    for inst in P.instnames:
        assert inst in P.data.groupby('tel').groups.keys(), \
            "No data found for instrument '{}'.\nInstruments found in this dataset: {}".format(inst,
                                                                                               list(telgrps.keys()))
        decorr_vectors = {}
        if decorr:
            for d in decorr_vars:
                decorr_vectors[d] = P.data.iloc[telgrps[inst]][d].values

        try:
            hnames = P.hnames[inst]
            liketype = radvel_likelihood.GPLikelihood
            try:
                kernel_name = P.kernel_name[inst]
                # if kernel_name == "Celerite":
                #     liketype = radvel_likelihood.CeleriteLikelihood
                if kernel_name == "Celerite":
                    liketype = radvel_likelihood.CeleriteLikelihood
            except AttributeError:
                kernel_name = "QuasiPer"
        except AttributeError:
            liketype = radvel_likelihood.RVLikelihood
            kernel_name = None
            hnames = None
        likes[inst] = liketype(
            mod, P.data.iloc[telgrps[inst]].time,
            P.data.iloc[telgrps[inst]].mnvel,
            P.data.iloc[telgrps[inst]].errvel, hnames=hnames, suffix='_' + inst,
            kernel_name=kernel_name, decorr_vars=decorr_vars,
            decorr_vectors=decorr_vectors
        )
        likes[inst].params['gamma_' + inst] = iparams['gamma_' + inst]
        likes[inst].params['jit_' + inst] = iparams['jit_' + inst]

    like = radvel_likelihood.CompositeLikelihood(list(likes.values()))

    # Initialize Posterior object
    post = radvel_posterior.Posterior(like)
    post.priors = P.priors

    return P, post


def round_sig(x, sig=2):
    """Round by significant figures
    Args:
        x (float): number to be rounded
        sig (int): (optional) number of significant figures to retain
    Returns:
        float: x rounded to sig significant figures
    """

    if x == 0:
        return 0.0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)


def sigfig(med, errlow, errhigh=None):
    """
    Format values with errors into an equal number of signficant figures.

    Args:
        med (float): median value
        errlow (float): lower errorbar
        errhigh (float): upper errorbar

    Returns:
        tuple: (med,errlow,errhigh) rounded to the lowest number of significant figures

    """

    if errhigh is None:
        errhigh = errlow

    ndec = Decimal(str(errlow)).as_tuple().exponent
    if abs(Decimal(str(errhigh)).as_tuple().exponent) > abs(ndec):
        ndec = Decimal(str(errhigh)).as_tuple().exponent
    if ndec < -1:
        tmpmed = round(med, abs(ndec))
        p = 0
        if med != 0:
            while tmpmed == 0:
                tmpmed = round(med, abs(ndec) + p)
                p += 1
            med = tmpmed
    elif (ndec == -1 and str(errhigh)[-1] == '0') and (ndec == -1 and str(errlow)[-1] == '0') or ndec == 0:
        errlow = int(round_sig(errlow))
        errhigh = int(round(errhigh))
        med = int(round(med))
    else:
        med = round(med, abs(ndec))

    return med, errlow, errhigh


def time_print(tdiff):
    """Print time

    Helper function to print time remaining in sensible units.

    Args:
        tdiff (float): time in seconds

    Returns:
        tuple: (float time, string units)
    """
    units = 'seconds'
    if tdiff > 60:
        tdiff /= 60
        units = 'minutes'
        if tdiff > 60:
            tdiff /= 60
            units = 'hours'
            if tdiff > 24:
                tdiff /= 24
                units = 'days'
    return tdiff, units


def timebin(time, meas, meas_err, binsize):
    """Bin in equal sized time bins

    This routine bins a set of times, measurements, and measurement errors
    into time bins.  All inputs and outputs should be floats or double.
    binsize should have the same units as the time array.
    (from Andrew Howard, ported to Python by BJ Fulton)

    Args:
        time (array): array of times
        meas (array): array of measurements to be comined
        meas_err (array): array of measurement uncertainties
        binsize (float): width of bins in same units as time array

    Returns:
        tuple: (bin centers, binned measurements, binned uncertainties)
    """

    ind_order = np.argsort(time)
    time = time[ind_order]
    meas = meas[ind_order]
    meas_err = meas_err[ind_order]
    ct = 0
    while ct < len(time):
        ind = np.where((time >= time[ct]) & (time < time[ct] + binsize))[0]
        num = len(ind)
        wt = (1. / meas_err[ind]) ** 2.  # weights based in errors
        wt = wt / np.sum(wt)  # normalized weights
        if ct == 0:
            time_out = [np.sum(wt * time[ind])]
            meas_out = [np.sum(wt * meas[ind])]
            meas_err_out = [1. / np.sqrt(np.sum(1. / (meas_err[ind]) ** 2))]
        else:
            time_out.append(np.sum(wt * time[ind]))
            meas_out.append(np.sum(wt * meas[ind]))
            meas_err_out.append(1. / np.sqrt(np.sum(1. / (meas_err[ind]) ** 2)))
        ct += num

    return time_out, meas_out, meas_err_out


def bintels(t, vel, err, telvec, binsize=1 / 2.):
    """Bin velocities by instrument

    Bin RV data with bins of with binsize in the units of t.
    Will not bin data from different telescopes together since there may
    be offsets between them.

    Args:
        t (array): array of timestamps
        vel (array): array of velocities
        err (array): array of velocity uncertainties
        telvec (array): array of strings corresponding to the instrument name for each velocity
        binsize (float): (optional) width of bin in units of t (default=1/2.)

    Returns:
        tuple: (bin centers, binned measurements, binned uncertainties, binned instrument codes)
    """

    # Bin RV data with bins of with binsize in the units of t.
    # Will not bin data from different telescopes together since there may
    # be offsets between them.

    ntels = len(np.unique(telvec))
    if ntels == 1:
        t_bin, vel_bin, err_bin = timebin(t, vel, err, binsize=binsize)
        return t_bin, vel_bin, err_bin, telvec[0:len(t_bin)]

    uniqorder = np.argsort(np.unique(telvec, return_index=1)[1])
    uniqsort = np.unique(telvec)[uniqorder]
    rvtimes = np.array([])
    rvdat = np.array([])
    rverr = np.array([])
    newtelvec = np.array([])
    for i, tel in enumerate(uniqsort):
        pos = np.where(telvec == tel)
        t_bin, vel_bin, err_bin = timebin(
            t[pos], vel[pos], err[pos], binsize=binsize
        )
        rvtimes = np.hstack((rvtimes, t_bin))
        rvdat = np.hstack((rvdat, vel_bin))
        rverr = np.hstack((rverr, err_bin))
        newtelvec = np.hstack((newtelvec, np.array([tel] * len(t_bin))))

    return rvtimes, rvdat, rverr, newtelvec


def fastbin(x, y, nbins=30):
    """Fast binning

    Fast binning function for equally spaced data

    Args:
        x (array): independent variable
        y (array): dependent variable
        nbins (int): number of bins

    Returns:
        tuple: (bin centers, binned measurements, binned uncertainties)
    """

    n, _ = np.histogram(x, bins=nbins)
    sy, _ = np.histogram(x, bins=nbins, weights=y)
    sy2, _ = np.histogram(x, bins=nbins, weights=y * y)
    bindat = sy / n
    binerr = np.sqrt(sy2 / n - bindat * bindat) / np.sqrt(n)
    bint = (_[1:] + _[:-1]) / 2.

    binN = n
    pos = binN >= 3  # 0.5 * np.mean(binN)
    bint = bint[pos]
    bindat = bindat[pos]
    binerr = binerr[pos]

    pos = bint > 0
    bint = bint[pos]
    bindat = bindat[pos]
    binerr = binerr[pos]
    return bint, bindat, binerr


def t_to_phase(params, t, num_planet, cat=False):
    """Time to phase

    Convert JD to orbital phase

    Args:
        params (radvel.params.RVParameters): RV parameters object
        t (array): JD timestamps
        num_planet (int): Which planet's ephemeris to phase fold on
        cat (bool): Concatenate/double the output phase array to extend from 0 to 2

    Returns:
        array: orbital phase at each timestamp
    """

    if ('tc%i' % num_planet) in params:
        timeparam = 'tc%i' % num_planet
    elif ('tp%i' % num_planet) in params:
        timeparam = 'tp%i' % num_planet

    P = params['per%i' % num_planet].value
    tc = params[timeparam].value
    phase = np.mod(t - tc, P)
    phase /= P
    if cat:
        phase = np.concatenate((phase, phase + 1))
    return phase


@contextmanager
def working_directory(dir):
    """Do something in a directory

    Function to use with `with` statements.

    Args:
       dir (string): name of directory to work in

    Example:
#        >>> with workdir('/temp'):
            # do something within the /temp directory
    """
    cwd = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(cwd)


def cmd_exists(cmd):
    return any(
        os.access(os.path.join(path, cmd), os.X_OK)
        for path in os.environ["PATH"].split(os.pathsep))


def date2jd(date):
    """
    Convert datetime object to JD"

    Args:
        date (datetime.datetime): date to convert
    Returns:
        float: Julian date
     """

    jd_td = date - datetime(2000, 1, 1, 12, 0, 0)
    jd = 2451545.0 + jd_td.days + jd_td.seconds / 86400.0
    return jd


def jd2date(jd):
    """
    Convert JD to datetime.datetime object

    Args:
        jd (float): Julian date
    Returns:
        datetime.datetime: calendar date
    """

    mjd = jd - 2400000.5
    td = timedelta(days=mjd)
    dt = datetime(1858, 11, 17, 0, 0, 0) + td

    return dt


def geterr(vec, angular=False):
    """
    Calculate median, 15.9, and 84.1 percentile values
    for a given vector.

    Args:
        vec (array): vector, usually an MCMC chain for one parameter
        angular (bool [optioanl]): Is this an angular parameter?
            if True vec should be in radians. This will perform
            some checks to ensure proper boundary wrapping.

    Returns:
        tuple: 50, 15.9 and 84.1 percentiles
    """

    try:
        vec = vec.values
    except AttributeError:
        pass

    if angular:
        val, edges = np.histogram(vec, bins=50)
        med = edges[np.argmax(val)]
        if med > np.radians(90):
            vec[vec < np.radians(0)] = vec[vec < np.radians(0)] + np.radians(360)
        if med <= np.radians(-90):
            vec[vec >= np.radians(0)] = vec[vec >= np.radians(0)] - np.radians(360)
        med = np.median(vec)
    else:
        med = np.median(vec)

    s = sorted(vec)
    errlow = med - s[int(0.159 * len(s))]
    errhigh = s[int(0.841 * len(s))] - med

    return med, errlow, errhigh


def semi_amplitude(Msini, P, Mtotal, e, Msini_units='jupiter'):
    """Compute Doppler semi-amplitude

    Args:
        Msini (float): mass of planet [Mjup]
        P (float): Orbital period [days]
        Mtotal (float): Mass of star + mass of planet [Msun]
        e (float): eccentricity
        Msini_units (Optional[str]): Units of Msini {'earth','jupiter'}
            default: 'jupiter'

    Returns:
        Doppler semi-amplitude [m/s]

    """

    # convert inputs to array so they work with units
    P = np.array(P)
    Msini = np.array(Msini)
    Mtotal = np.array(Mtotal)
    e = np.array(e)

    P = (P * u.d).to(u.year).value
    if Msini_units.lower() == 'jupiter':
        pass
    elif Msini_units.lower() == 'earth':
        Msini = (Msini * u.M_earth).to(u.M_jup).value
    else:
        raise Exception("Msini_units must be 'earth', or 'jupiter'")

    K = K_0 * (1 - e ** 2) ** -0.5 * Msini * P ** (-1.0 / 3.0) * Mtotal ** (-2.0 / 3.0)

    return K


def semi_major_axis(P, Mtotal):
    """Semi-major axis

    Kepler's third law

    Args:
        P (float): Orbital period [days]
        Mtotal (float): Mass [Msun]

    Returns:
        float or array: semi-major axis in AU
    """

    # convert inputs to array so they work with units
    P = np.array(P)
    Mtotal = np.array(Mtotal)

    Mtotal = Mtotal * c.M_sun.value
    P = (P * u.d).to(u.second).value
    G = c.G.value

    a = ((P ** 2) * G * Mtotal / (4 * (np.pi) ** 2)) ** (1 / 3.)
    a = a / c.au.value

    return a


def Msini(K, P, Mstar, e, Msini_units='earth'):
    """Calculate Msini

    Calculate Msini for a given K, P, stellar mass, and e

    Args:
        K (float or array: Doppler semi-amplitude [m/s]
        P (float or array): Orbital period [days]
        Mstar (float or array): Mass of star [Msun]
        e (float or array): eccentricity
        Msini_units (Optional[str]): Units of Msini {'earth','jupiter'}
            default: 'earth'

    Returns:
        float or array: Msini [units = Msini_units]

    """

    # convert inputs to array so they work with units
    P = np.array(P)
    Mstar = np.array(Mstar)
    K = np.array(K)
    e = np.array(e)
    G = c.G.value  # added gravitational constant
    Mjup = c.M_jup.value  # added Jupiter's mass
    Msun = c.M_sun.value  # added sun's mass
    Mstar = Mstar * Msun
    Mstar = np.array(Mstar)

    P_year = (P * u.d).to(u.year).value
    P = (P * u.d).to(u.second).value

    # First assume that Mp << Mstar
    Msini = K / K_0 * np.sqrt(1.0 - e ** 2.0) * (Mstar / Msun) ** (2.0 / 3.0) * P_year ** (1 / 3.0)

    # Use correct calculation if any elements are >10% of the stellar mass
    if (np.array(((Msini * u.Mjup).to(u.M_sun) / (Mstar / Msun)).value > 0.10)).any():
        warnings.warn("Mpsini << Mstar assumption broken, correcting Msini calculation.")

        a = K * (((2 * (np.pi) * G) / P) ** (-1 / 3.)) * np.sqrt(1 - (e ** 2))
        Msini = []
        if isinstance(P, float):
            n_elements = 1
        else:
            assert type(K) == type(P) == type(Mstar) == type(e), "All input data types must match."
            assert K.size == P.size == Mstar.size == e.size, "All input arrays must have the same length."
            n_elements = len(P)
        for i in range(n_elements):
            def func(x):
                try:
                    return x - a[i] * ((Mstar[i] + x) ** (2 / 3.))
                except IndexError:
                    return x - a * ((Mstar + x) ** (2 / 3.))

            sol = root(func, Mjup)
            Msini.append(sol.x[0])

        Msini = np.array(Msini)
        Msini = Msini / Mjup

    if Msini_units.lower() == 'jupiter':
        pass
    elif Msini_units.lower() == 'earth':
        Msini = (Msini * u.M_jup).to(u.M_earth).value
    else:
        raise Exception("Msini_units must be 'earth', or 'jupiter'")

    return Msini


def density(mass, radius, MR_units='earth'):
    """Compute density from mass and radius

    Args:
        mass (float): mass [MR_units]
        radius (float): radius [MR_units]
        MR_units (string): (optional) units of mass and radius. Must be 'earth', or 'jupiter' (default 'earth').

    Returns:
        float: density in g/cc
    """

    mass = np.array(mass)
    radius = np.array(radius)

    if MR_units.lower() == 'earth':
        uradius = u.R_earth
        umass = u.M_earth
    elif MR_units.lower() == 'jupiter':
        uradius = u.R_jup
        umass = u.M_jup
    else:
        raise Exception("MR_units must be 'earth', or 'jupiter'")

    vol = 4. / 3. * np.pi * (radius * uradius) ** 3
    rho = ((mass * umass / vol).to(u.g / u.cm ** 3)).value
    return rho


def draw_models_from_chain(mod, chain, t, nsamples=50):
    """Draw Models from Chain

    Given an MCMC chain of parameters, draw representative parameters
    and synthesize models.

    Args:
        mod (radvel_model.RVmodel) : RV model
        chain (DataFrame): pandas DataFrame with different values from MCMC
            chain
        t (array): time range over which to synthesize models
        nsamples (int): number of draws

    Returns:
        array: 2D array with the different models as different rows
    """

    np.random.seed(0)
    chain_samples = chain.ix[np.random.choice(chain.index, nsamples)]
    models = []
    for i in chain_samples.index:
        params = np.array(chain.ix[i, mod.vary_parameters])
        params = mod.array_to_params(params)
        models += [mod.model(params, t)]
    models = np.vstack(models)
    return models
