import re
from textblob import TextBlob
from typing import Dict, Any, List

class RiskAnalysisAgent:
    def __init__(self):
        self.panic_keywords = [
            "riot", "explosion", "attack", "curfew", "gunshot", "gunshots",
            "poison", "poisoned", "panic", "urgent", "bomb", "emergency"
        ]
        # To compute basic virality (count of recent similar posts), we would
        # track recent posts. For simplicity, we just count keywords in the current message
        # and we can be passed 'recent_messages' from orchestrator for virality.
        
    def analyze_post(self, post: Dict[str, Any], recent_posts: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyzes a single post for sentiment and panic keywords.
        Returns a dictionary with the analysis results.
        """
        text = post.get("text", "").lower()
        
        # 1. Keyword detection
        found_keywords = [kw for kw in self.panic_keywords if kw in text]
        keyword_score = len(found_keywords) / len(self.panic_keywords) if self.panic_keywords else 0
        
        # Normalize keyword score to 0-1 (cap at 1)
        keyword_score = min(keyword_score * 5, 1.0)
        
        # 2. Sentiment/Emotion analysis
        # TextBlob polarity goes from -1 (most negative) to 1 (most positive)
        # Fear/Anger are usually highly negative. Let's map negative polarity to a risk score (0-1).
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        emotion_score = 0.0
        if polarity < 0:
            emotion_score = abs(polarity)  # -1 -> 1.0 (highest emotion risk)
            
        # 3. Virality (Posts per time window)
        # simplified concept: how many posts have these keywords in recent history
        virality_score = 0.0
        if recent_posts and found_keywords:
            similar_post_count = 0
            for rp in recent_posts:
                if rp.get("id") != post.get("id"):
                    rp_text = rp.get("text", "").lower()
                    if any(kw in rp_text for kw in found_keywords):
                        similar_post_count += 1
            
            # Simple heuristic: 5 similar posts = max virality
            virality_score = min(similar_post_count / 5.0, 1.0)
            
        analysis = {
            "found_keywords": found_keywords,
            "keyword_score": keyword_score,
            "emotion_score": emotion_score,
            "virality_score": virality_score
        }
        
        return analysis
