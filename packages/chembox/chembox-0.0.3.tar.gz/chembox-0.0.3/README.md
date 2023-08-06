# chembox

## Introduction

`chembox` is a package for molecular information calculator based on empirical formulas of chemicals in raw text. It is designed to intelligently process text input containing the chemical formula and provide associated information on the inquired molecule. It is able to provide the molar mass, check a formula's validity, and provide a balanced combustion equation if the input is combustible. This tool can be utilized for various educational and research purposes for simple and fast information retrieval.

We are using a dataset that contains established element data properties from [this site](https://github.com/Bluegrams/periodic-table-data/blob/master/Periodica.Data/Data/ElementData.csv).

## Installation

`chembox` is developed and tested on Python 3.10. You can install it from PyPi via pip:

```bash
$ pip install chembox
```

## Usage

The package includes 4 functions for solving chemistry problems:

- `get_elements`a parser that takes a chemical formula in string format and returns a dictionary that contains the elements and their respective count. 

- `is_valid`: a checker that returns a boolean indicating whether a given input is chemically reasonable.

- `get_molec_props`: a method that takes a chemical formula in string format and returns a dataframe with various useful properties of each element in the formula.

- `get_combustion_equation`: a method that takes a text chemical formula that only contains carbon (`C`) and hydrogen (`H`) and outputs a balanced equation resulting from combustion.

## Dataset

In order to be able to perform some of the functions above, a dataset will need to be used that contains various atomic properties of the elements in the periodic table. The data can be found in the Chembox repo [here](https://github.com/UBC-MDS/chembox/tree/main/src/chembox/data) which was sourced from [here](https://github.com/Bluegrams/periodic-table-data/tree/master/Periodica.Data/Data). Please note that we do not take credit for the dataset, it is merely for use with our functions.

## Fitting into the Python ecosystem

A similar package [chemsolve](https://github.com/amogh7joshi/chemsolve) is available online that employs a similar string-parsing design and molar mass calculation.

What we do differently:

- We include a dataframe of the molecule properties to give the user enhanced functionality and insights.

- `chemsolve` accepts user-defined reactions. In our package, we include methods for automated combustion equation generation and balancing.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a [Code of Conduct](https://github.com/UBC-MDS/chembox/blob/main/CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## License

`chembox` is licensed under the terms of the MIT license.

## Contributors
The contributors of this project are
Wilfred Hass, Vikram Grewal, Luke Yang, and Nate Puangpanbut.


<a href="https://github.com/UBC-MDS/chembox/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=UBC-MDS/chembox&max=1000" />
</a>

## Credits

`chembox` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
