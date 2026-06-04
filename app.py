import streamlit as st
import requests
from nasa_api import get_apod, get_asteroids, get_epic_images, search_images
from datetime import date


st.set_page_config(
    page_title="NASA Space Explorer",
    page_icon="🌌"
)
st.title("🚀 NASA Space Explorer")

# Astronomy Picture of the Day
try:
    data = get_apod()
    st.header(data.get('title', 'Unknown Title'))
    if 'url' in data:
        st.image(data['url'])
    if 'explanation' in data:
        st.write(data["explanation"])
except requests.exceptions.RequestException as e:
    st.error(f"Failed to load Astronomy Picture of the Day. Could not connect to the NASA API or the API key is rate limited.\n\nError details: {e}")

# NeoWs (Near Earth Object Web Service)
st.title("Near Earth Asteroids")
today = str(date.today())

try:
    asteroid_data = get_asteroids()
    today_objects = asteroid_data.get("near_earth_objects", {}).get(today, [])
    st.subheader(f"Asteroids Today: {len(today_objects)}")
    for asteroid in today_objects:
        name = asteroid["name"]
        hazardous = asteroid["is_potentially_hazardous_asteroid"]
        diameter = asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"]
        miss_distance = asteroid["close_approach_data"][0]["miss_distance"]["kilometers"]
        st.subheader(name)
        if hazardous:
            st.error(f"**{name}** is potentially hazardous.  \n**Diameter:** {diameter} m  \n**Miss Distance**: {miss_distance} km", icon="⚠️")
        else:
            st.success(f"**{name}** is not hazardous.  \n**Diameter:** {diameter} m  \n**Miss Distance**: {miss_distance} km", icon="✅")
except Exception as e:
    st.error(f"Failed to load Near Earth Asteroids.\n\nError details: {e}")

st.divider()

# NASA Image Search
st.title("🔍 NASA Image Search")
search_term = st.text_input("Search NASA Images",placeholder="Moon, Saturn, Apollo...")
if st.button("Search"):
    results = search_images(search_term)
    items = results["collection"]["items"]
    items = items[:10]
    for item in items:
        title = item["data"][0]["title"]
        image_url = item["links"][0]["href"]
        st.subheader(title)
        st.image(image_url)
st.divider()

# Earth From Space (EPIC)

st.title("🌍 Earth From Space")

selected_date = st.date_input(
    "Choose a date"
)

date_string = selected_date.strftime(
    "%Y-%m-%d"
)

if st.button("Show Earth Images"):

    try:
        images = get_epic_images(date_string)

        if not images:
            st.warning(
                "No images available for this date."
            )

        else:

            year = date_string[0:4]
            month = date_string[5:7]
            day = date_string[8:10]

            for image_data in images:

                image_name = image_data["image"]

                image_url = (
                    f"https://epic.gsfc.nasa.gov/archive/"
                    f"natural/{year}/{month}/{day}"
                    f"/png/{image_name}.png"
                )

                st.image(
                    image_url,
                    caption=image_name
                )
                break
    except Exception as e:
        st.error(f"Failed to fetch EPIC images.\n\nError details: {e}")
