import pandas as pd
from typing import List, Dict, Any

class IngestionAgent:
    def __init__(self, data_source: str):
        self.data_source = data_source
        self.data = pd.DataFrame()
        
    def ingest_data(self) -> pd.DataFrame:
        """
        Loads data from the source (CSV or API simulation).
        For Phase 1, we load the CSV.
        """
        try:
            self.data = pd.read_csv(self.data_source)
            # Ensure timestamp is datetime
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            print(f"[IngestionAgent] Successfully loaded {len(self.data)} records from {self.data_source}")
            return self.data
        except Exception as e:
            print(f"[IngestionAgent] Error loading data: {e}")
            return pd.DataFrame()
            
    def stream_data(self) -> List[Dict[str, Any]]:
        """
        Simulates streaming by returning a list of dictionaries.
        """
        if self.data.empty:
            self.ingest_data()
        return self.data.to_dict('records')
