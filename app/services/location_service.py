"""Location service for detecting user location"""
import requests
import json


class LocationService:
    def __init__(self):
        self.api_url = "http://ip-api.com/json/"

    def get_location_info(self):
        """Get user location information"""
        try:
            response = requests.get(self.api_url, timeout=5)
            data = response.json()

            return {
                'ip': data.get('query', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'region': data.get('regionName', 'Unknown'),
                'timezone': data.get('timezone', 'Unknown'),
                'lat': data.get('lat'),
                'lon': data.get('lon')
            }
        except Exception as e:
            print(f"❌ Location detection error: {e}")
            return {
                'ip': 'Unknown',
                'country': 'Unknown',
                'city': 'Unknown',
                'region': 'Unknown',
                'timezone': 'Unknown',
                'lat': None,
                'lon': None
            }