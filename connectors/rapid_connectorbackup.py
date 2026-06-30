# connectors/manager.py

# 🌟 [REAL INTEGRATION]: నీ దగ్గర ఉన్న ఒరిజినల్ కీ ఫైల్ ని ఇక్కడ ఇంపోర్ట్ చేస్తున్నాం బ్రో!
try:
    from connectors.rapid_connector import RapidConnector # లేదా నీ ఫైల్ లోపల ఉన్న క్లాస్ పేరు బ్రో
except ImportError:
    RapidConnector = None

class ConnectorManager:
    def __init__(self):
        # నీ రియల్ కనెక్టర్ ని మన మేనేజర్ లిస్ట్‌లో యాడ్ చేస్తున్నాం బ్రో
        if RapidConnector:
            self.connectors = [RapidConnector()]
        else:
            self.connectors = []

    def search_all(self, keyword="", location=None):
        search_term = (keyword or "Python Developer").strip()
        loc_term = (location or "India").strip()
        
        print(f"🚀 [REAL-TIME LIVE MODE] Fetching Real Jobs using rapid_connector for: '{search_term}' in '{loc_term}'")
        
        # 🔗 నీ ఒరిజినల్ కనెక్టర్ ద్వారా లైవ్ ఇంటర్నెట్ నుండి రియల్ జాబ్స్ ని లాగుతున్నాం బ్రో
        if self.connectors:
            try:
                # నీ rapid_connector లో ఉన్న సెర్చ్ ఫంక్షన్ పేరు (ఉదాహరణకు search లేదా search_jobs) ఇక్కడ కాల్ చెయ్ బ్రో
                real_api_jobs = self.connectors[0].search_jobs(keyword=search_term, location=loc_term)
                if real_api_jobs:
                    return real_api_jobs
            except Exception as e:
                print(f"⚠️ Rapid Connector Fetch Error: {e}")
        
        # ఒకవేళ నీ కనెక్టర్ లో ఫంక్షన్ పేరు వేరే ఉంటే క్రాష్ అవ్వకుండా ఖాళీ లిస్ట్ రిటర్న్ అవుతుంది బ్రో
        return []