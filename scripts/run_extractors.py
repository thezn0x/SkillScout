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
                base_url=rozee_cfg["base_url"],
                card=rozee_cfg["card"]
            )
            rozee_jobs = rozee_extractor.fetch_jobs(rozee_cfg["max_pages"])

        if careerjet_cfg["enabled"]:
            logger.info("Starting CareerJet.pk scraper...")
            careerjet_extractor = CareerjetExtractor(
                base_url= careerjet_cfg["base_url"],
                card=careerjet_cfg["card"]
            )
            careerjet_jobs = careerjet_extractor.fetch_jobs(careerjet_cfg["max_pages"])

    except Exception:
        logger.exception("Fatal error in run_extractors")
        return False

    if rozee_jobs and rozee_extractor:
        rozee_extractor.save_jobs(rozee_cfg["output_path"], rozee_jobs)
        logger.info(f"Saved rozee_jobs to {rozee_cfg['output_path']}")

    if careerjet_jobs and careerjet_extractor:
        careerjet_extractor.save_jobs(careerjet_cfg['output_path'], careerjet_jobs)
        logger.info(f"Saved careerjet_jobs to {careerjet_cfg['output_path']}")

    return True


if __name__ == "__main__":
    main()
