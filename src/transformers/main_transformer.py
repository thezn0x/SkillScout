from .soft_skills import SOFT_SKILLS_KEYWORDS
from src.utils.logger import get_logger
from datetime import timedelta,datetime
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from config.settings import LOADERS
from dotenv import load_dotenv
from znpg import Database
import json
import os

logger = get_logger(__name__)

class BaseCleaner(ABC):
    def __init__(self, extractor_name: str):
        self.extractor_name = extractor_name

    @staticmethod
    def _clean_text(text: str) -> str:
        if text:
            return text.strip()
        return ""

    def clean_basic_fields(self, job: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_job = {}

        cleaned_job["title"] = self._clean_text(job.get("title", ""))
        cleaned_job["application_url"] = self._clean_text(job.get("url", ""))
        cleaned_job["location"] = self._clean_text(job.get("location", ""))
        cleaned_job["description"] = self._clean_text(job.get("description", ""))
        cleaned_job["company"] = self._clean_text(job.get("company", ""))
        cleaned_job["source"] = job.get("source", "unknown")
        
        # Copy other fields that don't need text cleaning
        cleaned_job["posted_date"] = job.get("posted_date")
        cleaned_job["apply_before"] = datetime.fromisoformat(job.get("posted_date")) + timedelta(10)
        cleaned_job["salary"] = job.get("salary")
        cleaned_job["salary_currency"] = "PKR"
        cleaned_job["experience_text"] = job.get("experience_text")
        cleaned_job["min_experience"] = job.get("experience_years")
        cleaned_job["skills"] = job.get("skills", [])
        cleaned_job["requirements"] = job.get("skills", [])
        cleaned_job["scraped_date"] = job.get("scraped_at")

        return cleaned_job

    def clean_salary(self, salary_str: str) -> tuple:
        if not salary_str:
            return None, None
            
        try:
            parts = salary_str.split("-")
            if len(parts) != 2:
                return None, None
            
            # Check if contains 'k' for thousands
            has_k = 'k' in parts[0].lower() or 'k' in parts[1].lower()
            
            # Clean and parse
            min_sal = parts[0].lower().replace("k", "").replace(",", "").strip()
            max_sal = parts[1].lower().replace("k", "").replace(",", "").strip()
            
            min_salary = int(min_sal) * (1000 if has_k else 1)
            max_salary = int(max_sal) * (1000 if has_k else 1)
            
            return min_salary, max_salary
            
        except Exception:
            logger.warning(f"Could not parse salary: {salary_str}")
            return None, None

    def filter_skills(self, skills: List[str]) -> tuple:
        if not skills:
            return [], []
        
        soft_skills = []
        core_skills = []
        
        for skill in skills:
            skill_lower = skill.lower().strip()
            if skill_lower in SOFT_SKILLS_KEYWORDS:
                soft_skills.append(skill_lower)
            else:
                core_skills.append(skill)
        
        return soft_skills, core_skills

    def clean_jobs(self, jobs: List) -> List[Dict[str, Any]]:
        logger.info(f"Starting clean_jobs() for {self.extractor_name}...")
        cleaned = []
        
        for job in jobs:
            try:
                cleaned_job = self.transform(job)
                if cleaned_job:
                    cleaned.append(cleaned_job)
            except Exception:
                logger.exception(f"Error cleaning job: {job.get('title', 'unknown')}")
        
        return cleaned

    @abstractmethod
    def transform(self, job: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclass must implement transform()")
    
    @staticmethod
    def save_jobs(filename: str, jobs: List[Dict]) -> bool:
        try:
            logger.info(f"Saving {len(jobs)} jobs to {filename}...")
            # Remove None values
            _jobs = [job for job in jobs if job is not None]
            
            # Deduplicate by title, company, and location
            seen_jobs_criteria = set()
            deduplicated_jobs = []
            
            for job in _jobs:
                title = job.get("title", "").strip().lower()
                company = job.get("company", "").strip().lower()
                location = job.get("location", "").strip().lower()
                # A job is considered unique if it has all three criteria
                if title and company and location:
                    job_criteria = (title, company, location)
                    if job_criteria not in seen_jobs_criteria:
                        deduplicated_jobs.append(job)
                        seen_jobs_criteria.add(job_criteria)
                    else:
                        logger.info(f"Skipping duplicate job based on title, company, location: {job.get('title', 'Unknown Title')} - {job.get('company', 'Unknown Company')} - {job.get('location', 'Unknown Location')}")
                else:
                    logger.warning(f"Job missing title, company, or location, skipping for deduplication: {job.get('title', 'Unknown Title')}")

            with open(filename, "w") as f:
                json.dump(deduplicated_jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(deduplicated_jobs)} unique jobs to {filename}. {len(_jobs) - len(deduplicated_jobs)} potential duplicates were removed.")
            return True
        except Exception:
            logger.exception(f"Error saving jobs to {filename}")
            return False