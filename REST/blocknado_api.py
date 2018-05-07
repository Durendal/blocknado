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
        self._markets = ['btc-ltc', 'btc-rby', 'btc-dash', 'btc-vtc']
    def getCredentials(self):
        return (self._apiKey, self._apiSecret)

    def checkCredentialsSet(self):
        if not self._apiKey or not self._apiSecret:
            return False
        return True

    def publicAPICall(self, call, params=[]):
        url = "%s/%s" % (self.baseURL, call)
        if len(params) > 0:
            url = "%s/%s" % (url, '/'.join(params))
        data = requests.get(url)
        return data.json()

    def privateAPICall(self, call, params=[]):
        if not self.checkCredentialsSet():
            raise UnauthenticatedException("Must provide an API Key and Secret")
        pass

    def markets(self):
        return self.publicAPICall("markets");

    def orderbook(self, symbol):
        if symbol not in self._markets:
            raise NonexistantMarketException("The selected market: %s does not exist" % symbol)
        symbol = [symbol]
        return self.publicAPICall("orderbook", params=symbol)
