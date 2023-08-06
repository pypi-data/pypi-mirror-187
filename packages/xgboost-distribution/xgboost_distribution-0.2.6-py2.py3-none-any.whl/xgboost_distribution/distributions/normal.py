"""Normal distribution
"""
import numpy as np
from scipy.stats import norm

from xgboost_distribution.distributions.base import BaseDistribution


class Normal(BaseDistribution):
    """Normal distribution with log scoring

    Definition:

        f(x) = exp( -[ (x-mean) / std ]^2 / 2 ) / std

    We reparameterize:

        a = mean         |  a = mean
        b = log ( std )  |  e^b = std

    (Note: reparameterizing to log(std) ensures that std >= 0, regardless of
    what the xgboost booster internally outputs, as std = e^b > 0.)

    The gradients are:

        d/da -log[f(x)] = e^(-2b) * (x-a) = (x-a) / var
        d/db -log[f(x)] = 1 - e^(-2b) * (x-a)^2 = 1 - (x-a)^2 / var

    as var = std^2 = e^(2b)

    The Fisher Information (diagonal):

        I(mean) = 1 / var
        I(std) = 2 / var

    In reparameterized form, we find I_r:

        1 / var = I_r [ d/d(mean) mean ]^2 = I
        2 / var = I_r [ d/d(std) log(std) ]^2 = I ( 1/(std) )^2

    Hence the reparameterized Fisher information:

        [ 1 / var, 0 ]
        [ 0,       2 ]

    Ref:

        https://www.wolframalpha.com/input/?i=d%2Fda+-log%28%28e%5E%28-%5B%28x-a%29%2Fe%5Eb%29%5D%5E2+%2F+2%29+%2F+e%5Eb%29%29
        https://www.wolframalpha.com/input/?i=d%2Fdb+-log%28%28e%5E%28-%5B%28x-a%29%2Fe%5Eb%29%5D%5E2+%2F+2%29+%2F+e%5Eb%29%29

    """

    @property
    def params(self):
        return ("loc", "scale")

    def gradient_and_hessian(self, y, params, natural_gradient=True):
        """Gradient and diagonal hessian"""

        loc, log_scale = self._split_params(params)
        var = np.exp(2 * log_scale)

        grad = np.zeros(shape=(len(y), 2))
        grad[:, 0] = (loc - y) / var
        grad[:, 1] = 1 - ((y - loc) ** 2) / var

        if natural_gradient:
            fisher_matrix = np.zeros(shape=(len(y), 2, 2))
            fisher_matrix[:, 0, 0] = 1 / var
            fisher_matrix[:, 1, 1] = 2

            grad = np.linalg.solve(fisher_matrix, grad)

            hess = np.ones(shape=(len(y), 2))  # we set the hessian constant
        else:
            hess = np.zeros(shape=(len(y), 2))  # diagonal elements only
            hess[:, 0] = 1 / var
            hess[:, 1] = 2 * ((y - loc) ** 2) / var

        return grad, hess

    def loss(self, y, params):
        loc, scale = self.predict(params)
        return "NormalDistribution-NLL", -norm.logpdf(y, loc=loc, scale=scale)

    def predict(self, params):
        loc, log_scale = self._split_params(params)
        # TODO: do we need clipping for safety?
        # log_scale = np.clip(log_scale, -100, 100)
        scale = np.exp(log_scale)

        return self.Predictions(loc=loc, scale=scale)

    def starting_params(self, y):
        return np.mean(y), np.log(np.std(y))

    def _split_params(self, params):
        """Return loc and log_scale from params"""
        return params[:, 0], params[:, 1]
