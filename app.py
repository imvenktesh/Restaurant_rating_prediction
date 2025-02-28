import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the trained model
with open("restaurant_rating_model.pkl", "rb") as file:
    model = pickle.load(file)

# Country Mapping Dictionary
country_mapping = {
    1: "India", 216: "Brazil", 215: "United States", 30: "Australia", 214: "Canada",
    189: "South Africa", 148: "New Zealand", 208: "Turkey", 14: "United Arab Emirates",
    162: "Indonesia", 94: "Qatar", 184: "Singapore", 166: "Malaysia",
    191: "Philippines", 37: "United Kingdom"
}

# Rating Color Mapping
rating_color_mapping = {
    "Dark Green": 0, "Green": 1, "Yellow": 2, 
}

# Rating Text Mapping
rating_text_mapping = {
    "Excellent": 0, "Good": 1,"Very Good": 2,
}

# City encoding dictionary
city_encoding = {
    "New Delhi": 0, "Gurgaon": 1, "Noida": 2, "Faridabad": 3, "Ghaziabad": 4, "Bhubaneshwar": 5,
    "Amritsar": 6, "Ahmedabad": 7, "Lucknow": 8, "Guwahati": 9, "Ludhiana": 10, "Kochi": 11,
    "Kolkata": 12, "Mumbai": 13, "Mangalore": 14, "Singapore": 15, "Orlando": 16, "Mysore": 17,
    "Nagpur": 18, "Nashik": 19, "Coimbatore": 20, "Dehradun": 21, "Tampa Bay": 22, "Jaipur": 23,
    "Patna": 24, "Pune": 25, "Cape Town": 26, "London": 27, "Manchester": 28, "Dubai": 29,
    "Bangalore": 30, "Goa": 31, "Bhopal": 32, "Chennai": 33, "Indore": 34, "Puducherry": 35,
    "Kanpur": 36, "Varanasi": 37, "Surat": 38, "Vadodara": 39, "Vizag": 40, "Hyderabad": 41,
    "Chandigarh": 42, "Jakarta": 43, "Istanbul": 44, "Johannesburg": 45, "Taguig City": 46,
    "Mandaluyong City": 47, "Pasig City": 48, "Bogor": 49, "Secunderabad": 50, "Makati City": 51,
    "San Juan City": 52, "Santa Rosa": 53, "Colombo": 54, "Ankara": 55, "Doha": 56, "Ranchi": 57,
    "Wellington City": 58, "Auckland": 59, "Davao City": 60, "Birmingham": 61, "Edinburgh": 62,
    "Brasilia": 63, "Rio de Janeiro": 64, "São Paulo": 65, "Pretoria": 66, "Athens": 67,
    "Dublin": 68, "Toronto": 69, "Vancouver": 70, "Paris": 71, "Berlin": 72, "Madrid": 73,
    "Rome": 74, "Milan": 75, "Vienna": 76, "Copenhagen": 77, "Brussels": 78, "Oslo": 79,
    "Stockholm": 80, "Helsinki": 81, "Seoul": 82, "Bangkok": 83, "Manila": 84, "Hanoi": 85,
    "Kuala Lumpur": 86, "Beijing": 87, "Shanghai": 88, "Hong Kong": 89, "Taipei": 90, "Mexico City": 91,
    "Buenos Aires": 92, "Santiago": 93, "Lima": 94, "Bogotá": 95, "São Luís": 96, "Cartagena": 97,
    "Quito": 98, "Montevideo": 99, "Havana": 100, "San José": 101, "Panama City": 102, "Caracas": 103,
    "Tehran": 104, "Baghdad": 105, "Riyadh": 106, "Jeddah": 107, "Damascus": 108, "Amman": 109,
    "Kuwait City": 110, "Muscat": 111, "Nairobi": 112, "Accra": 113, "Cape Coast": 114, "Lagos": 115,
    "Abuja": 116, "Dakar": 117, "Casablanca": 118, "Marrakech": 119, "Cairo": 120, "Alexandria": 121,
    "Tunis": 122, "Algiers": 123, "Khartoum": 124, "Addis Ababa": 125, "Luanda": 126, "Harare": 127,
    "Maputo": 128, "Gaborone": 129, "Windhoek": 130, "Lilongwe": 131, "Kampala": 132, "Dar es Salaam": 133,
    "Lusaka": 134, "Port Louis": 135, "Victoria": 136, "Antananarivo": 137, "Nouakchott": 138, "Freetown": 139,
    "Monrovia": 140, "Banjul": 141
}

# Title of the app
st.title("🍽️ Restaurant Rating Predictor")

# Two-column layout for inputs
col1, col2 = st.columns(2)

with col1:
    selected_city = st.selectbox("🏙️ Select City", list(city_encoding.keys()))
    encoded_city = city_encoding[selected_city]

    country_code = st.selectbox("🌎 Country Code", list(country_mapping.keys()), format_func=lambda x: country_mapping[x])
    price_range = st.selectbox("💲 Price Range", [1, 2, 3, 4])
    rating_color = st.selectbox("🎨 Rating Color", list(rating_color_mapping.keys()))
    rating_text = st.selectbox("🔤 Rating Text", list(rating_text_mapping.keys()))

with col2:
    avg_cost = st.number_input("💰 Average Cost for Two", min_value=500, step=50)
    has_table_booking = st.radio("📅 Has Dine-In?", ["Yes", "No"])
    has_online_delivery = st.radio("📦 Has Delivery?", ["Yes", "No"])
    is_delivering_now = st.radio("🚴‍♂️ Is Delivering Now?", ["Yes", "No"])
    votes = st.number_input("🗳️ No.of ratings", min_value=0, step=1)

# Convert categorical inputs into numerical values
has_table_booking = 1 if has_table_booking == "Yes" else 0
has_online_delivery = 1 if has_online_delivery == "Yes" else 0
is_delivering_now = 1 if is_delivering_now == "Yes" else 0
rating_color_value = rating_color_mapping[rating_color]
rating_text_value = rating_text_mapping[rating_text]

input_data = np.array([[encoded_city, country_code, avg_cost, has_table_booking,
                        has_online_delivery, is_delivering_now,price_range,
                        rating_color_mapping.get(rating_color, 0),  # Extract single value
                        rating_text_mapping.get(rating_text, 0),  # Extract single value
                        votes]])



# Prediction Button
if st.button("🔮 Predict Rating"):
    prediction = model.predict(input_data)[0]

    # Display Results
    st.success(f"📊 Predicted Restaurant Rating: {prediction:.2f}")
    st.info(f"🌍 Country: {country_mapping.get(country_code, 'Unknown')}")
    st.info(f"🎨 Rating Color: {rating_color}")
    st.info(f"🔤 Rating Text: {rating_text}")
