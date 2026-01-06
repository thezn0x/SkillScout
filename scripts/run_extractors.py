from src.extractors.rozee import RozeeExtractor
from src.extractors.careerjet import CareerjetExtractor
from src.utils.logger import get_logger
from config.settings import EXTRACTORS

logger = get_logger(__name__)

rozee_cfg = EXTRACTORS["rozee"]
careerjet_cfg = EXTRACTORS["careerjet"]

def run_extractors():
    rozee_jobs = []
    careerjet_jobs = []

    extractor_1 = None
    extractor_2 = None

    try:
        if rozee_cfg["enabled"]:
            logger.info("Starting Rozee.pk scraper...")
            extractor_1 = RozeeExtractor(
                base_url="https://www.rozee.pk/job/jsearch/q/",
                card="div.job"
            )
            rozee_jobs = extractor_1.fetch_jobs(rozee_cfg["max_pages"])

        if careerjet_cfg["enabled"]:
            logger.info("Starting CareerJet.pk scraper...")
            extractor_2 = CareerjetExtractor(
                base_url="https://www.careerjet.com.pk/jobs?l=Pakistan&nw=1&s=",
                card="ul.jobs li article.job"
            )
            careerjet_jobs = extractor_2.fetch_jobs(careerjet_cfg["max_pages"])

    except Exception:
        logger.exception("Fatal error in run_extractors")
        return False

    if rozee_jobs and extractor_1:
        extractor_1.save_jobs("data/raw/rozee.json", rozee_jobs)
        logger.info("Saved rozee_jobs to data/raw/rozee.json")

    if careerjet_jobs and extractor_2:
        extractor_2.save_jobs("data/raw/careerjet.json", careerjet_jobs)
        logger.info("Saved careerjet_jobs to data/raw/careerjet.json")

    return True


if __name__ == "__main__":
    run_extractors()
