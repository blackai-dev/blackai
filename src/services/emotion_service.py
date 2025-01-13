from utils.db_manager import insert_emotion_data, fetch_emotion_data
from models.emotion_model import EmotionModel

class EmotionService:
    def __init__(self):
        self.model = EmotionModel()

    def add_emotion_record(self, features, emotion):
        """Add a new emotion record and train the model if necessary."""
        insert_emotion_data(*features, emotion)
        data = fetch_emotion_data()
        if len(data) > 10:
            self.model.train(data)

    def predict_emotion(self, features):
        """Predict emotion using the trained model."""
        return self.model.predict(features)

