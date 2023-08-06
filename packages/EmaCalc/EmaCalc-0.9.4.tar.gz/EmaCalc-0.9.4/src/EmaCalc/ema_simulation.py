"""This module defines classes and methods for simulated EMA study
with group(s) of respondents drawn at random from population(s)
with specified inter-individual distributions of all model parameters.

The simulations can generate artificial data with the same structure
as a real experiment.


*** Main Module Classes:

EmaSimPopulation: defines distribution of model parameters
    for probabilities of one or more SITUATIONS, in one or more Situation Dimensions,
    and one or more perceptual ATTRIBUTE latent-variable locations
    in ONE (sub-)population of potential participants.

EmaSimExperiment: defines a complete EMA experiment,
    generates simulated responses by participants in one or more groups,
    sampled from EmaSimPopulation instance(s).
    The EMA data layout is defined by an ema_data.EmaFrame instance,
    defining Situation dimensions and categories, and
    defining discrete ordinal response scales for each Attribute.

EmaSimSubject = superclass for subject properties

SubjectBradley: single subject with Attribute ratings determined by
    the Bradley-Terry-Luce (BTL) model, assuming standard Logistic latent variable,
    i.e., with st.dev. approx= 1.8

SubjectThurstone: single subject with Attribute ratings determined by
    the Thurstone Case V model, assuming standard Gaussian latent variable,
    i.e., with st.dev. = 1.

EmaSimGroup: container for EmaSimSubject instances
    drawn at random from an EmaSimPopulation instance.


*** Main Class Methods:

EmaSimPopulation.gen_group(...)
    draws a group of simulated participants at random from the simulated Population.

EmaSimExperiment.gen_dataset(...)
    generates am ema_data.EmaDataSet instance with simulated EMA records
    for one or more groups of simulated participants.
    All records can be saved to files using the EmaDataSet.save(...) method.

*** Usage example: See script run_sim.py

*** Version History:
* Version 0.9:
2022-03-21, adapted to use Pandas in EmaFrame and EmaDataSet

* Version 0.7.1:
2022-01-19, module function set_sim_seed to ensure reproducibility
2022-01-19, EmaSimSubject.rvs methods defined here, to ensure reproducibility
2022-01-06, EmaSimPopulation.response_width_mean to control individual decision thresholds
2022-01-05, minor cleanup EmaSimExperiment

* Version 0.5.1:
2021-11-25, allow experiment with NO Attributes

* Version 0.5:
2021-11-14, copied and modified PairedCompCalc -> EmaCalc
2021-11-16, first functional version
2021-11-21, rather extensively tested
"""
# *** store true EmaSimSubject, EmaSimPopulation properties as pd.DataFrame instances ? *****

# **** specify separate Attribute variance for each Situation dimension ????
# **** separate inter-individual attribute variance jointly for all situation_dtypes,
# **** plus variance for independent variations across situation_dtypes???

import numpy as np
import pandas as pd
import logging

from .ema_data import EmaDataSet
from .ema_base import response_thresholds, tau_inv
from . import ema_latent


RNG = np.random.default_rng()
# = default module-global random generator
# may be modified via function set_sim_seed

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # test


# ------------------ module function
def set_sim_seed(seed=None):
    """Set module-global RNG with given seed.
    To be called by user BEFORE any other work,
    to achieve reproducible results.
    :param seed: (optional) integer
    :return: None
    """
    global RNG
    RNG = np.random.default_rng(seed)
    if seed is not None:
        logger.warning(f'*** Using seed={seed} -> reproducible results.')


