import pandas as pd
from typing import Dict, Any, List
from collections import Counter

class BotDetectionAgent:
    def __init__(self):
        self.bot_threshold = 0.6
        
    def detect_bot(self, post: Dict[str, Any], user_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Flags bot activity based on:
        1. Repeated content
        2. High posting frequency
        """
        if not user_history:
            return {"bot_probability": 0.0, "is_bot": False}
            
        username = post.get("username", "unknown")
        user_posts = [p for p in user_history if p.get("username") == username]
        
        if len(user_posts) < 2:
            return {"bot_probability": 0.0, "is_bot": False}
        
        # 1. Repeated content
        texts = [p.get("text", "") for p in user_posts]
        most_common_text, count = Counter(texts).most_common(1)[0]
        # If the user posts the exact same content mostly, it's an indicator
        repeated_content_score = count / len(user_posts)
        if len(user_posts) < 3 and repeated_content_score == 1.0:
            # Need more evidence for smaller history
            repeated_content_score = 0.5
            
        # 2. High posting frequency
        try:
            timestamps = [pd.to_datetime(p.get("timestamp")) for p in user_posts]
            timestamps.sort()
            time_diff = (timestamps[-1] - timestamps[0]).total_seconds()
            
            freq_score = 0.0
            if time_diff > 0:
                posts_per_second = len(user_posts) / time_diff
                # Assume 1 post per minute is suspicious for a human in a short burst
                freq_score = min(posts_per_second / (1/60.0), 1.0)
            elif len(user_posts) > 1 and time_diff == 0:
                # Same exact timestamp multiple posts = def bot
                freq_score = 1.0
        except Exception as e:
            freq_score = 0.0
            
        # Combine heuristics
        bot_probability = (repeated_content_score * 0.7) + (freq_score * 0.3)
        bot_probability = min(max(bot_probability, 0.0), 1.0)
        
        return {
            "bot_probability": bot_probability,
            "is_bot": bot_probability >= self.bot_threshold
        }
