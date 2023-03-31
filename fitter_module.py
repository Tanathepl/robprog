from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

def load_data(fn):
    data = pd.read_csv(fn, sep=',')
    return data

def model_function(x, a, b):
    return a * np.sin(x) + b

def fit_data(x, y):
    params, cov = curve_fit(model_function, x, y)

    err = np.sqrt(np.diag(cov))

    return params, err

def plot_fit(x, y, params, errors):
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
    # tests?
    pass
