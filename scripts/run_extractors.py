from src.extractors.rozee import RozeeExtractor
from src.extractors.careerjet import CareerjetExtractor
from src.utils.logger import get_logger
from config.settings import EXTRACTORS

logger = get_logger(__name__)

EXTRACTORS_MAP = {
    "rozee": RozeeExtractor,
    "careerjet":CareerjetExtractor
}

def main():
    try:
        overall_success = True
        for name, config in EXTRACTORS.items():
            if not isinstance(config, dict):
                continue
            
            if not config.get("enabled", False):
                continue

            try:
                extractor = EXTRACTORS_MAP.get(name)(
                    base_url=config.get("base_url"),
                    card=config.get("card")
                )
                logger.info(f"Starting {name} extractor...")
                if not extractor:
                    logger.warning(f"Couldn't find {name}, skipping to next extractor.")
                    continue

                jobs  = extractor.fetch_jobs(config.get("max_pages"))
                if not jobs:
                    logger.warning(f"No jobs found in {name}.")
                    continue

                try:
                    extractor.save_jobs(config.get("output_path"),jobs)
                    logger.info(f"Saved {len(jobs)} jobs from {name} to {config.get("output_path")}...")
                except Exception:
                    logger.exception(f"Error while saving jobs from {name}.")

            except Exception:
                logger.error(f"Error while extracting jobs from {name}.")

    except Exception:
        logger.exception(f"Critical error while performing {__name__}")
        overall_success = False

    return overall_success

if __name__ == "__main__":
    main()