# --------------------------------------- subject response models
class EmaSimSubject:
    """Simulate one individual participant in an EMA data-collection experiment.
    Superclass for either SubjectBradley or SubjectThurstone
    """
    def __init__(self, sc_prob, a_theta, a_tau):  # lapse_prob=0.):
        """
        :param sc_prob: mD array with (non-normalized) conditional Situation probability
            sc_prob[k0, k1, k2,...] propto Prob (k1, k2, ...)-th situation, GIVEN k0-th Stage
            sc_prob.shape == emf.situation_shape
        :param a_theta: dict with (a_key, a_theta) elements, where
            a_key = a string identifying ONE Attribute among emf.attribute_grades.keys()
            a_theta[k0, k1, ...] = mD array with mean of latent sensory variable for Attribute a_key,
        :param a_tau: dict with (a_key, thr) elements, where
            tnr[l] = UPPER interval limit for l-th ordinal response,
            NOT INCLUDING extreme -inf, +inf limits
        """
        self.sc_prob = sc_prob
        self.a_theta = a_theta
        self.a_tau = a_tau

    def __repr__(self):
        return (f'{self.__class__.__name__}(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    def gen_ema_records(self, emf, min_ema, max_ema):
        """Generate a sequence of EMA records at random
        using response properties of self.
        :param emf: ema_data.EmaFrame instance
        :param min_ema: min random number of EMA records per Stage
        :param max_ema: max random number of EMA records per Stage
        :return: ema_df = a pd.DataFrame instance containing simulated EMA results,
            stored according to given emf.
            One column for each Situation dimension and each Attribute.
            One row for each simulated EMA record.
            Number of records randomly drawn with
            min_ema <= ema_df.shape[0] < max_ema
        """
        def situation_index(sit_p, sit_shape):
            """Generate ONE random situation index tuple, NOT including Phase index
            :param sit_p: 1D probability-mass array for all situations, EXCEPT Phase
            :param sit_shape: tuple with situation_shape EXCEPT Phase dimension
            :return: ind = index tuple; len(ind) = len(sc_shape)
             """
            sit_ind = RNG.choice(len(sit_p), p=sit_p)  # linear random index
            return np.unravel_index(sit_ind, shape=sit_shape)

        def situation_dict(sit_ind):
            """Convert index tuple to situation dict
            """
            return {sit_key: sit_dtype.categories[i]
                    for (i, (sit_key, sit_dtype)) in zip(sit_ind,
                                                         emf.situation_dtypes.items())}
        # -------------------------------------------------------

        ema_list = []
        # = list of dicts, one for each simulated EMA record
        sit_shape_phase = emf.situation_shape[1:]
        sit_prob_phase = self.sc_prob.reshape((self.sc_prob.shape[0], -1))
        for (i, p) in enumerate(sit_prob_phase):
            n_rec = RNG.integers(min_ema, max_ema)
            for _ in range(n_rec):
                sit_index = (i, *situation_index(p, sit_shape_phase))
                a_grades = self.gen_attr_grades(emf, sit_index)
                ema_list.append(situation_dict(sit_index) | a_grades)
        return pd.DataFrame.from_records(ema_list).astype(emf.dtypes)

    def gen_attr_grades(self, emf, sit_index):
        """Generate random ordinal Attribute grades in given Situation
        :param emf: external ema_data.EmaFrame object defining experimental layout
        :param sit_index: index tuple defining ONE situation for this record,
            including index in ALL situation dimensions
        :return: a_grades = dict with elements (a, grade)
        """
        def rvs_grade(th, tau):
            """Generate a random grade index for ONE attribute in ONE situation
            :param th: scalar location of latent variable in the given situation
            :param tau: 1D threshold array for this attribute,
                NOT INCLUDING extreme -inf, +inf limits
            :return: scalar integer index of given rating
            """
            x = self.rvs(th)  # done by sub-class
            return np.sum(x > tau)
        # -------------------------------------------------------
        return {a: emf.attribute_dtypes[a].categories[rvs_grade(a_th[sit_index],
                                                                self.a_tau[a])]
                for (a, a_th) in self.a_theta.items()}

    @staticmethod
    def rvs(loc, size=None):
        """Abstract method, implemented by sub-class.
        Draw random variables from self
         :param loc: scalar or array-like location
         :param size: (optional) size of result
         :return: x = scalar or array
             x.shape == loc.shape, if no size is given
         """
        raise NotImplementedError

    # def lapse(self):  # *** future ???
    #     """Generate True with prob = self.lapse_prob
    #     """
    #     return uniform.rvs(0, 1.) < self.lapse_prob
    #
    # def lapse_response(self):
    #     """Generate a random result, disregarding latent variable and threshold parameters
    #     :return: scalar integer
    #         in {-n_difference_grades, ...,-1, +1,..., + n_difference_grades}, if forced_choice
    #         in {-n_difference_grades+1, ...,0, ...,  + n_difference_grades-1}, if not forced_choice
    #         i.e., excluding 0 if self.emf.forced_choice
    #     """
    #     n_response_limits = len(self.response_thresholds)
    #     # if self.emf.forced_choice:
    #     if self.response_thresholds[0] == 0.:  # forced_choice
    #         return ((-1 if uniform.rvs() < 0.5 else +1) *
    #                 randint.rvs(low=1, high=n_response_limits + 1))
    #
    #     else:
    #         return randint.rvs(low=-n_response_limits,
    #                            high=n_response_limits + 1)
    #


class SubjectThurstone(ema_latent.Thurstone, EmaSimSubject):
    """Simulate a subject using the Thurstone Case V choice model.
    """
    @staticmethod
    def rvs(loc, size=None):
        """Draw random sample(s) from self
        :param loc: scalar or array-like location
        :param size: (optional) size of result
        :return: x = scalar or array
            x.shape == loc.shape, if no size is given
        """
        loc = np.asarray(loc)
        if size is None:
            size = loc.shape
        return loc + RNG.standard_normal(size=size)


class SubjectBradley(ema_latent.Bradley, EmaSimSubject):
    """Simulate one individual participant in a paired-comparison experiment.
    The subject responds using the Bradley-Terry-Luce choice model,
    with parameters defined in the log domain.
    """
    @staticmethod
    def rvs(loc, size=None):
        """Draw random variables from self
        :param loc: scalar or array-like location
        :param size: (optional) size of result
        :return: x = scalar or array
            x.shape == loc.shape
        """
        return RNG.logistic(loc, size=size)


# -------------------------------------------------------------------------
class EmaSimPopulation:
    """Defines a simulated population
    from which groups of random test participants can be generated
    for a simulated EMA experiment.

    The population instance defines distributions for
    one or more nominal Situation categories, and
    zero, one or more perceptual Attributes, given any Situation.

    Each Situation is a combination of one category from each Situation Dimension.
    """
    def __init__(self, emf,
                 situation_prob,
                 attribute_mean=None,
                 log_situation_std=0.,
                 attribute_std=0.,
                 response_width_mean=None,  # -> subject_class.scale
                 log_response_width_std=0.,
                 lapse_prob_range=(0., 0.),  # ******* not needed, not used ******
                 subject_class=SubjectBradley,
                 id=''):
        """
        :param emf: ema_data.EmaFrame instance defining Situations and Attributes
        :param situation_prob: array-like multi-dim, with
            situation_prob[k0, k1,...] prop.to probability of (k1, k2,...)-th situation,
            GIVEN the k0-th test phase category, even if only one phase category.
            situation_prob.shape must correspond to shape of emf.situation_dtypes.
        :param attribute_mean: (optional) dict or iterable with elements (a_key, a_mean), where
            a_key is string id of a rated perceptual attribute,
            a_mean is an mD array with
            a_mean[k0, k1, ...] = latent-variable mean for attribute a_key,
            given the (k0, k1,...)-th Situation category, i.e.,
            a_mean.shape == situation_prob.shape, for all attributes.
        :param log_situation_std: (optional) inter-individual standard deviation of
            log probabilities for each situation category.
        :param attribute_std: (optional) scalar inter-individual standard deviation of all attribute parameters
        :param response_width_mean: (optional) mean width of response intervals,
            in subject_class scale units
        :param log_response_width_std: (optional) scalar standard deviation of log(response-interval-width)
        :param lapse_prob_range: (optional) tuple (min, max) probability of random lapse response
        :param subject_class: (optional) subject probabilistic model for generating responses
        :param id: (optional) string label, used as prefix in all generated subject names
        """
        self.emf = emf  # save emf ref here, too, although same all sub-populations
        situation_prob = np.asarray(situation_prob)
        if emf.situation_shape[0] == 1 and emf.situation_shape[1:] == situation_prob.shape:
            situation_prob = situation_prob[None, ...]
        if emf.situation_shape != situation_prob.shape:
            raise RuntimeError('situation_prob.shape must agree with EmaFrame situation_dtypes')
        self.situation_prob = situation_prob
        for (i, sc_i) in enumerate(self.situation_prob):
            self.situation_prob[i] /= np.sum(sc_i)
            # = normalizes conditional probabilities, for each phase
        self.log_situation_std = log_situation_std

        if attribute_mean is None:
            attribute_mean = dict()  # NO attributes
        else:
            attribute_mean = dict(attribute_mean)
        if set(attribute_mean.keys()) != set(emf.attribute_dtypes.keys()):
            raise RuntimeError('attribute_mean must define same attributes as EmaFrame')
        for (a, a_mean) in attribute_mean.items():
            if (emf.situation_shape[0] == 1
                    and emf.situation_shape[1:] == a_mean.shape):
                attribute_mean[a] = attribute_mean[a][None, ...]
        assert all(a_mean.shape == emf.situation_shape
                   for a_mean in attribute_mean.values()), 'attribute_mean.shape must match situation_shape'
        self.attribute_mean = attribute_mean
        self.attribute_std = attribute_std
        if response_width_mean is None:
            response_width_mean = subject_class.scale
        self.response_width_mean = response_width_mean
        self.log_response_width_std = log_response_width_std
        self.lapse_prob_range = lapse_prob_range
        self.subject_class = subject_class
        self.id = id

    def __repr__(self):
        return (f'{self.__class__.__name__}(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    @property
    def n_attributes(self):
        return len(self.attribute_mean)

    def gen_group(self, n_participants=1):
        """Create a group of simulated-subject instances randomly drawn from self,
        with properties suitable for a planned experiment.
        :param n_participants: number of randomly drawn participants from self
        :return: single EmaSimGroup instance, containing generated participants,
            each with properties drawn from self.
        """
        def gen_sc_prob():
            sc_p = np.exp(np.log(self.situation_prob) +
                          self.log_situation_std *
                          RNG.standard_normal(size=self.emf.situation_shape))
            for (i, sc_i) in enumerate(sc_p):
                sc_p[i] /= np.sum(sc_i)
                # normalized conditional probabilities, for each phase
            return sc_p

        def gen_attr():
            theta = self.attribute_std * RNG.standard_normal(size=(self.n_attributes,
                                                                   *self.emf.situation_shape))
            # theta[i, ...] = random offset of location for i-th attribute of s-th subject
            return {a: th_mean + th_d
                    for ((a, th_mean), th_d) in zip(self.attribute_mean.items(),
                                                    theta)}

        def gen_tau():
            """Random threshold parameters for each attribute
            """
            def tau(n_levels):
                """Calc response thresholds
                :param n_levels: integer number of response intervals
                :return: t = 1D array with INNER interval limits, i.e.,
                    t[m] = UPPER interval limit for m-th ordinal response
                    t.shape == (n_levels - 1,)
                """
                t = self.response_width_mean * (np.arange(n_levels - 1) + 1. - n_levels / 2)
                log_w = tau_inv(t) + self.log_response_width_std * RNG.standard_normal(size=n_levels)
                # incl. random variations of log interval width in mapped [0, 1] range
                return response_thresholds(log_w)[1:-1]  # EXCL (-inf, +inf) extremes
            # ----------------------------------------------------
            scale_tau = {s_id: tau(len(scale.categories))
                         for (s_id, scale) in self.emf.ordinal_scales.items()}
            # = scale thresholds, possibly used for more than one attribute
            return {a: scale_tau[s_id]
                    for (a, s_id) in self.emf.attribute_scales.items()}
            # --------------------------------------------------------------------

        return EmaSimGroup(self,
                           {self.id + f'_S{i}': self.subject_class(sc_prob=gen_sc_prob(),
                                                                   a_theta=gen_attr(),
                                                                   a_tau=gen_tau())
                            for i in range(n_participants)})


# ----------------------------------------------------------------------
class EmaSimGroup:
    """Group of test participants drawn from a given population
    """
    def __init__(self, pop, participants):
        """
        :param pop: an EmaSimPopulation instance,
            from which participants have been drawn at random
        :param participants: dict with (s_id, s_sim)
            s_id = string id for the subject
            s_sim = an EmaSimSubject instance
        """
        self.pop = pop
        self.participants = participants

    def __repr__(self):
        # n_ema = sum(s_df.shape[0] for s_df in self.participants.values())
        return (self.__class__.__name__ + '('
                + f'\n\tpop={repr(self.pop)}'
                + f'\n\tparticipants= dict with {len(self.participants)} simulated participants)')


# -------------------------------------------------------------------------
class EmaSimExperiment:
    """Defines a simulated EMA data-collection experiment,
    with one or more groups of simulated participants, with
    each group generated from an EmaSimPopulation instance.

    Method gen_dataset() generates a complete ema_data.EmaDataSet instance
    with EMA records for all participants in all groups.

    The experimental procedure is defined by
    emf = an ema_data.EmaFrame instance
    """
    def __init__(self, emf, groups):
        """
        :param emf: EmaFrame instance, defining experimental parameters
        :param groups: dict with elements (g_id, g_sim),
            g_sim = an EmaSimGroup instance
        """
        self.emf = emf
        self.groups = groups

    def __repr__(self):
        return (f'{self.__class__.__name__}(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    def gen_dataset(self, min_ema=3, max_ema=50):
        """Generate a complete EmaDataSet instance for this experiment,
        with one or more groups of participants.
        :param min_ema: min random number of EMA records in each Stage
        :param max_ema: max random number of EMA records in each Stage
        :return: a single EmaDataSet instance
        """
        emd = {g: {s_id: s.gen_ema_records(self.emf, min_ema, max_ema)
                   for (s_id, s) in g_sim.participants.items()}
               for (g, g_sim) in self.groups.items()}
        return EmaDataSet(self.emf, emd)
