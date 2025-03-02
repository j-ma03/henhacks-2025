import requests

class OverpassAPI:
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
            tags_str = ", ".join([f"{k}={v}" for k, v in tags.items()])
            formatted_features.append(f"{feature_type} #{feature_id} ({tags_str})")
        
        return formatted_features

# # Example usage
# latitude = 39.328627
# longitude = -76.612188
# radius = 2  # Radius in meters

# api = OverpassAPI(latitude, longitude, radius)
# features = api.get_nearby_features()
# formatted_features = api.format_features(features)

# print("Nearby features:")
# for feature in formatted_features:
#     print(feature)