from rswg_weather_sdk import Apis
import json as j
import asyncio

#correct key
api=Apis().get_api("4219ff37a155ea4305cd9cefc916c336")

print(api.get_weather('nyc'))
print(api.get_weather('chicago'))
print(api.get_weather('berlin'))
#incorrect key
#api=Api("228148291")
print(123)
async def main():
    recent_cities_weather = await api.get_weather_for_recent_cities_async()
    print(j.dumps(recent_cities_weather, ensure_ascii=False, indent=1))
    print(recent_cities_weather)

asyncio.run(main())