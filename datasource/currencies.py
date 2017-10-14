# currencies.py
# by James Fulford
# converts currencies by retriving conversion data and using inheritance and classes.
# began 6/14/2016
# ended 6/19/2016
# reformed to make more importable 12/24/2016


def get_rates(classes=False):
    """
    datasource.currencies.get_rates
    Returns a dictionary full of conversion rates
        what the 3 letters mean: https://oxr.readme.io/docs/supported-currencies
    Setting classes=True adds a class for each currency.
    """
    import urllib
    import json
    from credentials import credentials

    url = "https://openexchangerates.org/api/latest.json?app_id={}"
    response = urllib.urlopen(url.format(credentials["openexchangerates"]["app_id"]))
    conversions = json.load(response)["rates"]  # dict of conversion rates.
    if(classes):
        class Currency(object):
            """Base class for all currencies."""
            def __init__(self, amount):
                assert type(amount) == float or type(amount) == int, amount
                self.amount = amount

            def __str__(self):
                return str(self.__class__.__name__) + ": " + str(self.amount)

            def get_rate(self):
                return conversions[self.__class__.__name__]

            def convert_to(self, currency):
                value = self.amount
                value *= rates()[str(currency.__name__)]
                value /= self.get_rate()
                returningValue = currency(value)
                return returningValue

            convert = exchange_for = exchange = convert_to

        for currency in conversions.keys():
            globals()[str(currency)] = type(str(currency), (Currency,), {
                '__name__': currency,
                '__doc__': str(currency) + " currency class"
            })  # adds currencies to globals
    return conversions
