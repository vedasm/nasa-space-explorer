import requests
from datetime import date
import os

API_KEY = os.getenv("NASA_API_KEY")

def get_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_asteroids():
    today = date.today()
    url = (
        f"https://api.nasa.gov/neo/rest/v1/feed"
        f"?start_date={today}"
        f"&end_date={today}"
        f"&api_key={API_KEY}"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_epic_images(selected_date):

    url = (
        f"https://api.nasa.gov/EPIC/api/natural/date/"
        f"{selected_date}"
        f"?api_key={API_KEY}"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def search_images(query):

    url = (
        f"https://images-api.nasa.gov/search"
        f"?q={query}"
        f"&media_type=image"
    )
    response = requests.get(url)
    return response.json()


