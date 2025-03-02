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
