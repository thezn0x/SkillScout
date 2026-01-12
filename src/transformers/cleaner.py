from typing import List, Dict, Any
from src.utils.logger import get_logger
from .soft_skills import SOFT_SKILLS_KEYWORDS
import json
import os
from datetime import datetime, timedelta
import re
from config.settings import TRANSFORMERS

rozee_cfg = TRANSFORMERS["rozee"]
careerjet_cfg = TRANSFORMERS["careerjet"]


# OUTPUT DIRECTORY
OUTPUT_DIR = TRANSFORMERS["output_dir"]
os.makedirs(OUTPUT_DIR,exist_ok=True)

# LOGGER
logger = get_logger(__name__)

class Cleaner:
    def __init__(self,extractor_name: str):
        self.extractor_name = extractor_name

    @staticmethod
    def _parse_date(date_str: str) -> str:
            """Parse date to ISO format (YYYY-MM-DD)"""
            if not date_str:
                return None
            
            date_str = date_str.strip()
            
            # Already ISO
            if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                return date_str
            
            # "Jan 07, 2026" format
            for fmt in ['%b %d, %Y', '%B %d, %Y']:
                try:
                    parsed = datetime.strptime(date_str, fmt)
                    return parsed.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # "3 days ago" format
            relative = re.search(r'(\d+)\s+(hour|day|week|month)s?\s+ago', 
                            date_str, re.IGNORECASE)
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
            return date_str
    
    def clean_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_job = {}

        # HELPER FUNCTION
        def _clean_text(text: str) -> str:
            if text:
                return text.strip()
            return ""
        if self.extractor_name == 'careerjet':
            # CLEAN TIME: Only for careerjet for now
            cleaned_job["posted_date"] = None
            rel_date = job["posted_date"]
            scraped_date = job["scraped_at"]
            pattern = careerjet_cfg["date_pattern"] if self.extractor_name == 'careerjet' else rozee_cfg["date_pattern"]
            date = datetime.fromisoformat(scraped_date)
            find_pattern = re.search(pattern=pattern,flags=re.I,string=rel_date)
            if find_pattern:
                rel_date_list = find_pattern.group().split(" ")
                try:
                    time_to_minus = int(rel_date_list[0])
                    type_of_time = rel_date_list[1]
                    match type_of_time:
                        case 'hour' | 'hours':
                            actual_posted_date = date - timedelta(hours=time_to_minus)
                        case 'day' | 'days':
                            actual_posted_date = date - timedelta(days=time_to_minus)
                        case 'week' | 'weeks':
                            actual_posted_date = date - timedelta(weeks=time_to_minus)
                        case 'month' | 'months':
                            if time_to_minus > 1:
                                actual_posted_date = None
                            else:
                                actual_posted_date = date - timedelta(days=time_to_minus*30)
                        case 'year' | 'years':
                            actual_posted_date = None
                        case _:
                            actual_posted_date = None
                    cleaned_job["posted_date"] = str(actual_posted_date)
                except Exception:
                    cleaned_job["posted_date"] = None
        elif self.extractor_name == 'rozee':
            cleaned_job["posted_date"] = self._parse_date(job["posted_date"])

        # EDGE-CASE: If job is older than 1 month then it will be truncated: BETA
        # if cleaned_job["posted_date"] is None:
            # cleaned_job["posted_date"] = job["posted_date"]
            #return None

        # CLEAN BASIC FIELDS FOR SAFETY
        cleaned_job["title"] = _clean_text(job.get("title", ""))
        cleaned_job["url"] = _clean_text(job.get("url", ""))
        cleaned_job["location"] = _clean_text(job.get("location", ""))
        cleaned_job["description"] = _clean_text(job.get("description", ""))
        cleaned_job["company"] = _clean_text(job.get("company", ""))
        
        # CLEAN SALARY
        if "salary" in job and job["salary"]:
            try:
                salary_text = job["salary"]
                parts = salary_text.split("-")
                if "k" in parts[0] or parts[1]:
                    min_sal = parts[0].lower().replace("k", "").replace(",", "").strip()
                    max_sal = parts[1].lower().replace("k", "").replace(",", "").strip()
                    
                    cleaned_job["min_salary"] = int(min_sal) * 1000
                    cleaned_job["max_salary"] = int(max_sal) * 1000
                else:
                    min_sal = parts[0].lower().replace(",", "").strip()
                    max_sal = parts[1].lower().replace(",", "").strip()
                    cleaned_job["min_salary"] = int(min_sal)
                    cleaned_job["max_salary"] = int(max_sal)
            except Exception:
                logger.warning(f"Could not perform {__name__}, setting min_salary and max_salary to 'None'")
                cleaned_job["min_salary"] = None
                cleaned_job["max_salary"] = None
        else:
            cleaned_job["min_salary"] = None
            cleaned_job["max_salary"] = None
        
        # CLEAN SKILLS
        cleaned_job["soft_skills"] = []
        cleaned_job["skills"] = []
        raw_skills = job.get("skills", [])
        for skill in raw_skills:
            if skill.lower() in SOFT_SKILLS_KEYWORDS:
                cleaned_job["soft_skills"].append(skill.lower())
            else:
                cleaned_job["skills"].append(skill.lower())
                
        # SOURCE
        cleaned_job["source"] = job.get("source", "unknown")

        return cleaned_job

    def clean_jobs(self, jobs: List) -> List[Dict[str, Any]]:
        logger.info("Starting clean_jobs()...")
        return [self.clean_job(j) for j in jobs]
    
    @staticmethod
    def save_jobs(filename: str, jobs: List[Dict]) -> None:
        try:
            logger.info("Saving jobs...")
            # EDGE-CASE: If job is None then remove it
            with open(filename, "w") as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            logger.exception("Error while performing operation: %s",__name__)
            return False