import spacy
from typing import Dict, Any

class GeoTaggingAgent:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            print("Downloading spacy model...")
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
            
    def geotag_post(self, post: Dict[str, Any]) -> str:
        """
        Extracts location from the provided text using spacy NER.
        If location not found, fallback to 'provided_location' if available.
        """
        text = post.get("text", "")
        doc = self.nlp(text)
        
        # Look for Geopolitical Entities or Locations
        locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC"]]
        
        if locations:
            return locations[0] # Return first found location
            
        # Fallback to provided location
        provided_loc = post.get("provided_location")
        if provided_loc and provided_loc != "None":
            return provided_loc
            
        return "Unknown"
