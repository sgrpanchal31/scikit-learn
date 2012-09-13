# Author: Christian Osendorfer <osendorf@gmail.com>
#         Alexandre Gramfort <alexandre.gramfort@inria.fr>
# Licence: BSD3

import numpy as np

from nose.tools import assert_true

from sklearn.decomposition import FactorAnalysis


def test_fa_generative():
    """Test FactorAnalysis ability to recover the data covariance structure
    """
    n_samples, n_features, n_components = 20, 5, 3

    # Some random settings for the generative model
    W = np.random.randn(n_components, n_features)
    # latent variable of dim 3, 20 of it
    h = np.random.randn(n_samples, n_components)
    # using gamma to model different noise variance
    # per component
    noise = np.random.gamma(1, size=n_features) \
                * np.random.randn(n_samples, n_features)

    # generate observations
    # wlog, mean is 0
    X = np.dot(h, W) + noise

    fa = FactorAnalysis(n_components=n_components)
    fa.fit(X)
    X_t = fa.transform(X)
    assert_true(X_t.shape == (n_samples, n_components))

    # Sample Covariance
    scov = np.cov(X, rowvar=0., bias=1.)

    # Model Covariance
    mcov = fa.get_covariance()
    diff = np.sum(np.abs(scov - mcov)) / W.size
    assert_true(diff < 0.1, "Mean absolute difference is %f" % diff)
