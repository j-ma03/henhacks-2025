import requests
import numpy as np

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

# # Example usage
# latitude = 39.328627
# longitude = -76.612188
# radius = 2  # Radius in meters

# api = OverpassAPI(radius)
# features = api.get_and_format_nearby_features(latitude, longitude)

# print("Nearby features:")
# for feature in features:
#     print(feature)