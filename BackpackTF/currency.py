import requests

BACKPACK_TF_URL = "https://backpack.tf/api/{url}/v{version}"


class ApiRequestError(Exception):
    pass


class Currency:
    """
    Documentation for the backpack.tf API https://backpack.tf/api/index.html#/
    """

    def __init__(self, apikey):
        self.apikey = apikey

    def _request(self, url, params, version=1):
        params.update(
            {"key": self.apikey,}
        )
        response = requests.get(
            BACKPACK_TF_URL.format(url=url, version=version), params=params
        )
        json_data = response.json()["response"]
        if int(json_data["success"]) == 1:
            return json_data
        else:
            raise ApiRequestError(json_data["message"])

    def get_currencies(self):
        """
        Function Returning a dictionary of the value of currencies
        """
        response = self._request("IGetCurrencies", {})
        return response["currencies"]

    def price_history(
        self, name="", quality="Unique", craftable=1, tradable=1, priceIndex=0
    ):
        """
        Gets Price History of a specific item in an array of previous values
        
        Name - The item's base name
        Quality - The item's quality, Strange, Unique, Unusual
        Craftable - Get the item's craftable or not 0 or 1
        Tradable - get the item's tradable status
        PriceIndex - Most items is 0, however particle effects is the ID of the particle effect
          for crates it corresponds to the crate series, for strangifiers/unusualifiers is the
          definition index of the item it can be used on, chemistry set is a hyphented
          definition index 1086-14 is the index for a collector's festive wrangler
          here's a link to an item http://prntscr.com/pf2s0h
        """
        params = {
            "appid": "440",
            "quality": quality,
            "item": name,
            "tradable": tradable,
            "craftable": craftable,
            "priceindex": priceIndex,
        }
        response = self._request("IGetPriceHistory", params)
        return response["history"]

    def item_price(
        self, name="", quality="Unique", craftable=1, tradable=1, priceIndex=0
    ):
        """
        Gets Price of a specific item
        
        Name - The item's base name
        Quality - The item's quality, Strange, Unique, Unusual
        Craftable - Get the item's craftable or not 0 or 1
        Tradable - get the item's tradable status
        PriceIndex - Not really sure to be honest
        """
        response = self.price_history(name, quality, craftable, tradable, priceIndex)
        if len(response):
            return response[-1]

    def get_all_prices(self, raw=2, since=0):
        """
        Gets all prices, requires an elevated API key
    
        Since - Only prices that have been updated since the unix EPOCH will be shown
        """
        params = {
            "raw": raw,
            "since": since,
        }
        return self._request("IGetPrices", params, version=4)

    # alias for compatibility with older versions
    getCurrencies = get_currencies
    priceHistory = price_history
    itemPrice = item_price
    getAllPrices = get_all_prices
