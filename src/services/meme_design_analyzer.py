# Meme Design Analysis 
from sentiment_analysis import analyze_sentiment
from design_impact import analyze_design_elements
from prediction_model import predict_purchase_intent

class MemeDesignAnalyzer:
    def __init__(self, model, sentiment_model):
        self.model = model
        self.sentiment_model = sentiment_model

    def analyze_design(self, image_path, text):
        # Step 1: 
        design_data = analyze_design_elements(image_path)
        
        # Step 2: 
        sentiment_score = analyze_sentiment(text)
        
        # Step 3: 
        purchase_prediction = predict_purchase_intent(design_data, sentiment_score)
        
        return {
            "design_data": design_data,
            "sentiment_score": sentiment_score,
            "purchase_prediction": purchase_prediction
        }

# 
analyzer = MemeDesignAnalyzer(model="CLIP", sentiment_model="BERT")
results = analyzer.analyze_design("meme_coin.png", "FIGHT FIGHT FIGHT")
print(results)
