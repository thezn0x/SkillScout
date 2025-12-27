from playwright.sync_api import sync_playwright
import json
import time
from playwright.sync_api import sync_playwright
from typing import List,Dict,Any

class Extractor:
    def __init__(self, role:str, base_url:str,cards_class:str):
        self.role = role
        self.base_url = base_url
        self.cards_class = cards_class

    def fetch_jobs(self, max_pages:int = 1) -> List[Any]:
        jobs = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            for page_num in range(1, max_pages+1):
                url = self.base_url if page_num == 1 else f"{self.base_url}/p{page_num}"
                page.goto(url, timeout=60000)
                time.sleep(6.0)
                job_cards = page.query_selector_all(f"div.{self.cards_class}")
                for card in job_cards:
                    job = self.extract_single_job(card)
                    if job and job.get("title"):
                        jobs.append(job)
        return jobs
    @staticmethod
    def clean_text(text:str) -> str:
        return " ".join(text.split()).strip(" ,.-") if text else ""

    @staticmethod
    def save_jobs(filename: str, jobs: List[Dict]) -> None:
        with open(filename, "w") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)