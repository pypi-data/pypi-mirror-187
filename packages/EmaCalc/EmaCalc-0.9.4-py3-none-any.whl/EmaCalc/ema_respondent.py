"""This module defines a class for individual participant parameter model
to be part of an ema_group.EmaGroupModel instance,
which is part the main Bayesian probabilistic model of EMA data.

Individual parameter distributions are approximated by sampling.
The population mixture model is common prior for all individuals in
the group recruited from the same population.

*** Class Defined here:

EmaRespondentModel: Distribution of individual parameter vector
    assumed to determine the observed EMA data from ONE respondent,
    including, in each EMA record,
    (1) a nominal (possibly multi-dimensional) Situation category, and
    (2) ordinal Ratings for zero, one, or more perceptual Attributes.
    The parameter distribution is represented by an array xi with many samples.
    The sample distribution is independent across EmaRespondentModel instances,
    so instances may be adapt-ed in parallel processes.

*** Version History:
* Version 0.9.3:
2022-07-27, changed module name ema_subject -> ema_respondent
            EmaSubjectModel -> EmaRespondentModel
2022-07-20, moved _initialize xi -> ema_base, for same reason
2022-07-19, moved logprob calc -> ema_base, to hide parameter indexing details there
2022-07-xx, minor update for notation change: scenario -> situation

* Version 0.9.2:
2022-06-15, EmaSubjectModel methods mean_attribute_grades, nap_diff deleted.
            Replaced by ema_data.EmaDataSet.(mean_attribute_table, nap_table).

2022-06-15, new _initialize_rating_eta(y); changed _initialize_rating_theta(y, eta)
            tested initial response thresholds crudely based on response counts

2022-05-21, EmaSubjectModel.cdf_arg: check for too small response interval,
            that might cause numerical underflow in case of many missing data

* Version 0.8.3:
2022-03-08, minor cleanup logging to work in multi-processing

* Version 0.8.2: prepared for multi-processing subject adapt() in parallel processes
2022-03-03, EmaSubjectModel methods mean_zeta, mean_zeta_mom no longer needed

* Version 0.8.1: minor cleanup of comments and logger output

* Version 0.8
2022-02-12, Changed VI factorization for better approximation,
    with individual indicators conditional on parameter samples,
    defining variational q(zeta_n, xi_n) = q(zeta_n | xi_n) q(xi_n)
"""
import multiprocessing
import logging

import numpy as np
from scipy.optimize import minimize

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy

from EmaCalc.ema_base import PRIOR_PARAM_SCALE


# -------------------------------------------------------------------
__ModelVersion__ = "2022-07-27"

DITHER_PARAM_SCALE = 0.1 * PRIOR_PARAM_SCALE
# -> initial dithering of point-estimated individual parameters

N_SAMPLES = 1000
# = number of parameter vector samples in each EmaRespondentModel instance

logger = logging.getLogger(__name__)
# logger does NOT inherit parent handlers, when this module is running as child process
if multiprocessing.current_process().name != "MainProcess":
    # restore a formatter like ema_logging, only for console output
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('{asctime} {name}: {message}',
                                           style='{',
                                           datefmt='%H:%M:%S'))
    logger.addHandler(console)
# Might instead send the parent logger as argument to adapt() ? ***
# logger.setLevel(logging.DEBUG)  # *** TEST
# ham.logger.setLevel(logging.DEBUG)  # *** TEST sampler


