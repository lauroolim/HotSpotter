from django.conf import settings
import requests
import json

class Directions:
    def __init__(self, lat_a, long_a, lat_b, long_b):
        self.origin = f'{lat_a},{long_a}'
        self.destination = f'{lat_b},{long_b}'
        self.api_key = settings.GOOGLE_API_KEY
        self.directions = self._get_directions()

    def _get_directions(self):
        result = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?',
            params={
                'origin': self.origin,
                'destination': self.destination,
                'key': self.api_key
            }
        )
        return result.json()

    def get_route_info(self):
        if self.directions["status"] == "OK":
            route = self.directions["routes"][0]["legs"][0]
            origin = route["start_address"]
            destination = route["end_address"]
            distance = route["distance"]["text"]
            duration = route["duration"]["text"]

            steps = [
                [
                    s["distance"]["text"],
                    s["duration"]["text"],
                    s["html_instructions"],
                ]
                for s in route["steps"]
            ]

            return {
                "origin": origin,
                "destination": destination,
                "distance": distance,
                "duration": duration,
                "steps": steps
            }
        else:
            return None
