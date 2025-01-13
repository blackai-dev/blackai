import unittest
from utils.db_manager import initialize_db, insert_emotion_data, fetch_emotion_data
from utils.feature_extractor import extract_features

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Initialize the database before each test."""
        initialize_db()

    def test_insert_and_fetch_data(self):
        """Test inserting and fetching data from the database."""
        insert_emotion_data(128.0, 128.0, 128.0, 128.0, 0.0, "happy")
        data = fetch_emotion_data()
        self.assertTrue(len(data) > 0, "No data was fetched from the database.")
        self.assertEqual(data[0][5], "happy", "Emotion data does not match.")

    def test_feature_extraction(self):
        """Test feature extraction from a sample image."""
        image_path = "test_image.jpg"
        features = extract_features(image_path)
        self.assertEqual(len(features), 5, "Feature extraction did not return the expected number of features.")
        self.assertIsInstance(features[0], float, "Extracted features are not of type float.")

if __name__ == "__main__":
    unittest.main()

