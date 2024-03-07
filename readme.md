# installation:
1. install python 3.12.0
2. run pip install aiohttp asyncio requests json
3. put folder rswg_weather_sdk in root of your project
4. see example usage
## run tests:
~
python -m pytest -s
~
## example usage:
~
from rswg_weather_sdk import Apis
import json as j
import asyncio
api=Apis().get_api("YOUR KEY")
print(api.get_weather('nyc'))
___OR___
async def main():
    recent_cities_weather = await api.get_weather_for_recent_cities_async()
    print(j.dumps(recent_cities_weather, ensure_ascii=False, indent=1))
asyncio.run(main())
~
# task:
see document backend sdk task.pdf