import unittest
from meme_design_analyzer import MemeDesignAnalyzer

class TestMemeAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MemeDesignAnalyzer(model="CLIP", sentiment_model="BERT")
    
    def test_analyze_design(self):
        result = self.analyzer.analyze_design("sample_image.png", "Fight for the future!")
        self.assertIn("purchase_prediction", result)
        self.assertGreaterEqual(result["purchase_prediction"], 0.0)
        self.assertLessEqual(result["purchase_prediction"], 1.0)

if __name__ == "__main__":
    unittest.main()
