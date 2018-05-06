import requests

class BlocknadoREST:

    def __init__(self, apiKey='', apiSecret=''):
        self.baseURL = 'https://blocknado.com/api/v1'
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def publicAPICall(self, call, params={}):
        data = requests.get("%s/%s" % (self.baseURL, call), params=params)
        return data.json()

    def privateAPICall(self, call, params={}):
        pass

    def markets(self):
        return self.publicAPICall("markets");
