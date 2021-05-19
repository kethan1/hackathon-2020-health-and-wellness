import json
from urllib.parse import urlencode
from urllib.request import urlopen

class AirAPI(object):
    def __init__(self, api_key):
        self.base_url = 'https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&API_KEY=%s' % api_key 

    def search(self, zip_code):
        url = self.base_url + '&zipCode=%s' % \
            (zip_code)
        response = urlopen(url).read()
        return json.loads(response)
