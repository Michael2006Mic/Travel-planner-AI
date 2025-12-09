# -*- coding: utf-8 -*-
import os
import streamlit as st
import google.generativeai as genai

# --- Gemini API Setup ---
def configure_gemini_api():
    api_key = None
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        st.error("GEMINI_API_KEY not found. Please set it in your Streamlit secrets or environment variables.")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"An error occurred during Gemini API initialization: {e}")
        return False

# --- Gemini Travel Recommendation ---
def generate_travel_recommendation(location=None, destination_type=None, interests=None, budget_range=None, travel_companions=None, duration=None, time_of_year=None):
    prompt = f"""
    Generate a personalized travel recommendation for {location or 'any location'} based on these preferences:
    - Destination Type: {destination_type or 'Any'}
    - Interests: {interests or 'General'}
    - Budget: {budget_range or 'Any'}
    - Traveling With: {travel_companions or 'Any'}
    - Trip Duration: {duration or 'Not specified'}
    - Time of Year: {time_of_year or 'Not specified'}
    Please provide a detailed and engaging travel plan. Suggest a specific city or region.
    Include recommendations for:
    1. **Accommodation:** Suggest a type of place to stay (e.g., boutique hotel, budget hostel, luxury resort) that fits the budget.
    2. **Activities:** A brief, day-by-day itinerary or a list of 3-5 key activities and sights that match the user's interests.
    3. **Food:** Mention 1-2 local dishes or types of restaurants to try.
    4. **Why this destination?** Briefly explain why this location is a great fit for the user's preferences.
    Format the output using Markdown for readability. Use headings, bold text, bullet points, and sprinkle in some fun emojis.
    """
    try:
        model = genai.GenerativeModel('models/gemini-2.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating the recommendation: {e}")
        return "Sorry, I couldn't generate a recommendation at this time. Please try again."

def display_recommendations(recommendation_text):
    st.subheader("Your Personalized Travel Recommendation! ✈️🌟")
    st.markdown(recommendation_text)

# --- Streamlit App Layout ---
st.set_page_config(layout="wide")
st.title("AI Travel Recommendation System 🤖✈️🌴")
st.markdown("Get personalized travel recommendations powered by Gemini AI. Fill out the form below to get started! 🚀")

if configure_gemini_api():
    st.header("Your Travel Preferences 🧳")

    # Improved Location Input
    popular_locations = ["Paris", "Tokyo", "Sydney", "New York", "London", "Other"]
    location_choice = st.selectbox("🌍 Choose your destination:", popular_locations)
    if location_choice == "Other":
        location = st.text_input(
            "Enter your destination (City or Region)",
            placeholder="e.g., Chennai, Cape Town, Rio de Janeiro"
        )
    else:
        location = location_choice

    col1, col2 = st.columns(2)
    with col1:
        destination_type = st.selectbox(
            "🏞️ What type of destination are you interested in?",
            ["Any", "City", "Beach", "Mountains", "Rural", "Adventure", "Historical", "Relaxation"]
        )
        interests = st.multiselect(
            "🎯 What are your interests?",
            ["History", "Adventure", "Relaxation", "Food", "Art", "Nature", "Nightlife", "Shopping"]
        )
        budget_range = st.select_slider(
            "💸 What is your budget range?",
            options=["Budget", "Mid-range", "Luxury"]
        )
    with col2:
        travel_companions = st.selectbox(
            "👫 Who are you traveling with?",
            ["Any", "Solo", "Family", "Couple", "Friends"]
        )
        duration = st.text_input(
            "⏳ How long do you plan to travel? (e.g., 7 days, 1 week)"
        )
        time_of_year = st.text_input(
            "📅 When do you plan to travel? (e.g., June, Summer, Winter)"
        )

    # Button to trigger recommendation generation
    if st.button("Get Recommendations 🎉"):
        selected_destination_type = destination_type if destination_type != "Any" else None
        selected_travel_companions = travel_companions if travel_companions != "Any" else None
        formatted_interests = ", ".join(interests) if interests else None
        with st.spinner("✨ Generating your personalized itinerary..."):
            recommendations = generate_travel_recommendation(
                location=location or None,
                destination_type=selected_destination_type,
                interests=formatted_interests,
                budget_range=budget_range,
                travel_companions=selected_travel_companions,
                duration=duration or None,
                time_of_year=time_of_year or None
            )
        display_recommendations(recommendations)
else:
    st.warning("Gemini API is not configured. Please provide your API key to continue.")