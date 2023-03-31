# Copyright 2023 Julien Peloton
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Tuple, TypeVar

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import seaborn as sns
sns.set_context('talk')

T = TypeVar('T', float, np.ndarray)

def load_data(fn: str) -> pd.DataFrame:
    """ Load data

    Parameters
    ----------
    fn: str
        Name of the file to open.
        The data must be formatted as csv.

    Returns
    ----------
    pd.DataFrame
        File data as a pd.DataFrame

    Examples
    ----------
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> filename = os.path.join(dir_path, '../data.csv')
    >>> pdf = load_data(filename)
    """
    data = pd.read_csv(fn, sep=',')
    return data

def model_function(x: T, scale: float, offset: float) -> T:
    """ Evaluate sine function at angle `x` with parameters `scale` and `offset`

    Parameters
    ----------
    x: array_like
        Angle, in radians (:math:`2 \pi` rad equals 360 degrees).
    scale: float
        scale factor for the sine
    offset: float
        Offset

    Returns
    ----------
    array_like
        The scaled sine of each element of `x`.
        This is a scalar if `x` is a scalar.

    Notes
    ----------
    The sine is one of the fundamental functions of trigonometry (the
    mathematical study of triangles).  Consider a circle of radius 1
    centered on the origin.  A ray comes in from the :math:`+x` axis, makes
    an angle at the origin (measured counter-clockwise from that axis), and
    departs from the origin.  The :math:`y` coordinate of the outgoing
    ray's intersection with the unit circle is the sine of that angle.  It
    ranges from -1 for :math:`x=3\pi / 2` to +1 for :math:`\pi / 2.`  The
    function has zeroes where the angle is a multiple of :math:`\pi`.
    Sines of angles between :math:`\pi` and :math:`2\pi` are negative.
    The numerous properties of the sine and related functions are included
    in any standard trigonometry text.

    Examples
    -----------
    >>> scale, offset = 1.0, 0.0
    >>> np.allclose(model_function(np.pi, scale, offset), 0.0)
    True

    >>> scale, offset = 2.0, -1.0
    >>> np.allclose(model_function(np.pi, scale, offset), -1.0)
    True
    """
    return scale * np.sin(x) + offset

def fit_data(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """ Use non-linear least squares to fit `model_function` to data (`x`, `y`)

    Assumes ``ydata = model_function(xdata)``, with default parameters
    of ``optimize.curve_fit`` from scipy.

    Parameters
    ----------
    x: array
        The independent variable where the data is measured.
    y: array
        The dependent data, nominally ``model_function(x, ...)``.

    Returns
    ----------
    params: array
        Optimal values for the parameters so that the sum of the squared
        residuals of ``f(xdata) - ydata`` is minimized.
    errors: array
        The estimated one standard deviation errors
        on the parameters from the covariance returned by
        `optimize.curve_fit`: ``errors = np.sqrt(np.diag(pcov))``.

    Notes
    -----
    The algorithm uses the Levenberg-Marquardt algorithm
    through `leastsq`. Note that this algorithm can only deal with
    unconstrained problems.

    See Also
    --------
    scipy.optimize.least_squares : Minimize the sum of squares of
        nonlinear functions.
    scipy.stats.linregress : Calculate a linear least squares regression for
        two sets of measurements.

    Examples
    -----------
    >>> xdata = np.arange(0, 4 * np.pi, 0.1)
    >>> ydata = np.sin(xdata)
    >>> params, errors = fit_data(xdata, ydata)
    >>> np.allclose(params[0], 1.0)
    True
    """
    params, cov = curve_fit(model_function, x, y)

    err = np.sqrt(np.diag(cov))

    return params, err

def plot_fit(
        x: np.ndarray, y: np.ndarray,
        params: np.ndarray, errors: np.ndarray) -> None:
    """ Plot fit against measurements

    Parameters
    ----------
    x: ndarray
        The independent variable where the data is measured.
    y: ndarray
        The dependent data
    params: ndarray
        Optimal values for the parameters from `fit_data`
    errors: ndarray
        The estimated one standard deviation errors
        on the parameters from `fit_data`
    """
    _ = plt.figure(figsize=(12, 6))
    plt.plot(
        x, y, ls='', marker='o',
        label='data'
    )
    plt.plot(
        x, model_function(x, *params), '--',
        label='fit'.format(*params)
    )
    plt.title(
        r'$f(x) = a \times sin(x) + b$, with a = {:.2f} $\pm$ {:.2f}, b = {:.2f} $\pm$ {:.2f}'.format(
            *np.transpose((params, errors)).flatten()
        )
    )
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    """ Run the unit test suite """
    import doctest
    import sys
    sys.exit(doctest.testmod()) # type: ignore  # noqa
