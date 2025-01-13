from utils.db_manager import initialize_db, insert_emotion_data, fetch_emotion_data
from utils.feature_extractor import extract_features
from api.blockchain_api import issue_token

def main():
    # Step 1: Initialize database
    initialize_db()

    # Step 2: Simulate image processing
    image_path = "test_image.jpg"
    features = extract_features(image_path)
    print(f"Extracted Features: {features}")

    # Step 3: Simulate emotion collection
    user_emotion = "happy"  # Placeholder for user input
    print(f"User Emotion: {user_emotion}")

    # Step 4: Store data in database
    insert_emotion_data(*features, user_emotion)
    print("Emotion data stored successfully!")

    # Step 5: Reward user with tokens
    user_wallet = "user_wallet_address"  # Placeholder wallet address
    token_reward = 10  # Reward amount
    blockchain_response = issue_token(user_wallet, token_reward)
    print(f"Blockchain Response: {blockchain_response}")

    # Step 6: Display stored data
    data = fetch_emotion_data()
    print(f"Stored Data:\n{data}")

if __name__ == "__main__":
    main()

