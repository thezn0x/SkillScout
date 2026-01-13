from src.transformers.cleaner import Cleaner
import json 
from src.utils.logger import get_logger
from pathlib import Path
from config.settings import TRANSFORMERS,EXTRACTORS

# Logger
logger = get_logger(__name__)


TRANSFORMERS_MAP = {
    "rozee": Cleaner,
    "careerjet": Cleaner
}

def main():
    try:
        overall_success = True
        for name, config in TRANSFORMERS.items():
            if not isinstance(config, dict):
                continue

            if not config.get("enabled", False):
                continue

            input_path = EXTRACTORS[name]["output_path"]
            if not Path(input_path).exists():
                logger.warning(f"No data from {name} extractor")
                continue

            with open(input_path) as f:
                jobs = json.load(f)

            cleaner = Cleaner(extractor_name=name)
            cleaned = cleaner.clean_jobs(jobs)

            cleaner.save_jobs(config["output_path"], cleaned)
            logger.info(f"Cleaned {len(cleaned)} jobs from {name}")
        
    except Exception:
        logger.exception(f"Critical error while performing {__name__}")
        overall_success = False

    return overall_success

if __name__ == "__main__":
    main()