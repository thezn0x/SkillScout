from src.transformers.cleaner import Cleaner
from src.utils.logger import get_logger
from config.settings import TRANSFORMERS

rozee_config = TRANSFORMERS["rozee"]
careerjet_config = TRANSFORMERS["careerjet"]

logger = get_logger(__name__)

# Map transformer names to their classes for scalability
# If you want to add a transformer, just import it and add to the map and also add its config in config/config.toml
TRANSFORMER_MAP = {
    "rozee": Cleaner,
    "careerjet": Cleaner,
}

def main():
    try:
        for name, config in TRANSFORMERS.items():
            overall_success = True
            # Skip items that are not transformer configurations
            if not isinstance(config, dict):
                continue

            if not config.get("enabled", False):
                continue

            try:
                logger.info(f"Starting {name} transformer...")
                transformer_class = TRANSFORMER_MAP.get(name)
                if not transformer_class:
                    logger.warning(f"No transformer class found for '{name}'. Skipping.")
                    continue
                transformer = transformer_class(base_url=config["base_url"],card=config["card"])
                jobs = transformer.fetch_jobs(max_pages=config["max_pages"])
                if jobs:
                    file_path = config["file_path"]
                    transformer.save_jobs(file_path, jobs)
                    logger.info(f"Saved {len(jobs)} jobs from {name} to {file_path}")
                else:
                    logger.info(f"No jobs found for {name}.")

            except Exception:
                logger.exception(f"Fatal error in '{name}' transformer")
                return False                      
    except Exception:
        logger.exception("Error while performing %s",__name__)
        return False
        overall_success = False
    return overall_success


if __name__ == "__main__":
    if main():
        logger.info("All transformers finished successfully.")
    else:
        logger.error("One or more transformers failed.")