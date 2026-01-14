from src.utils.logger import get_logger
from .main_transformer import BaseCleaner
import re
from datetime import datetime, timedelta
from config.settings import TRANSFORMERS
from typing import Dict, Any

logger = get_logger(__name__)
rozee_cfg = TRANSFORMERS["rozee"]


class RozeeCleaner(BaseCleaner):
    
    def parse_date(self, date_str: str) -> str:
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Already ISO format
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            return date_str
        
        # "Jan 07, 2026" format
        for fmt in ['%b %d, %Y', '%B %d, %Y']:
            try:
                parsed = datetime.strptime(date_str, fmt)
                return parsed.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # "3 days ago" format (if Rozee uses this)
        relative = re.search(
            rozee_cfg.get("date_pattern", r'(\d+)\s+(hour|day|week|month)s?\s+ago'), 
            date_str, 
            re.IGNORECASE
        )
        if relative:
            amount = int(relative.group(1))
            unit = relative.group(2).lower()
            
            now = datetime.now()
            if unit == 'hour':
                date = now - timedelta(hours=amount)
            elif unit == 'day':
                date = now - timedelta(days=amount)
            elif unit == 'week':
                date = now - timedelta(weeks=amount)
            elif unit == 'month':
                date = now - timedelta(days=amount * 30)
            
            return date.strftime('%Y-%m-%d')
        
        # Fallback
        logger.warning(f"Could not parse date: {date_str}")
        return date_str
    
    def transform(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Main transformation pipeline for Rozee jobs"""
        # Step 1: Clean basic text fields
        cleaned = self.clean_basic_fields(job)
        
        # Step 2: Parse salary
        if cleaned.get("salary"):
            min_sal, max_sal = self.clean_salary(cleaned["salary"])
            cleaned["min_salary"] = min_sal
            cleaned["max_salary"] = max_sal
        else:
            cleaned["min_salary"] = None
            cleaned["max_salary"] = None
        
        # Step 3: Filter skills
        if cleaned.get("skills"):
            soft_skills, core_skills = self.filter_skills(cleaned["skills"])
            cleaned["soft_skills"] = soft_skills
            cleaned["core_skills"] = core_skills
            cleaned["skill_count"] = len(core_skills)
        else:
            cleaned["soft_skills"] = []
            cleaned["core_skills"] = []
            cleaned["skill_count"] = 0
        
        # Step 4: Parse date
        if cleaned.get("posted_date"):
            cleaned["posted_date"] = self.parse_date(cleaned["posted_date"])
        
        return cleaned