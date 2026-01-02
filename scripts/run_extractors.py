import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.extractors.rozee import RozeeExtractor
from src.extractors.careerjet import CareerjetExtractor

def main():
    print("Starting Rozee.pk scraper...")
    extractor_1 = RozeeExtractor(base_url="https://www.rozee.pk/job/jsearch/q/",card="div.job")
    rozee_jobs = extractor_1.fetch_jobs(max_pages=2)
    if rozee_jobs:
        extractor_1.save_jobs("data/raw/rozee.json", rozee_jobs)


    print("Starting Careerjet.com.pk scraper...")
    extractor_2 = CareerjetExtractor(base_url="https://www.careerjet.com.pk/jobs?l=Pakistan&nw=1&s=",card="ul.jobs li article.job")
    careerjet_jobs = extractor_2.fetch_jobs(max_pages=2)
    if careerjet_jobs:    
        extractor_2.save_jobs("data/raw/careerjet.json", careerjet_jobs)
        print("Saved to data/raw/careerjet.json")

if __name__ == "__main__":
    main()
