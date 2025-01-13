import unittest
from models.emotion_model import EmotionModel

class TestEmotionModel(unittest.TestCase):
    def setUp(self):
        """Prepare mock data for testing the EmotionModel."""
        self.data = [
            [128.0, 128.0, 128.0, 128.0, 0.0, "happy"],
            [100.0, 120.0, 110.0, 125.0, 5.0, "sad"]
        ]
        self.model = EmotionModel()

    def test_training(self):
        """Test the training process of the EmotionModel."""
        self.model.train(self.data)
        self.assertIsNotNone(self.model.model, "Model was not trained successfully.")

    def test_prediction(self):
        """Test prediction with the trained model."""
        self.model.train(self.data)
        features = [128.0, 128.0, 128.0, 128.0, 0.0]
        result = self.model.predict(features)
        self.assertIsInstance(result, int, "Prediction did not return a valid label.")

if __name__ == "__main__":
    unittest.main()

