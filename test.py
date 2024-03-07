from rswg_weather_sdk import Apis
import json as j

#correct key
api=Apis().get_api("4219ff37a155ea4305cd9cefc916c336")

print(api.get_weather('nyc'))
#incorrect key
#api=Api("228148291")