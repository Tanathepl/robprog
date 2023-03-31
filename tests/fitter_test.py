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
    x=strategies.floats(allow_nan=False, allow_infinity=False, width=32),
    a=strategies.floats(allow_nan=False, allow_infinity=False, width=32),
    b=strategies.floats(allow_nan=False, allow_infinity=False, width=32),
)
@example(x=0, a=1, b=1)
def test_add__hypothesis(x, a, b):
    # what if we relax nan & inf?
    # what if we relax width=32?
    x = np.deg2rad(x % 360)
    assert model_function(x, a, b) <= np.abs(a) + np.abs(b)