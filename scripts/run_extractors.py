from src.extractors.rozee import RozeeExtractor
from src.extractors.careerjet import CareerjetExtractor
from src.utils.logger import get_logger
from config.settings import EXTRACTORS

logger = get_logger(__name__)

# Map extractor names to their classes for scalability
# If you want to add an extractor just import it and add to the map and also add its config in config/config.toml
EXTRACTOR_MAP = {
    "rozee": RozeeExtractor,
    "careerjet": CareerjetExtractor,
}

def main():
    """
    Runs all enabled extractors based on the configuration.
    Each extractor runs independently.
    """
    overall_success = True
    for name, config in EXTRACTORS.items():
        # Skip items that are not extractor configurations
        if not isinstance(config, dict):
            continue

        if not config.get("enabled", False):
            continue

        try:
            logger.info(f"Starting {name} scraper...")
            extractor_class = EXTRACTOR_MAP.get(name)

            if not extractor_class:
                logger.warning(f"No extractor class found for '{name}'. Skipping.")
                continue

            extractor = extractor_class(
                base_url=config["base_url"],
                card=config["card"]
            )
            jobs = extractor.fetch_jobs(config["max_pages"])

            if jobs:
                file_path = config["file_path"]
                extractor.save_jobs(file_path, jobs)
                logger.info(f"Saved {len(jobs)} jobs from {name} to {file_path}")
            else:
                logger.info(f"No jobs found for {name}.")

        except Exception:
            logger.exception(f"Fatal error in '{name}' extractor")
            overall_success = False
            # Continue to the next extractor

    return overall_success


if __name__ == "__main__":
    if main():
        logger.info("All extractors finished successfully.")
    else:
        logger.error("One or more extractors failed.")
