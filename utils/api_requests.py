import requests
import json

# Send a GET request
def send_get_request(url, params=None):
    """
    Send a GET request to the given URL with optional parameters.
    """
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("GET request successful.")
            return response.json()  # Return JSON data if available
        else:
            print(f"GET request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error in GET request: {e}")
        return None

# Send a POST request
def send_post_request(url, data):
    """
    Send a POST request to the given URL with
