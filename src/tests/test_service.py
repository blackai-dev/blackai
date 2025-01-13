import unittest
from services.emotion_service import EmotionService

class TestEmotionService(unittest.TestCase):
    def setUp(self):
        self.service = EmotionService()

    def test_add_emotion_record(self):
        features = [128.0, 128.0, 128.0, 128.0, 0.0]
        emotion = "happy"
        self.service.add_emotion_record(features, emotion)
        print("Emotion record added successfully.")

    def test_predict_emotion(self):
        features = [128.0, 128.0, 128.0, 128.0, 0.0]
        predicted_emotion = self.service.predict_emotion(features)
        print(f"Predicted emotion: {predicted_emotion}")

if __name__ == "__main__":
    unittest.main()

