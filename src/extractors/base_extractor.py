from playwright.sync_api import sync_playwright
import json
import time
from abc import abstractmethod

class Extractor:
    def __init__(self, role, base_url,cards_class):
        self.role = role
        self.base_url = base_url
        self.cards_class = cards_class

    @abstractmethod
    def extract_single_job(self,card):
        pass

    def fetch_jobs(self, max_pages):
        jobs = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            for page_num in range(1, max_pages+1):
                url = self.base_url if page_num == 1 else f"{self.base_url}/p{page_num}"
                page.goto(url, timeout=60000)
                time.sleep(6.0)
                job_cards = page.query_selector_all(f"div.{cards_class}")
                for card in job_cards:
                    job = extract_single_job(card)
                    if job and job.get("title"):
                        jobs.append(job)
            if page_num < max_pages:
                time.sleep(2.0)
        browser.close()
        return jobs

    def clean_text(self,text):
        return " ".join(text.split()).strip(" ,.-") if text else ""

    def save_jobs_to_json(self, filename, jobs):
        with open(filename, "w") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
