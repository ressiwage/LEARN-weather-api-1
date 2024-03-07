from .resources import requests, json, datetime
#TODO:
# on demand and pooling mode
# two instances with same key not possible
class Apis:
    def __init(self):
        self.keys=set()
    def get_api(self, api_key):
        if api_key not in self.keys:
            return __Api(api_key)
        else:
            raise Exception('multiple apis with same keys not allowed')

        
class __Api:
    def __init__(self, api_key):
        self.api_key = api_key
        #check if correct key
        
    def get_weather(city, time="now"):
        """

        @city=string
        @time={'now'|datetime.datetime}
        """
        if time!='now' and not isinstance(time, datetime.datetime):
            raise Exception('incorrect time argument')
        
    