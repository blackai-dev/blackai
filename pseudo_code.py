import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from lightgbm import LGBMClassifier
from PIL import Image
import os

# Database setup
DB_FILE = "emotion_data.db"

def initialize_db():
    """Initialize the SQLite database and create table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            R REAL,
            G REAL,
            B REAL,
            Brightness REAL,
            Contrast REAL,
            Emotion TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_emotion_data(r, g, b, brightness, contrast, emotion):
    """Insert emotion data into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emotions (R, G, B, Brightness, Contrast, Emotion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (r, g, b, brightness, contrast, emotion))
    conn.commit()
    conn.close()

def fetch_emotion_data():
    """Fetch all emotion data from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT R, G, B, Brightness, Contrast, Emotion FROM emotions")
    data = cursor.fetchall()
    conn.close()
    return data

# Feature extraction
def capture_image(image_path="captured_image.jpg"):
    """Simulate capturing an image."""
    placeholder_image = np.ones((50, 50, 3), dtype=np.uint8) * 128
    Image.fromarray(placeholder_image).save(image_path)
    return image_path

def extract_features(image_path):
    """Extract features from an image."""
    image = Image.open(image_path)
    np_image = np.array(image)
    mean_rgb = np.mean(np_image, axis=(0, 1))  # Mean R, G, B
    brightness = np.mean(np.max(np_image / 255.0, axis=2)) * 255  # Brightness
    contrast = np.std(np_image)  # Contrast
    return np.hstack((mean_rgb, brightness, contrast))

# Simulated functions
def collect_user_emotion():
    """Simulate user selecting an emotion."""
    return "happy"

# Main workflow
initialize_db()  # Ensure the database is initialized

# Simulate capturing an image and extracting features
image_path = "test_image.jpg"
capture_image(image_path)
features = extract_features(image_path)
print(f"Extracted Features: {features}")

# Simulate collecting user emotion
user_emotion = collect_user_emotion()
print(f"User Emotion: {user_emotion}")

# Insert new data into the database
insert_emotion_data(*features, user_emotion)

# Fetch data from the database
data = fetch_emotion_data()
print(f"Fetched Data: {data}")

# Train a model if sufficient data is available
if len(data) > 1000:
    # Convert data to a DataFrame for easy manipulation
    import pandas as pd
    df = pd.DataFrame(data, columns=['R', 'G', 'B', 'Brightness', 'Contrast', 'Emotion'])
    df['Emotion_Label'] = df['Emotion'].astype('category').cat.codes

    X = df[['R', 'G', 'B', 'Brightness', 'Contrast']]
    y = df['Emotion_Label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LGBMClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Predict using the latest features
    predicted_label = model.predict([features[:-1]])[0]
    predicted_emotion = df['Emotion'].astype('category').cat.categories[predicted_label]
    print(f"Predicted Emotion: {predicted_emotion}")

