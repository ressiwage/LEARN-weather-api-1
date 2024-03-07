from .resources import requests, json, datetime
from .utils import timed_lru_cache
#TODO:
# on demand and pooling mode

class Apis:
    
    keys=set()
    def get_api(self, api_key):
        if api_key not in self.keys:
            return Api(api_key, self)
        else:
            raise Exception('multiple apis with same keys not allowed')
        
    def __delete(self, child):
        pass

        
class Api:
    def __init__(self, api_key, parent):
        self.api_key = api_key
        #check if correct key
        check = requests.get(
            rf"""https://api.openweathermap.org/data/2.5/weather?lat=55.751244&lon=37.618423&exclude=current&appid={self.api_key}"""
            )
        self.latest_cities=list()
        if check.status_code==401:
            raise Exception('invalid api key')

    @timed_lru_cache(60*10, 10)
    def get_weather(self, city):
        """
        @city=string
        """
        coordinates = self.__get_city_coordinates(city)
        
        resp = requests.get(
            rf"""https://api.openweathermap.org/data/2.5/weather?lat={coordinates["lat"]}&lon={coordinates["lon"]}&exclude=current&appid={self.api_key}"""
            )
        if resp.status_code==401:
            raise Exception('invalid api key')
        self.latest_cities.append(coordinates['_name'])
        if self.latest_cities.__len__>10:
            self.latest_cities.pop(0)
        return resp.json()
        

        
    def __get_city_coordinates(self, city):
        resp = requests.get(
            rf"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}").json()
        if len(resp)==0:
            raise Exception('city not found')
        return {'lat':resp[0]['lat'], 'lon':resp[0]['lon'], '_name':resp[0]['name']}
    