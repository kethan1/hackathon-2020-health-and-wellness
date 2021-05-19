import json
from urllib.parse import urlencode
from urllib.request import urlopen

class RecallsAPI(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.fda.gov/food/enforcement.json?' 

    def search(self, params):
        url = self.base_url + 'api_key=%s%s' % \
            (self.api_key, params)
        response = urlopen(url).read()
        return json.loads(response)
