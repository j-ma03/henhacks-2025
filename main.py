import gemini_api
import features
import route

# create gemini api object
# create overpass api object
# define latitude and longitude
# define prompt

start_latitude, start_longitude = map(float, input("Enter the start latitude and longitude separated by spaces: ").split())
destination_latitude, destination_longitude = map(float, input("Enter the destination latitude and longitude separated by spaces: ").split())
prompt = input("Enter your prompt: ")

gemini = gemini_api.GeminiAPI("AIzaSyBCGrr4M1xkbFjRuNFW3lR0y4NSAxnTy1A") # gets suggested tags from prompt
overpass = features.OverpassAPI() # gets nearby features from latitude and longitude
router = route.RouteAPI() # gets route between two points

suggested_tags = gemini.generate_suggestions(prompt) # gets suggested tags from prompt

# get route between two points
router_response = router.get_osrm_route(start_latitude, start_longitude, destination_latitude, destination_longitude)

nearby_features = overpass.get_and_format_nearby_features(latitude, longitude)

print("Suggested tags:")
print(suggested_tags)
print(suggested_tags.shape)
print("\nNearby features:")
print(nearby_features)
print(nearby_features.shape)
