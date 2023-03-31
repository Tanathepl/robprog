from fitter_module import load_data
from fitter_module import fit_data
from fitter_module import plot_fit

import sys

def main():
    """ TBD """
    fn = sys.argv[1]

    data = load_data(fn)

    params, errors = fit_data(data['x'], data['y'])

    plot_fit(data['x'], data['y'], params, errors)


if __name__ == "__main__":
    main()