# -------------------------------------------------------------------
class EmaRespondentModel:
    """Container for EMA response-count data for ONE respondent,
    and a sampled approximation of the individual parameter distribution.

    Individual parameter distributions are approximated by a large set of samples
    stored as property xi, with
    self.xi[s, :] = s-th sample vector of parameters,
    with subsets of parameter types (alpha, beta, eta) as defined in self.base.
    """
    def __init__(self, base, situation_count, rating_count, xi, rng, prior=None, id=''):
        """
        :param base: single common ema_base.EmaParamBase object, used by all model parts
        :param situation_count: 2D array with response counts
            situation_count[k0, k] = number of responses
            in k-th <=> (k1, k2, ...)-th situation category at k0-th test phase,
            using flattened index for situation dimensions 1,2,....
            NOTE: ema_data.EmaFrame always stores test phase as first situation dimension.
        :param rating_count: list of 2D arrays with response counts
            rating_count[i][l, k] = number of responses for i-th ATTRIBUTE,
            at l-th ordinal level, given the k-th <=> (k0, k1, k2, ...)-th situation
        :param xi: 2D array with parameter sample vector(s)
            xi[s, j] = s-th sample of j-th individual parameter,
                concatenated by parameter sub-types as defined in base.
        :param rng: random Generator object for sampler
        :param prior: ref to owner EmaGroupModel
        :param id: key label of self
        """
        self.id = id
        self.base = base
        self.situation_count = situation_count
        self.rating_count = rating_count
        self.xi = xi
        self._sampler = ham.HamiltonianSampler(x=self.xi,
                                               fun=self._neg_ll,
                                               jac=self._grad_neg_ll,
                                               epsilon=0.2,
                                               n_leapfrog_steps=10,     # = default
                                               min_accept_rate=0.8,     # = default
                                               max_accept_rate=0.95,    # = default
                                               rng=rng
                                               )
        # keeping sampler properties across learning iterations
        self.prior = prior
        self.ll = None  # space for log-likelihood result from self.adapt()

    def __repr__(self):
        return (self.__class__.__name__ + '('
                + '\n\tsituation_count=' + f'{self.situation_count},'
                + '\n\trating_count=' + f'{self.rating_count},'
                + f'\n\txi= parameter array with shape {self.xi.shape}; id={id(self.xi)},'
                + f'\n\tid(prior)= {id(self.prior)},'
                + f'\n\tll= {self.ll})')

    @classmethod
    def initialize(cls, base, ema_df, rng, id=''):
        """Create model from recorded data
        :param base: single common EmaParamBase object
        :param ema_df: a pandas.DataFrame object for ONE respondent
        :param rng np.random.Generator for sampler use
        :param id: key to identify self (in logger output)
        :return: a cls instance
        """
        z = base.emf.count_situations(ema_df).reshape((base.emf.n_phases, -1))
        # z[k0, k] = number of EMA records at k0-th test phase
        # in k-th <=> (k1, k2, ...)-th situation, EXCL. k0= test phase
        y = [base.emf.count_grades(a, ema_df)
             for a in base.emf.attribute_dtypes.keys()]
        # y[i][l, k] = number of attribute_grades at l-th ordinal level for i-th ATTRIBUTE question
        # given k-th <=> (k0, k1, k2, ...)-th situation (INCL. k0= test phase)
        xi = base.initialize_xi(z, y)
        # dither to N_SAMPLES:
        xi = xi + DITHER_PARAM_SCALE * rng.standard_normal(size=(N_SAMPLES, len(xi)))
        return cls(base, z, y, xi, rng, id=id)

    def _kl_div_zeta(self, prior):
        """KLdiv for indicator variables zeta re prior
        = KLdiv{q(zeta | self.xi) || p(zeta | prior.mix_weight)}
        using current variational q(xi, zeta) = q(zeta | xi) q(xi)
        :param prior: ref to EmaGroupModel instance containing self
        :return: kl = scalar E{ ln q(zeta | self.xi) - ln p(zeta | prior.mix_weight)}

        Method: Leijon doc eq:VIlowerBoundCalc
        """
        w = prior.mean_conditional_zeta(self.xi)
        # w[c, s] = E{zeta_c | self.xi[s, :]} Leijon doc eq:ProbZetaGivenXi
        return np.sum(np.mean(w * (np.log(w + np.finfo('float').tiny)  # avoid log(0.) = nan
                                   - prior.mix_weight.mean_log[:, None]),
                              axis=1))

    def adapt(self, s_name):
        """Adapt parameter distribution self.xi
        to stored EMA count data, given the current self.w
        and the current estimate of population GMM components self.prior.comp.
        :param s_name: respondent id, for logger output  **** NOT NEEDED: using self.id ***
        :return: self, to send result via map() or Pool.imap()

        Result: Updated self.xi, and
            self.ll = E{ ln p(self.situation_count, self.rating_count | self.xi) }_q(xi)
                - E{ ln q(xi) / prior_p(xi) }_q(xi)
                - KLdiv( q(zeta | xi) || p(zeta | prior.mix_weight)
        """
        # find MAP point first:
        # lp_0 = - np.mean(self._neg_ll(self.xi), axis=0)  # ****** ref for test
        xi_0 = np.mean(self.xi, axis=0)
        res = minimize(fun=self._neg_ll,
                       jac=self._grad_neg_ll,
                       x0=xi_0)
        if res.success:
            xi_map = res.x.reshape((1, -1))
        else:
            raise RuntimeError(f'{self.id}: MAP search did not converge: '
                               + 'res= ' + repr(res))
        if len(self.xi) != N_SAMPLES:
            # run sampler starting from x_map
            self._sampler.x = xi_map
        else:
            # we have sampled before, start from those samples
            self._sampler.x = self.xi + xi_map - xi_0
        # **** ------------------------------------- test effect of MAP
        # lp_1 = - np.mean(self._neg_ll(self._sampler.x), axis=0)  # ***** test after MAP adjustment
        # print(f'adapt: Subj {s_name}: MAP adjustment: d_lp = {lp_1 - lp_0:.3f}')
        # -----------------------------------------------------
        self._sampler.safe_sample(n_samples=N_SAMPLES, min_steps=2)
        logger.debug(f'{self.id}: sampler.epsilon= {self._sampler.epsilon:.3f}. '
                     + f'accept_rate= {self._sampler.accept_rate:.1%}. '
                     + f'n_steps= {self._sampler.n_steps}')
        self.xi = self._sampler.x
        self.base.restrict(self.xi)
        # adjust for modified xi:
        self._sampler.U = self._sampler.potential(self._sampler.x)
        self._sampler.args = ()  # just in case a pickled prior copy was there
        # Calc log-likelihood contribution with final xi samples:
        lp_xi = - np.mean(self._sampler.U)  # after restrict_xi
        # lp_xi = E_xi{ ln p(data | xi) + self.prior.logpdf(xi) }
        h_xi = entropy(self.xi)
        # approx = - E{ ln q(xi) }
        kl_zeta = self._kl_div_zeta(self.prior)
        self.ll = lp_xi + h_xi - kl_zeta
        logger.debug(f'{self.id}: adapt: ll={self.ll:.3f}; '
                     + f'(lp_xi={lp_xi:.3f}; '
                     + f'h_xi= {h_xi:.3f}. '
                     + f'-kl_zeta= {-kl_zeta:.3f})')
        self.ll = lp_xi + h_xi - kl_zeta
        return self

    def _neg_ll(self, xi):
        """Objective function for self.adapt_xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: neg_ll = scalar or 1D array
            neg_ll[...] = - ln P{ self.situation_count, self.rating_count | xi[..., :]}
                    - ln p(xi[..., :] | prior)
            neg_ll.shape == xi.shape[:-1]
        """
        return - self.prior.logpdf(xi) - self.logprob(xi)

    def _grad_neg_ll(self, xi):
        """Gradient of self._neg_ll w.r.t. xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: dll = scalar or 1D array
            dll[..., j] = d _neg_ll(xi[..., :]) / d xi[..., j]
            dll.shape == xi.shape
        """
        return - self.prior.d_logpdf(xi) - self.d_logprob(xi)

    def logprob(self, xi):
        """log likelihood of EMA count data, given parameters xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: ll = scalar or 1D array
            ll[...] = ln P{ self.situation_count, self.rating_count | xi[..., :]}
            ll.shape == xi.shape[:-1]
        """
        ll_z = self.base.situation_logprob(xi, self.situation_count)
        ll_y = self.base.rating_logprob(xi, self.rating_count)

        # ----------- any rating_logprob = -inf -> ll_y == NaN
        if np.any(np.isnan(ll_y)):
            logger.warning('EmaRespondentModel.logprob: Some ll_y == NaN. Should never happen!')
        return ll_z + ll_y

    def d_logprob(self, xi):
        """Gradient of self.logprob(xi)
        :param xi: 1D or 2D array with candidate parameter vectors
        :return: d_ll = 1D or 2D array
            d_ll[..., j] = d ln P{ self.situation_count, self.attribute_grades | xi[..., :]} / d xi[..., j]
            d_ll.shape == xi.shape
        """
        d_ll_z = self.base.d_situation_logprob(xi, self.situation_count)
        # = list of arrays with shapes concatenable along axis=-1
        d_ll_y = self.base.d_rating_logprob(xi, self.rating_count)
        # = list of arrays with shapes concatenable along axis=-1
        return np.concatenate(d_ll_z + d_ll_y, axis=-1)

    def rvs(self, size=N_SAMPLES):
        # re-sample if size != len(self.xi) ???
        return self.xi
