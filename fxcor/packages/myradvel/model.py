import numpy as np
from collections import OrderedDict

from radvel import kepler
from radvel.basis import Basis


texdict = {
    'per': 'P',
    'logper': '\\ln{P}',
    'logk': '\\ln{K}',
    'tc': 'T\\rm{conj}',
    'secosw': '\\sqrt{e}\\cos{\\omega}',
    'sesinw': '\\sqrt{e}\\sin{\\omega}',
    'ecosw': 'e\\cos{\\omega}',
    'esinw': 'e\\sin{\\omega}',
    'e': 'e',
    'w': '\\omega',
    'tp': 'T\\rm{peri}',
    'k': 'K',
    'gamma_': '\\gamma_{\\rm ',
    'logjit_': '\\ln{\\sigma_{\\rm jit}}_{\\rm ',
    'jit_': '\\sigma_{\\rm ',
    'dvdt': '\\dot{\\gamma}',
    'curv': '\\ddot{\\gamma}',
    'gp_amp': '\\eta_{1}',
    'gp_explength': '\\eta_{2}',
    'gp_per': '\\eta_{3}',
    'gp_perlength': '\\eta_{4}',
    'gp_length':'\\eta_{2}',
    'gp_B': 'B',
    'gp_C': 'C',
    'gp_L': 'L',
    'gp_Prot': 'P_{\\rm rot}',
}

class Parameter(object):
    """Object to store attributes of each orbital parameter

    Attributes:
        value (float): value of parameter.
        vary (Bool): True if parameter is allowed to vary in
            MCMC or max likelihood fits, false if fixed
        mcmcscale (float): step size to be used for MCMC fitting
        linear (bool): if vary=False and linear=True for gamma parameters then they will be calculated analytically
            using the `trick <http://cadence.caltech.edu/~bfulton/share/Marginalizing_the_likelihood.pdf>`_. derived by Timothy Brandt.
    """

    def __init__(self, value=None, vary=True, mcmcscale=None, linear=False):
        self.value = value
        self.vary = vary
        self.mcmcscale = mcmcscale
        self.linear = linear

    def _equals(self, other):
        """method to assess the equivalence of two Parameter objects"""
        if isinstance(other, self.__class__):
            return (self.value == other.value) \
                   and (self.vary == other.vary) \
                   and (self.mcmcscale == other.mcmcscale)

    def __repr__(self):
        s = (
            "Parameter object: value = {}, vary = {}, mcmc scale = {}"
        ).format(self.value, self.vary, self.mcmcscale)
        return s

    def __float__(self):
        return self.value


class Parameters(OrderedDict):

    """Object to store the model parameters.

    Parameters to describe a radial velocity orbit
    stored as an OrderedDict.

    Args:
        num_planets (int): Number of planets in model
        basis (string): parameterization of orbital parameters. See
            ``radvel.basis.Basis`` for a list of valid basis strings.
        planet_letters (dict [optional): custom map to match the planet
            numbers in the Parameter object to planet letters.
            Default {1: 'b', 2: 'c', etc.}. The keys of this dictionary must
            all be integers.

    Attributes:
        basis (radvel.Basis): Basis object
        planet_parameters (list): orbital parameters contained within the
            specified basis
        num_planets (int): number of planets in the model

    Examples:
       >>> import radvel
       # create a Parameters object for a 2-planet system with
       # custom planet number to letter mapping
       >>> params = radvel.Parameters(2, planet_letters={1:'d', 2:'e'})

    """
    def __init__(self, num_planets, basis='per tc secosw sesinw logk',
                 planet_letters=None):
        super(Parameters, self).__init__()

        basis = Basis(basis,num_planets)
        self.planet_parameters = basis.name.split()

        for num_planet in range(1,1+num_planets):
            for parameter in self.planet_parameters:
                new_name = self._sparameter(parameter, num_planet)
                self.__setitem__(new_name, Parameter())

        if planet_letters is not None:
            for k in planet_letters.keys():
                assert isinstance(k, int), """\
Parameters: ERROR: The planet_letters dictionary \
should have only integers as keys."""

        self.basis = basis
        self.num_planets = num_planets
        self.planet_letters = planet_letters

    def __reduce__(self):

        red = (self.__class__, (self.num_planets,
                                self.basis.name,
                                self.planet_letters),
                                None,None,iter(self.items()))
        return red

    def tex_labels(self, param_list=None):
        """Map Parameters keys to pretty TeX code representations.

        Args:
            param_list (list [optional]): Manually pass a list of parameter labels

        Returns:
            dict: dictionary mapping Parameters keys to TeX code

        """

        if param_list is None:
            param_list = self.keys()

        tex_labels = {}
        for k in param_list:
            n = k[-1]
            p = k[:-1]
            if n.isdigit() and (not 'gamma' in p and not 'jit' in p):
                tex_labels[k] = self._planet_texlabel(p, n)
            elif k in texdict.keys():
                tex_labels[k] = "$%s$" % texdict[k]
            elif p not in self.planet_parameters:
                for tex in texdict.keys():
                    if tex in k and len(tex) > 1:
                        tex_labels[k] = "$%s}$" % k.replace(tex, texdict[tex])
                        if k.startswith('gp_'):
                            tex_labels[k] = tex_labels[k].replace("}_", ", \\rm ")

            if k not in tex_labels.keys():
                tex_labels[k] = k

        return tex_labels

    def _sparameter(self, parameter, num_planet):
        return '{0}{1}'.format(parameter, num_planet)

    def _planet_texlabel(self, parameter, num_planet):
        pname = texdict.get(parameter, parameter)
        if self.planet_letters is not None:
            lett_planet = self.planet_letters[int(num_planet)]
        else:
            lett_planet = chr(int(num_planet)+97)
        return '$%s_{%s}$' % (pname, lett_planet)


