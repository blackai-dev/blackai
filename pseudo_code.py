import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import cv2
import os
import joblib
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb

# Function to extract enhanced features from the image
def extract_features(image_path):
    """
    Extract enhanced features from an image, including:
    - RGB mean
    - HSV mean
    - Brightness and Contrast
    """
    image = Image.open(image_path).resize((50, 50))
    pixels = np.array(image).reshape(-1, 3)
    rgb_mean = np.mean(pixels, axis=0)  # RGB mean

    # Convert to HSV and calculate HSV mean
    hsv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
    hsv_pixels = hsv_image.reshape(-1, 3)
    hsv_mean = np.mean(hsv_pixels, axis=0)  # HSV mean

    # Brightness and Contrast
    grayscale = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    brightness = np.mean(grayscale)
    contrast = np.std(grayscale)

    return np.concatenate((rgb_mean, hsv_mean, [brightness, contrast]))

# Update dataset with enhanced features
def update_dataset(features, user_emotion, data_file="emotion_data.csv"):
    if not os.path.exists(data_file):
        columns = ['R', 'G', 'B', 'H', 'S', 'V', 'Brightness', 'Contrast', 'Emotion']
        df = pd.DataFrame(columns=columns)
        df.to_csv(data_file, index=False)

    df = pd.read_csv(data_file)
    new_entry = dict(zip(df.columns[:-1], features), Emotion=user_emotion)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(data_file, index=False)
    return df

# Train a LightGBM model
def train_model(data_file="emotion_data.csv", model_file="enhanced_emotion_model.pkl"):
    df = pd.read_csv(data_file)
    if len(df) <= 10:
        print("Not enough data to train the model. Add more samples.")
        return None

    df['Emotion_Label'] = df['Emotion'].astype('category').cat.codes
    X = df.drop(['Emotion', 'Emotion_Label'], axis=1)
    y = df['Emotion_Label']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = lgb.LGBMClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Enhanced Model Accuracy:", accuracy)
    print(classification_report(y_test, y_pred, target_names=df['Emotion'].unique()))

    # Save model and scaler
    joblib.dump({'model': model, 'scaler': scaler}, model_file)
    print(f"Model and scaler saved to {model_file}.")
    return model

# Predict emotion with enhanced features
def predict_emotion(image_path, model_file="enhanced_emotion_model.pkl"):
    if not os.path.exists(model_file):
        print("No trained model found. Train the model first.")
        return None

    model_data = joblib.load(model_file)
    model, scaler = model_data['model'], model_data['scaler']

    features = extract_features(image_path).reshape(1, -1)
    scaled_features = scaler.transform(features)
    predicted_label = model.predict(scaled_features)[0]

    # Load dataset to map label back to emotion
    df = pd.read_csv("emotion_data.csv")
    emotion_categories = df['Emotion'].astype('category').cat.categories
    return emotion_categories[predicted_label]

# Visualize enhanced emotion distribution
def visualize_emotion_distribution(data_file="emotion_data.csv"):
    df = pd.read_csv(data_file)
    sns.set(style="whitegrid")
    sns.barplot(x=df['Emotion'].value_counts().index, y=df['Emotion'].value_counts().values)
    plt.title("Enhanced Emotion Distribution")
    plt.xlabel("Emotions")
    plt.ylabel("Frequency")
    plt.show()

# Main Workflow
image_path = "captured_image.jpg"
capture_image(image_path)  # Mock capturing an image
features = extract_features(image_path)
print("Extracted Features:", features)

user_emotion = collect_user_emotion()
print("User Emotion:", user_emotion)

df = update_dataset(features, user_emotion)
print("Dataset updated.")

model = train_model()

predicted_emotion = predict_emotion(image_path)
if predicted_emotion:
    print("Predicted Emotion:", predicted_emotion)

visualize_emotion_distribution()

