import requests

class UnauthenticatedException(Exception):
    pass

class BlocknadoREST:

    def __init__(self, apiKey='', apiSecret=''):
        self.baseURL = 'https://blocknado.com/api/v1'
        self._apiKey = apiKey
        self._apiSecret = apiSecret

    def getCredentials(self):
        return (self._apiKey, self._apiSecret)

    def checkCredentialsSet(self):
        if not self._apiKey or not self._apiSecret:
            return False
        return True

    def publicAPICall(self, call, params={}):
        data = requests.get("%s/%s" % (self.baseURL, call), params=params)
        return data.json()

    def privateAPICall(self, call, params={}):
        if not self.checkCredentialsSet():
            raise UnauthenticatedException("Must provide an API Key and Secret")
        pass

    def markets(self):
        return self.publicAPICall("markets");
