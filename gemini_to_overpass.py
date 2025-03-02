import gemini_api_test
import overpass_api_test

# create gemini api object
# create overpass api object
# define latitude and longitude
# define prompt

latitude, longitude = map(float, input("Enter the latitude and longitude separated by spaces: ").split())
prompt = input("Enter your prompt: ")

gemini = gemini_api_test.GeminiAPI("AIzaSyBCGrr4M1xkbFjRuNFW3lR0y4NSAxnTy1A")
overpass = overpass_api_test.OverpassAPI()

suggested_tags = gemini.generate_suggestions(prompt)
nearby_features = overpass.get_and_format_nearby_features(latitude, longitude)

print("Suggested tags:")
print(suggested_tags)
print("\nNearby features:")
print("\n".join(nearby_features))
