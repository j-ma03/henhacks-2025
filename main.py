import gemini_api
import features
import route
import requests
import numpy as np
import random

class OverpassAPI:
    """
    get nearby features in a 2m radius given a latitude and longitude

    args:
        - radius: int: radius in meters

    methods:
        - get_and_format_nearby_features: list: get nearby features in a 2m radius given a 
          latitude and longitude
    """
    def __init__(self, radius=2):
        self.radius = radius
        self.overpass_url = "http://overpass-api.de/api/interpreter"

    def get_and_format_nearby_features(self, lat, lon):
        overpass_query = f"""
        [out:json];
        (
          node(around:{self.radius},{lat},{lon});
          way(around:{self.radius},{lat},{lon});
        );
        out body;
        """
        response = requests.get(self.overpass_url, params={'data': overpass_query})
        data = response.json()
        
        formatted_features = []
        for element in data['elements']:
            if element['type'] == 'node':
                feature_type = "Node"
            elif element['type'] == 'way':
                feature_type = "Way"
            
            feature_id = element['id']
            tags = element.get('tags', {})
            for k, v in tags.items():
                formatted_features.append(f"{k}={v}")
        
        # return formatted_features
        return np.array(formatted_features)


# create gemini api object
# create overpass api object
# define latitude and longitude
# define prompt

start_latitude, start_longitude = map(float, input("Enter the start latitude and longitude separated by spaces: ").split())
destination_latitude, destination_longitude = map(float, input("Enter the destination latitude and longitude separated by spaces: ").split())
prompt = input("Enter your prompt: ")

gemini = gemini_api.GeminiAPI("AIzaSyBCGrr4M1xkbFjRuNFW3lR0y4NSAxnTy1A") # gets suggested tags from prompt
overpass = OverpassAPI(radius=2) # gets nearby features from latitude and longitude
router = route.RouteAPI() # gets route between two points

suggested_tags = gemini.generate_suggestions(prompt) # gets suggested tags from prompt

# get route between two points
route1 = router.get_osrm_route(start_latitude, start_longitude, destination_latitude, destination_longitude)
sampled_coords1 = router.get_sampled_coords(route1)

# define 2 random points between the start and destination points to create alternate routes
def generate_random_point(center_lat, center_lon, radius):
    # Convert radius from meters to degrees
    radius_in_degrees = radius / 111320

    # Generate random angle and distance
    angle = random.uniform(0, 2 * np.pi)
    distance = random.uniform(0, radius_in_degrees)

    # Calculate new latitude and longitude
    new_lat = center_lat + (distance * np.cos(angle))
    new_lon = center_lon + (distance * np.sin(angle)) / np.cos(np.radians(center_lat))

    return new_lat, new_lon

# Calculate the center point between start and destination
center_latitude = (start_latitude + destination_latitude) / 2
center_longitude = (start_longitude + destination_longitude) / 2

# Calculate the distance between start and destination in meters
distance = np.sqrt((start_latitude - destination_latitude)**2 + (start_longitude - destination_longitude)**2) * 111320

# Generate two random points within the circle
random_point1 = generate_random_point(center_latitude, center_longitude, distance / 2)
random_point2 = generate_random_point(center_latitude, center_longitude, distance / 2)

# get alternate route 1
route2 = router.get_osrm_route(start_latitude, start_longitude, random_point1[0], random_point1[1])
sampled_coords2 = router.get_sampled_coords(route2)
route2 = router.get_osrm_route(random_point1[0], random_point1[1], destination_latitude, destination_longitude)
sampled_coords2 = router.get_sampled_coords(route2)
sampled_coords2 = np.concatenate((sampled_coords1, sampled_coords2))

# get alternate route 2
route3 = router.get_osrm_route(start_latitude, start_longitude, random_point2[0], random_point2[1])
sampled_coords3 = router.get_sampled_coords(route3)
route3 = router.get_osrm_route(random_point2[0], random_point2[1], destination_latitude, destination_longitude)
sampled_coords3 = router.get_sampled_coords(route3)
sampled_coords3 = np.concatenate((sampled_coords3, sampled_coords2))

score1 = 0
score2 = 0
score3 = 0

for coord in sampled_coords1:
    nearby_features = overpass.get_and_format_nearby_features(coord[1], coord[0])
    for feature in nearby_features:
        for tag in suggested_tags:
            if feature.find(tag) != -1:
                score1 += 1

for coord in sampled_coords2:
    nearby_features = overpass.get_and_format_nearby_features(coord[1], coord[0])
    for feature in nearby_features:
        for tag in suggested_tags:
            if feature.find(tag) != -1:
                score2 += 1

for coord in sampled_coords3:
    nearby_features = overpass.get_and_format_nearby_features(coord[1], coord[0])
    for feature in nearby_features:
        for tag in suggested_tags:
            if feature.find(tag) != -1:
                score3 += 1

print("Scores:")
print("Route 1:", score1)
print("Route 2:", score2)
print("Route 3:", score3)

print("The best route is:")
if score1 > score2 and score1 > score3:
    print("Route 1")
elif score2 > score1 and score2 > score3:
    print("Route 2")
else:
    print("Route 3")
# print(start_latitude, start_longitude)
# print(destination_latitude, destination_longitude)

# latitude = 39.328627
# longitude = -76.612188
# radius = 2  # Radius in meters

# api = features.OverpassAPI(radius=2)
# features = api.get_and_format_nearby_features(latitude, longitude)

# print("Nearby features:")
# for feature in features:
#     print(feature)

# print("Suggested tags:")
# print(suggested_tags)
# print(suggested_tags.shape)
# print("\nNearby features:")
# print(nearby_features)
# print(nearby_features.shape)
