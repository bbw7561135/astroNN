Gaia DR2 Preparation and Possible Science with astroNN
========================================================

Gaia DR2 will be released on 25 April 2018 with data collected from 25 July 2014 to 23 May 2016 with 1.5 billion sources.

Official Gaia DR2 page: https://www.cosmos.esa.int/web/gaia/dr2

astroNN will be used to train neural network with Gaia DR1 parallax to predict intrinsic brightness of stars from APOGEE
spectra. Since Gaia uses geometric method to infer distances to stars, and it has its own limitation, the major one
will be the star must be close to us. If neural network can infer intrinsic brightness based on APOGEE spectra, with apparent
magnitude we can get the distance as long as we have the stellar spectra.

This page will act as a notebook for the author (Henry) and share his latest update on Gaia DR2 preparation.

FAQ: What is fakemag? : http://astronn.readthedocs.io/en/latest/tools_gaia.html#fakemag-dummy-scale

FAQ: Which band I will use for apparent magnitude?: K-mag will be used to minimize the effect of extinction

Plans/Questions
------------------

#. Train nerual network on Gaia DR1 and validate on Gaia DR2
#. Temperature cuts on spectra?

#. If neural network turns out very accurate when DR2 comes out, how did neural network predict those distance
#. If neural network turns out very accurate when DR2 comes out, then we can get distance for many APOGEE spectra
#. If neural network failed, is predicting intrinsic brightness from APOGEE spectra impossible, or just because the training set is too small in DR1 led to failure


2M16363993+3654060 Distance Disagreement between astroNN and Gaia/Anderson2017 Parallax
-----------------------------------------------------------------------------------------

.. image:: gaia_dr2/fakemag.png

Neural Network trained on Anderson2017 parallax constantly predicted an almost constant offset with very small uncertainty
to the ground truth (Anderson2017) on the star with APOGEE_ID `2M16363993+3654060`. astroNN agreed pretty well with APOGEE_distances BPG_dist50.
Seems like Gaia/Anderson2017 are the one which is far off.

I have to emphasise that the neural network is trained on the parallax from Anderson2017 which is improved parallax
from Gaia DR1. There is no surprise that neural network identified outliers from the training/testing set. But
the fact that neural network managed to have a similar answer with `APOGEE_distances BPG_dist50` may indicate neural
network learned some "correct" physics to infer intrinsic distance from APOGEE spectra.

The result:

#. astroNN Bayesian Neural Network [#f1]_ : :math:`2188.34 \text{ parsec} \pm 395.16 \text{ parsec}`
#. APOGEE_distances BPG_dist50 [#f2]_ : :math:`2266.15 \text{ parsec} \pm 266.1705 \text{ parsec}`
#. Anderson2017 parallax: :math:`568.08 \text{ parsec} \pm 403.86 \text{ parsec}`
#. Gaia DR1 parallax: :math:`318.05 \text{ parsec} \pm 1021.73 \text{ parsec}`

.. rubric:: Footnotes

.. [#f1] Trained on ASPCAP parameters [Teff, Log(g) and 22 abundances] and Anderson2017 parallax
.. [#f2] http://www.sdss.org/dr14/data_access/value-added-catalogs/?vac_id=apogee-dr14-based-distance-estimations


Distance Prediction with APOGEE Spectra
----------------------------------------------------

The model will be uploaded here later