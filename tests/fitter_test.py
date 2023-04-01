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
from fitter_module import load_data
from fitter_module import model_function
from fitter_module import fit_data

import numpy as np
import pandas as pd
import pytest

from hypothesis import example, given, strategies

def test_load_data():
    data = load_data('data.csv')
    assert type(data) == pd.DataFrame

@pytest.mark.parametrize(
    "x,a,b,expected", [(0, 1, 1, 1), (np.pi/2, 1, 1, 2)]
)
def test_model_function(x, a, b, expected):
    assert model_function(x, a, b) == expected

def test_load_wrong_data():
    # how could we issue a better error?
    with pytest.raises(FileNotFoundError):
        load_data("toto.csv")

def test_fit_data_exception():
    # how we could make our function more robust to this?
    with pytest.raises(ValueError):
        x = np.arange(10)
        y = np.ones(10)
        y[0] = None
        fit_data(x, y)

@given(
    a=strategies.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000),
    b=strategies.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000),
)
def test_idempotence(a, b):
    # what if we release the bounds?
    x0 = np.arange(0., 4 * np.pi, 0.1)
    y0 = a * np.sin(x0) + b

    params0, errs0 = fit_data(x0, y0)

    y1 = params0[0] * np.sin(x0) + params0[1]
    params1, errs1 = fit_data(x0, y1)

    assert np.allclose(params0[0], params1[0], atol=1e-6)