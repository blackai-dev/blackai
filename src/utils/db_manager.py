# Directory: blackai/utils
# File: db_manager.py

import os
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://koxlkelwlkcappevkdcb.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"  # Replace with your actual Supabase anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def initialize_db():
    """Ensure the Supabase table exists (manual setup required on Supabase)."""
    print("Supabase database is ready. Ensure your table structure is set up.")

def insert_emotion_data(r, g, b, brightness, contrast, emotion):
    """Insert emotion data into the Supabase database."""
    data = {
        "R": r,
        "G": g,
        "B": b,
        "Brightness": brightness,
        "Contrast": contrast,
        "Emotion": emotion
    }
    response = supabase.table("emotions").insert(data).execute()
    if response.get("status_code") == 201:
        print("Emotion data inserted successfully!")
    else:
        print(f"Error inserting data: {response.get('error')}")

def fetch_emotion_data():
    """Fetch all emotion data from the Supabase database."""
    response = supabase.table("emotions").select("*").execute()
    if response.get("status_code") == 200:
        return response.get("data")
    else:
        print(f"Error fetching data: {response.get('error')}")
        return []


