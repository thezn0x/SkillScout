import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.extractors.rozee import RozeeExtractor
from src.extractors.careerjet import CareerjetExtractor
from src.utils.logger import get_logger

# LOGGER
logger = get_logger(__name__)

def run_extractors():
    try:
        logger.info("Starting Rozee.pk scraper...")
        extractor_1 = RozeeExtractor(base_url="https://www.rozee.pk/job/jsearch/q/",card="div.job")
        rozee_jobs = extractor_1.fetch_jobs(max_pages=2)
        logger.info("Starting CareerJet.pk scraper...")
        extractor_2 = CareerjetExtractor(base_url="https://www.careerjet.com.pk/jobs?l=Pakistan&nw=1&s=",card="ul.jobs li article.job")
        careerjet_jobs = extractor_2.fetch_jobs(max_pages=2)

    except Exception:
            logger.error("Error while performing operation: %s",__name__)
            return False

    finally:
        if rozee_jobs:
            extractor_1.save_jobs("data/raw/rozee.json", rozee_jobs)
            logger.info("Saved rozee_jobs to data/raw/rozee.json")
        if careerjet_jobs:    
            extractor_2.save_jobs("data/raw/careerjet.json", careerjet_jobs)
            logger.info("Saved careerjet_jobs to data/raw/careerjet.json")

if __name__ == "__main__":
    run_extractors()