from typing import Dict, Any

class RiskScoringAgent:
    def __init__(self):
        # Weights for different components
        self.weights = {
            "keyword_score": 0.4,
            "emotion_score": 0.3,
            "virality_score": 0.3
        }
        
    def calculate_score(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combines scores linearly to produce a 0-100 risk score.
        Returns the numerical score and the risk category.
        """
        keyword_score = analysis.get("keyword_score", 0.0)
        emotion_score = analysis.get("emotion_score", 0.0)
        virality_score = analysis.get("virality_score", 0.0)
        
        # Weighted sum out of 1.0
        combined_score = (
            keyword_score * self.weights["keyword_score"] +
            emotion_score * self.weights["emotion_score"] +
            virality_score * self.weights["virality_score"]
        )
        
        # Convert to 0-100 scale
        final_score = int(combined_score * 100)
        final_score = min(max(final_score, 0), 100)
        
        # Determine label based on thresholds
        if final_score < 30:
            label = "LOW"
        elif final_score < 70:
            label = "MEDIUM"
        else:
            label = "HIGH"
            
        return {
            "score": final_score,
            "label": label
        }
