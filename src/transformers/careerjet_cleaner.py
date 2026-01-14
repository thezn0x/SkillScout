from src.utils.logger import get_logger
from .main_transformer import BaseCleaner
import re
from datetime import datetime, timedelta
from config.settings import TRANSFORMERS
from typing import Dict, Any

logger = get_logger(__name__)
careerjet_cfg = TRANSFORMERS["careerjet"]


class CareerjetCleaner(BaseCleaner):
    
    def parse_date(self, date_str: str, scraped_at: str) -> str:
        if not date_str or not scraped_at:
            return None
        
        rel_date = date_str.strip()
        
        try:
            # Parse scraped_at timestamp
            scraped_date = datetime.fromisoformat(scraped_at.strip())
        except Exception:
            logger.error(f"Could not parse scraped_at: {scraped_at}")
            return None
        
        # Find relative date pattern
        pattern = careerjet_cfg.get("date_pattern", r'\d+\s+(hour|day|week|month)s?\s+ago')
        find_pattern = re.search(pattern, rel_date, re.I)
        
        if not find_pattern:
            return None
        
        try:
            # Parse "3 days ago" format
            parts = find_pattern.group().split()
            time_amount = int(parts[0])
            time_unit = parts[1].lower()
            
            # Calculate actual date
            if time_unit in ['hour', 'hours']:
                actual_date = scraped_date - timedelta(hours=time_amount)
            elif time_unit in ['day', 'days']:
                actual_date = scraped_date - timedelta(days=time_amount)
            elif time_unit in ['week', 'weeks']:
                actual_date = scraped_date - timedelta(weeks=time_amount)
            elif time_unit in ['month', 'months']:
                # If more than 1 month old, set to None (too old)
                if time_amount > 1:
                    return None
                actual_date = scraped_date - timedelta(days=time_amount * 30)
            elif time_unit in ['year', 'years']:
                # Too old
                return None
            else:
                return None
            
            return actual_date.strftime('%Y-%m-%d')
            
        except Exception:
            logger.exception(f"Error parsing date: {rel_date}")
            return None
    
    def transform(self, job: Dict[str, Any]) -> Dict[str, Any]:
        # Step 1: Clean basic text fields
        cleaned = self.clean_basic_fields(job)
        
        # Step 2: Parse salary (CareerJet usually doesn't have salary)
        if cleaned.get("salary"):
            min_sal, max_sal = self.clean_salary(cleaned["salary"])
            cleaned["min_salary"] = min_sal
            cleaned["max_salary"] = max_sal
        else:
            cleaned["min_salary"] = None
            cleaned["max_salary"] = None
        
        # Step 3: Filter skills (CareerJet usually doesn't have skills)
        if cleaned.get("skills"):
            soft_skills, core_skills = self.filter_skills(cleaned["skills"])
            cleaned["soft_skills"] = soft_skills
            cleaned["core_skills"] = core_skills
            cleaned["skill_count"] = len(core_skills)
        else:
            cleaned["soft_skills"] = []
            cleaned["core_skills"] = []
            cleaned["skill_count"] = 0
        
        # Step 4: Parse date (uses scraped_at for calculation)
        if cleaned.get("posted_date") and cleaned.get("scraped_at"):
            cleaned["posted_date"] = self.parse_date(
                cleaned["posted_date"], 
                cleaned["scraped_at"]
            )
        
        return cleaned