
.. automodule:: astroNN.lamost

Mini Tools for LAMOST data - **astroNN.lamost**
=================================================

This module is designed for dealing with LAMOST DR5.

**LAMOST DR5 is not a public data release yet, this module only provides a limited amount of tools to deal with the spectra.
If you do not have the data, astroNN will not provide any LAMOST DR5 data nor functions to download them.**

*LAMOST Data Policy*: http://www.lamost.org/policies/data_policy.html

*LAMOST DR5 Homepage*: http://dr5.lamost.org/

*LAMOST DR5 Data Model*: http://dr5.lamost.org/doc/data-production-description

------------------------------------
LAMOST Spectra Wavelength Solution
------------------------------------

.. autofunction::  astroNN.lamost.wavelength_solution

You can retrieve APOGEE spectra wavelength solution by

.. code:: python

   from astroNN.lamost import wavelength_solution

   lambda_solution = wavelength_solution(dr=14)
