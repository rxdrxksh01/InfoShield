from typing import Dict, Any

class CounterMessagingAgent:
    def __init__(self):
        self.templates_en = {
            "riot": "We are aware of reports regarding unrest. Local authorities are managing the situation. Please stay safe and avoid the area.",
            "explosion": "Emergency services are responding to reports of an incident. Please remain calm and clear of the affected zone for your safety.",
            "curfew": "Please verify any curfew information with official local government channels before altering your plans.",
            "attack": "Law enforcement is active in the area responding to incident reports. Follow official guidance and find a safe location.",
            "poison": "Do not panic. Await official environmental safety updates before assuming water or resources are unsafe.",
            "default": "We noticed rising concerns about this topic. Please rely on verified official sources for accurate information."
        }
        
        self.templates_hi = {
             "riot": "हमें अशांति की रिपोर्टों की जानकारी है। स्थानीय अधिकारी स्थिति को संभाल रहे हैं। कृपया सुरक्षित रहें और क्षेत्र से दूर रहें।",
             "explosion": "आपातकालीन सेवाएं एक घटना की रिपोर्ट पर प्रतिक्रिया दे रही हैं। कृपया अपनी सुरक्षा के लिए शांत रहें और प्रभावित क्षेत्र से दूर रहें।",
             "curfew": "अपनी योजनाओं को बदलने से पहले कृपया आधिकारिक स्थानीय सरकारी चैनलों से किसी भी कर्फ्यू की जानकारी को सत्यापित करें।",
             "attack": "पुलिस घटना की रिपोर्ट पर प्रतिक्रिया देने के लिए क्षेत्र में सक्रिय है। आधिकारिक मार्गदर्शन का पालन करें और सुरक्षित स्थान खोजें।",
             "poison": "घबराएं नहीं। पानी या संसाधनों को असुरक्षित मानने से पहले आधिकारिक पर्यावरण सुरक्षा अपडेट की प्रतीक्षा करें।",
             "default": "हमने इस विषय के बारे में बढ़ती चिंताओं पर ध्यान दिया है। कृपया सटीक जानकारी के लिए सत्यापित आधिकारिक स्रोतों पर भरोसा करें।"
        }
        
    def generate_psa(self, risk_analysis: Dict[str, Any], lang: str = "en") -> str:
        """
        Generates a calm, neutral, and informative Public Service Announcement 
        based on the detected high-risk keywords.
        """
        keywords = risk_analysis.get("found_keywords", [])
        templates = self.templates_en if lang == "en" else self.templates_hi
        
        if not keywords:
            return "" # No PSA needed
            
        # Prioritize matching a specific keyword
        for kw in keywords:
            if kw in templates:
                return templates[kw]
                
        # Fallback if keywords exist but don't match exactly in template map
        return templates["default"]