if __name__ == "__main__":
    a = Parameter(value=1.3)
    a.mcmcscale = 100.
    print(a)

class GeneralRVModel(object):
    """
    A generalized RV Model

    Args:
        params (radvel.Parameters): The parameters upon which the RV model depends.
        forward_model (callable): 
            The function that defines the signal as a function of time and parameters.
            The forward model is called as
            
                ``forward_model(time, params, *args, **kwargs) -> float``
        time_base (float): time relative to which 'dvdt' and 'curv' terms are computed.
    Examples:
        >>> import radvel
        #  In this example, we'll assume a function called 'my_rv_function' that
        #  computes RV values has been defined elsewhere. We'll assume that 
        #  'my_rv_function' depends on planets' usual RV parameters
        #  contained in radvel.Parameters as well as some additional
        #  parameter, 'my_param'.
        >>> params = radvel.Parameters(2)
        >>> params['my_param'] = rv.Parameter(my_param_value,vary=True)
        >>> rvmodel = radvel.GeneralRVModel(myparams,my_rv_function)
        >>> rv = rvmodel(10)
    """
    def __init__(self,params,forward_model,time_base=0):
        self.params = params
        self.time_base = time_base
        self._forward_model = forward_model
        assert callable(forward_model)
        if 'dvdt' not in params.keys():
            self.params['dvdt'] = Parameter(value=0.)
        if 'curv' not in params.keys():
            self.params['curv'] = Parameter(value=0.)
    def __call__(self,t,*args,**kwargs):
        """Compute the radial velocity.

        Includes all Keplerians and additional trends.

        Args:
            t (array of floats): Timestamps to calculate the RV model
            planet_num (int [optional]): calculate the RV model for a single
                planet within a multi-planet system

        Returns:
            vel (array of floats): Radial velocity at each time in `t`
        """
        vel = self._forward_model(t,self.params,*args,**kwargs)
        vel += self.params['dvdt'].value * (t - self.time_base)
        vel += self.params['curv'].value * (t - self.time_base)**2
        return vel

def _standard_rv_calc(t,params,planet_num=None):
        vel = np.zeros(len(t))
        params_synth = params.basis.to_synth(params)
        if planet_num is None:
            planets = range(1, params.num_planets+1)
        else:
            planets = [planet_num]

        for num_planet in planets:
            per = params_synth['per{}'.format(num_planet)].value
            tp = params_synth['tp{}'.format(num_planet)].value
            e = params_synth['e{}'.format(num_planet)].value
            w = params_synth['w{}'.format(num_planet)].value
            k = params_synth['k{}'.format(num_planet)].value
            orbel_synth = np.array([per, tp, e, w, k])
            vel += kepler.rv_drive(t, orbel_synth)
        return vel

class RVModel(GeneralRVModel):
    """
    Generic RV Model

    This class defines the methods common to all RV modeling
    classes. The different RV models, with different
    parameterizations, all inherit from this class.
    """
    def __init__(self,params, time_base=0):
        super(RVModel,self).__init__(params,_standard_rv_calc,time_base)
        self.num_planets=params.num_planets
