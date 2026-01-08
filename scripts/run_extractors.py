from src.extractors.rozee import RozeeExtractor
from src.extractors.careerjet import CareerjetExtractor
from src.utils.logger import get_logger
from config.settings import EXTRACTORS

logger = get_logger(__name__)

rozee_cfg = EXTRACTORS["rozee"]
careerjet_cfg = EXTRACTORS["careerjet"]

def main():
    rozee_jobs = []
    careerjet_jobs = []

    rozee_extractor = None
    careerjet_extractor = None

    try:
        if rozee_cfg["enabled"]:
            logger.info("Starting Rozee.pk scraper...")
            rozee_extractor = RozeeExtractor(
                base_url="https://www.rozee.pk/job/jsearch/q/",
                card="div.job"
            )
            rozee_jobs = rozee_extractor.fetch_jobs(rozee_cfg["max_pages"])

        if careerjet_cfg["enabled"]:
            logger.info("Starting CareerJet.pk scraper...")
            careerjet_extractor = CareerjetExtractor(
                base_url="https://www.careerjet.com.pk/jobs?l=Pakistan&nw=1&s=",
                card="ul.jobs li article.job"
            )
            careerjet_jobs = careerjet_extractor.fetch_jobs(careerjet_cfg["max_pages"])

    except Exception:
        logger.exception("Fatal error in run_extractors")
        return False

    if rozee_jobs and rozee_extractor:
        rozee_extractor.save_jobs("data/raw/rozee.json", rozee_jobs)
        logger.info("Saved rozee_jobs to data/raw/rozee.json")

    if careerjet_jobs and careerjet_extractor:
        careerjet_extractor.save_jobs("data/raw/careerjet.json", careerjet_jobs)
        logger.info("Saved careerjet_jobs to data/raw/careerjet.json")

    return True


if __name__ == "__main__":
    main()
