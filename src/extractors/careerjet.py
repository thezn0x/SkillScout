from datetime import datetime
import os
from .base import Extractor
from typing import Dict,Any

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR,exist_ok=True)

class CareerjetExtractor(Extractor):
    def extract(self,card) -> Dict[str,Any]:
        job={}
        def get_text(selector:str):
            element = card.query_selector(selector)
            return element.inner_text().strip() if element else "N/A"
        # GET APPLICATION URL
        appli_url = f"https://careerjet.com.pk{card.get_attribute('data-url')}"    
        job["url"] = appli_url if appli_url else None
        # GET TITLE
        title = get_text("header h2 a")
        job["title"]= title
        # GET COMPANY NAME
        company = get_text("p a")
        job["company"]=company
        # GET LOCATION
        location = get_text("ul.location li")
        job["location"]=location + ", Pakistan"
        # GET DESCRIPTION
        description = get_text("div.desc")
        text = description
        job["description"]=description
        job["is_truncated"]=text.strip().endswith("…")
        # GET DATE
        date = get_text("footer ul.tags li span[class='badge badge-r badge-s badge-icon']")
        job["date"]=date
        # METADATA
        job["source"] = "https://careerjet.com.pk"
        job["scraped_at"]=datetime.utcnow().isoformat()
        return job
                