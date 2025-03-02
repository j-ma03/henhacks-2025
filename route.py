import requests
import numpy as np

class RouteAPI:
    """
    get route between two points given their latitude and longitude

    methods:
    - get_osrm_route: dict: get route between two points using OSRM
    - get_sampled_coords: np.array: get sampled coordinates from the route
    """
    def __init__(self):
        pass

    def get_osrm_route(self, start_lat, start_lon, end_lat, end_lon):
        """
        get route between two points using OSRM

        args:
        - start_lat: float: latitude of the starting point
        - start_lon: float: longitude of the starting point
        - end_lat: float: latitude of the ending point
        - end_lon: float: longitude of the ending point

        return:
        - dict: route between the two points
        """
        osrm_url = "http://router.project-osrm.org/route/v1/driving/"
        coordinates = f"{start_lon},{start_lat};{end_lon},{end_lat}"
        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "true"
        }
        response = requests.get(osrm_url + coordinates, params=params)
        return response.json()

    def get_sampled_coords(self, route):
        """
        get sampled coordinates from the route

        args:
        - route: dict: route between two points

        return:
        - np.array: sampled coordinates from the route
        """
        sampled_coords = []

        if route and "routes" in route:
            for step in route["routes"][0]["legs"][0]["steps"]:
                start_coord = step['geometry']['coordinates'][0]
                end_coord = step['geometry']['coordinates'][-1]
                middle_coord = step['geometry']['coordinates'][len(step['geometry']['coordinates']) // 2] if len(step['geometry']['coordinates']) > 2 else None
                if start_coord:
                    sampled_coords.append(start_coord)
                if end_coord:
                    sampled_coords.append(end_coord)
                if middle_coord:
                    sampled_coords.append(middle_coord)
        else:
            print("No route found.")

        return np.array(sampled_coords)

if __name__ == "__main__":
    start_lat = 39.328518
    start_lon = -76.612188
    end_lat = 39.328596
    end_lon = -76.634209


    # # Replace with your GraphHopper API key
    # graphhopper_api_key = "YOUR_GRAPHHOPPER_API_KEY"
    # # Replace with your Mapbox access token
    # mapbox_access_token = "YOUR_MAPBOX_ACCESS_TOKEN"
    route = RouteAPI()

    osrm_route = route.get_osrm_route(start_lat, start_lon, end_lat, end_lon)
    # print(osrm_route)

    # graphhopper_route = get_graphhopper_route(start_lat, start_lon, end_lat, end_lon, graphhopper_api_key)
    # mapbox_route = get_mapbox_route(start_lat, start_lon, end_lat, end_lon, mapbox_access_token)

    sampled_coords = route.get_sampled_coords(osrm_route)
    print("Sampled Coordinates:")
    print(sampled_coords)

    # print("\nGraphHopper Route:")
    # if graphhopper_route and "paths" in graphhopper_route:
    #     for instruction in graphhopper_route["paths"][0]["instructions"]:
    #         print(f"{instruction['text']} for {instruction['distance']} meters")
    # else:
    #     print("No route found.")

    # print("\nMapbox Route:")
    # if mapbox_route and "routes" in mapbox_route:
    #     for step in mapbox_route["routes"][0]["legs"][0]["steps"]:
    #         print(f"{step['maneuver']['instruction']} to {step['name']}")
    # else:
    #     print("No route found.")