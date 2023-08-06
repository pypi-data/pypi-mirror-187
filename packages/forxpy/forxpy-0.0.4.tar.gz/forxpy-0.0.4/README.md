 # forxpy

Package to access daily exchange rates and forex conversion created by Group 6: Dhruvi Nishar, Mohammad Reza Nabizadeh, Hongjian Li, and Stepan Zaiatc.

`forxpy` allows users to easily convert currency rates by utilizing data from [Bank of Canada](https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/). The package supports multiple currencies and provides historical exchange rates. It also has the ability to make currency conversions with the use of a simple function call, making it easy for developers to integrate into their projects. Additionally, it provides a way to get historical exchange rates in a chart, which makes it useful for dashboard building. Overall, **forxpy** is a powerful and flexible package for handling currency conversions in Python.

## Installation

```bash
$ pip install forxpy
```

## Usage

`forxpy` can be used to get the daily exchange rate data, currency conversion, and plotting  as below:

```python
from forxpy.forxpy import *

data = retrieve_data(export_csv = False)
fastest_slowest_currency('2019-05-23', '2022-05-30')
currency_convert(23, 'USD', 'CAD')
sbs_plot = plot_historical('2020-05-23', '2022-05-30', 'USD', 'CAD')
```

### Functions included in the package:

- **retrieve_data()**: Retrieve historical daily currency exchange rate data for Canadian Dollars in CSV format from the Bank of Canada website.
- **currency_convert**: The conversion rate is based on the average exchange rate by the 4:00 pm ET of the closest business day.
- **fastest_slowest_currency()**: This function takes start and end date as input and returns a  list of two lists containing the fastest and slowest growing currency exchange rate in relation to Canadian Dollar along with their current exchange rate in the provided date range.
- **plot_historical()**:Plots the historical rate of the entered currencies within a specific period of time.

**forxpy** can be a useful tool for many industries that require currency conversions. Here are a few examples:
1. **Finance and Banking**: Banks and financial institutions often need to convert currencies for international transactions, and "forxpy" can provide accurate and up-to-date exchange rates for these purposes.
2. **E-commerce**: Online retailers that sell internationally may need to display prices in multiple currencies, and "forxpy" can help them convert the prices in real-time.
3. **Travel and Tourism**: Travel agencies and booking websites may need to convert currency for pricing and budgeting purposes, and "forxpy" can provide them with accurate exchange rates.
4. **Data Analysis**: Companies that conduct global business can use "forxpy" to collect and analyze historical exchange rate data, which can be useful for making business decisions and forecasting.
5. **Cryptocurrency**: As the cryptocurrency markets are decentralized and global, the package can be used to convert cryptocurrency prices to different fiat currencies, which is helpful for investors and traders.

Overall, "forxpy" can be a valuable tool for any industry that needs to handle currency conversions in Python.

## Similar Packages

1. [`forex-python`](https://pypi.org/project/forex-python/): Used to retrieve foreign currency exchange rates and currency conversion.
2. [`CurrencyConverter`](https://pypi.org/project/CurrencyConverter/): This is a currency converter package that uses historical rates against a reference currency (Euro)


## Contributing
**Authors**: Dhruvi Nishar, Mohammad Reza Nabizadeh, Hongjian Li, and Stepan Zaiatc.

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`forxpy` was created by Group 6 - Dhruvi Nishar, Mohammad Reza Nabizadeh, Hongjian Li, and Stepan Zaiatc. It is licensed under the terms of the MIT license.

## Credits

`forxpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
