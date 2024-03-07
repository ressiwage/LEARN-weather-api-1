from .resources import requests, asyncio, aiohttp
from .utils import timed_lru_cache


class Apis:
    def __init__(self):
        self.keys=set()
    def get_api(self, api_key):
        """
        Creates a new instance of the `Api` class with the provided API key.
        If an instance with the same API key already exists, it raises an exception.

        Args:
            api_key (str): The API key for the new `Api` instance.

        Returns:
            Api: The new `Api` instance.

        Raises:
            Exception: If an instance with the same API key already exists.
        """
        if api_key not in self.keys:
            self.keys.add(api_key)
            return Api(api_key, self)
        else:
            raise Exception('multiple apis with same keys not allowed')
        
    def _delete(self, child):
        """
        Deletes an instance of the `Api` class.

        Args:
            child (Api): The `Api` instance to be deleted.
            """
        self.keys.remove(child.api_key)
        del child

        
class Api:
    def __init__(self, api_key, parent=None):
        """
        Initializes a new instance of the `Api` class with the provided API key and parent `Apis` instance.
        It checks if the API key is valid by making a request to the OpenWeatherMap API.

        Args:
            api_key: The API key used to authenticate requests to the OpenWeatherMap API.
            parent: The parent `Apis` instance that created the current instance of the `Api` class.
        """
        self.api_key = api_key
        self.parent=parent
        #check if correct key
        check = requests.get(
            rf"""https://api.openweathermap.org/data/2.5/weather?lat=55.751244&lon=37.618423&exclude=current&appid={self.api_key}"""
            )
        self.latest_cities=list()
        if check.status_code==401:
            raise Exception('invalid api key')

    
    def get_weather(self, city):
        """
        @city=string
        """
        @timed_lru_cache(60*10, 10)
        def cached(city):
            coordinates = self.__get_city_coordinates(city)
        
            resp = requests.get(
                rf"""https://api.openweathermap.org/data/2.5/weather?lat={coordinates["lat"]}&lon={coordinates["lon"]}&exclude=current&appid={self.api_key}"""
                )
            if resp.status_code==401:
                raise Exception('invalid api key')
            return resp
        resp = cached(city)
        self.latest_cities.append(city)
        if self.latest_cities.__len__()>10:
            self.latest_cities.pop(0)
        return resp.json()
    
    def __get_city_coordinates(self, city):
        resp = requests.get(
            rf"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}").json()
        if len(resp)==0:
            raise Exception('city not found')
        return {'lat':resp[0]['lat'], 'lon':resp[0]['lon'], '_name':resp[0]['name']}
        
    async def get_weather_async(self, city):
        """
        Asynchronously gets weather for a given city.
        """
        coordinates = await self.__get_city_coordinates_async(city)
        async with aiohttp.ClientSession() as session:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates['lat']}&lon={coordinates['lon']}&exclude=current&appid={self.api_key}"
            async with session.get(url) as resp:
                if resp.status == 401:
                    raise Exception('invalid api key')
                data = await resp.json()
                return data

    async def __get_city_coordinates_async(self, city):
        """
        Asynchronously gets city coordinates.
        """
        async with aiohttp.ClientSession() as session:
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
            async with session.get(url) as resp:
                data = await resp.json()
                if len(data) == 0:
                    raise Exception('city not found')
                return {'lat': data[0]['lat'], 'lon': data[0]['lon'], '_name': data[0]['name']}

    async def get_weather_for_recent_cities_async(self):
        """
        Asynchronously gets weather for the 10 most recent cities.
        """
        
        tasks = [self.get_weather_async(city) for city in self.latest_cities]
        
        results = await asyncio.gather(*tasks)
        return results
        
    def delete(self):
        if self.parent is not None: 
            self.parent._delete(self)
        else:
            del self