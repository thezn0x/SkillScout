from typing import List, Dict, Any
from src.utils.logger import get_logger

# LOGGER
logger = get_logger(__name__)

class Cleaner:
    def clean_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_job = {}

        # HELPER FUNCTION
        def _clean_text(text: str) -> str:
            if text:
                return text.strip()
            return ""

        # CLEAN BASIC FIELDS FOR SAFETY
        cleaned_job["title"] = _clean_text(job.get("title", ""))
        cleaned_job["url"] = _clean_text(job.get("url", ""))
        cleaned_job["location"] = _clean_text(job.get("location", ""))
        cleaned_job["description"] = _clean_text(job.get("description", ""))
        cleaned_job["posted_date"] = _clean_text(job.get("posted_date", ""))
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
        cleaned_job["skills"] = job.get("skills", [])
        
        # SOURCE
        cleaned_job["source"] = job.get("source", "unknown")
        
        return cleaned_job

    def clean_jobs(self, jobs: List) -> List[Dict[str, Any]]:
        logger.info("Starting clean_jobs()...")
        return [self.clean_job(j) for j in jobs]