from .ingestion_agent import IngestionAgent
from .risk_analysis_agent import RiskAnalysisAgent
from .risk_scoring_agent import RiskScoringAgent
from .bot_detection_agent import BotDetectionAgent
from .geo_tagging_agent import GeoTaggingAgent
from .counter_messaging_agent import CounterMessagingAgent
from typing import List, Dict, Any

class OrchestratorAgent:
    def __init__(self, data_source: str):
        self.ingestion = IngestionAgent(data_source)
        self.analyzer = RiskAnalysisAgent()
        self.scorer = RiskScoringAgent()
        self.bot_detector = BotDetectionAgent()
        self.geo_tagger = GeoTaggingAgent()
        self.messenger = CounterMessagingAgent()
        
        self.post_history = []
        
    def process_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a single post through all agents.
        """
        # 1. Geo Tagging
        location = self.geo_tagger.geotag_post(post)
        post["extracted_location"] = location
        
        # 2. Bot Detection
        bot_info = self.bot_detector.detect_bot(post, self.post_history)
        
        # 3. Risk Analysis
        # Pass recent history (e.g., last 50 posts) down to analyze virality
        recent_history = self.post_history[-50:] if self.post_history else []
        analysis = self.analyzer.analyze_post(post, recent_history)
        
        # 4. Risk Scoring
        score_info = self.scorer.calculate_score(analysis)
        
        # 5. Counter Messaging
        # Generate PSA templates for High/Medium risk
        psa_en = ""
        psa_hi = ""
        if score_info["label"] in ["HIGH", "MEDIUM"]:
            psa_en = self.messenger.generate_psa(analysis, "en")
            psa_hi = self.messenger.generate_psa(analysis, "hi")
            
        # Compile Final Result
        result = {
            **post,
            "location": location,
            **bot_info,
            **analysis,
            **score_info,
            "psa_en": psa_en,
            "psa_hi": psa_hi
        }
        
        # Bonus: Basic Explainability
        explanations = []
        if analysis["found_keywords"]:
            explanations.append(f"Keywords: {', '.join(analysis['found_keywords'])}")
        if analysis["emotion_score"] > 0.3:
            explanations.append("Negative sentiment detected")
        if analysis["virality_score"] > 0.0:
            explanations.append("Trending panic topic")
        if bot_info["is_bot"]:
            explanations.append(f"Bot-like behavior (prob={bot_info['bot_probability']:.2f})")
            
        result["explanation"] = " | ".join(explanations) if explanations else "Normal activity"
        
        self.post_history.append(post)
        return result

    def run_pipeline(self) -> List[Dict[str, Any]]:
        """
        Coordinates all agents to process the data stream end-to-end.
        """
        raw_stream = self.ingestion.stream_data()
        processed_data = []
        
        for post in raw_stream:
            result = self.process_post(post)
            processed_data.append(result)
            
        return processed_data
