import pytest
from .api import Api, Apis
from .resources import asyncio

VALID_KEY='4219ff37a155ea4305cd9cefc916c336'
INVALID_KEY='oguzok'

class TestApis:
    
    # create a new instance of Api with a valid api_key
    def test_valid_api_key(self):
        apis = Apis()
        api_key = VALID_KEY
        api = apis.get_api(api_key)
        assert isinstance(api, Api)

    # create a new instance of Api with an invalid api_key
    def test_invalid_api_key(self):
        apis = Apis()
        api_key = INVALID_KEY
        with pytest.raises(Exception):
            apis.get_api(api_key)

    # get_weather for a valid city
    def test_get_weather_valid_city(self):
        # Create an instance of Apis
        apis = Apis()

        # Generate a valid API key
        api_key = VALID_KEY

        # Create an instance of Api using the valid API key
        api = apis.get_api(api_key)

        # Call the get_weather method with a valid city
        city = "London"
        weather_data = api.get_weather(city)

        # Assert that the weather data is not empty
        assert weather_data is not None

        # Assert that the weather data contains the expected keys
        expected_keys = ["coord", "weather", "base", "main", "visibility", "wind", "clouds", "dt", "sys", "timezone", "id", "name", "cod"]
        assert all(key in weather_data for key in expected_keys)

    # get_weather_async for a valid city
    def test_get_weather_async_valid_city(self):
        apis = Apis()
        api_key = VALID_KEY
        api = apis.get_api(api_key)
        city = "London"
        weather = asyncio.run(api.get_weather_async(city))
        assert isinstance(weather, dict)
        assert "name" in weather
        assert "weather" in weather
        assert "main" in weather
        assert "wind" in weather

    # get_weather_for_recent_cities_async for a valid Api instance with at least one recent city
    def test_get_weather_for_recent_cities_async_valid_api(self):
        # Create an instance of Apis
        apis = Apis()

        # Create a valid API key
        api_key = VALID_KEY

        # Get an API instance with the valid API key
        api = apis.get_api(api_key)

        # Add a recent city to the API instance
        api.latest_cities.append("London")

        # Call the get_weather_for_recent_cities_async method
        results = asyncio.run(api.get_weather_for_recent_cities_async())

        # Assert that the results are not empty
        assert results

        # Assert that the results contain weather data for the recent city
        assert any(result["name"] == "London" for result in results)

    # delete an Api instance
    def test_delete_api_instance(self):
        apis = Apis()
        api_key = VALID_KEY
        api = apis.get_api(api_key)
        assert isinstance(api, Api)
        api.delete()
        assert api_key not in apis.keys

    # get_weather for an invalid city
    def test_get_weather_invalid_city(self):
        apis = Apis()
        api_key = VALID_KEY
        api = apis.get_api(api_key)
    
        with pytest.raises(Exception):
            api.get_weather("invalid_city")

    # get_weather_async for an invalid city
    def test_get_weather_async_invalid_city(self):
        apis = Apis()
        api_key = VALID_KEY
        api = apis.get_api(api_key)
    
        with pytest.raises(Exception):
            asyncio.run(api.get_weather_async("invalid_city"))

    # get_weather_for_recent_cities_async for an Api instance with no recent cities
    def test_get_weather_for_recent_cities_async_no_recent_cities(self):
        # Create an instance of Apis
        apis = Apis()

        # Create a new Api instance with a valid API key
        api_key = VALID_KEY
        api = apis.get_api(api_key)

        # Call get_weather_for_recent_cities_async on the Api instance
        results = asyncio.run(api.get_weather_for_recent_cities_async())

        # Assert that the results list is empty
        assert len(results) == 0