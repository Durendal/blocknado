from urllib.parse import urlencode
from time import time
import hashlib
import hmac

import requests

class UnauthenticatedException(Exception):
    pass
class NonexistantMarketException(Exception):
    pass

class BlocknadoREST:

    def __init__(self, apiKey='', apiSecret=''):
        self.baseURL = 'https://blocknado.com/api/v1'
        self._apiKey = apiKey
        self._apiSecret = apiSecret
        self._markets = [x['market'] for x in self.markets()]

    def getCredentials(self):
        return (self._apiKey, self._apiSecret)

    def checkCredentialsSet(self):
        if not self._apiKey or not self._apiSecret:
            return False
        return True

    def _getURL(self, call):
        return "%s/%s" % (self.baseURL, call)

    def publicAPICall(self, call, params=[]):
        url = self._getURL(call)
        if len(params) > 0:
            url = "%s/%s" % (url, '/'.join(params))
        data = requests.get(url)
        return data.json()

    def privateAPICall(self, call, params={}):
        if not self.checkCredentialsSet():
            raise UnauthenticatedException("Must provide an API Key and Secret")
        url = self._getURL(call)
        params['nonce'] = int(time())
        params = urlencode(params).encode('utf-8')
        sign = hmac.new(bytes(self._apiSecret, 'latin-1'), params, hashlib.sha512).hexdigest()
        headers = {
            "Key": self._apiKey,
            "Sign": sign
        }

        data = requests.post(url, data=params, headers=headers)
        return data.json()

    def markets(self):
        return self.publicAPICall("markets");

    def orderbook(self, market):
        if market.upper() not in self._markets:
            raise NonexistantMarketException("The selected market: %s does not exist" % market)
        return self.publicAPICall("orderbook", params=[market])

    def buy(self, market, amount, price):
        return self.privateAPICall('buy', {"market": market, "amount": amount, "price": price})

    def sell(self, market, amount, price):
        return self.privateAPICall('sell', {"market": market, "amount": amount, "price": price})

    def cancel(self, orderID):
        return self.privateAPICall('cancel', {"orderNumber": orderID})

    def open(self, market):
        return self.privateAPICall('open', {"market": market})

    def order(self, orderID):
        return self.privateAPICall('order', {"orderNumber": orderID})

    def balances(self):
        return self.privateAPICall('balances')
