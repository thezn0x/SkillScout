from src.transformers.careerjet_cleaner import CareerjetCleaner
from src.transformers.rozee_cleaner import RozeeCleaner
import json
import os
from src.utils.logger import get_logger
from pathlib import Path
from config.settings import TRANSFORMERS,EXTRACTORS

OUTPUT_DIR = TRANSFORMERS["output_dir"]
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Logger
logger = get_logger(__name__)


TRANSFORMERS_MAP = {
    "rozee": RozeeCleaner,
    "careerjet": CareerjetCleaner
}

def main():
    try:
        overall_success = True
        for name, config in TRANSFORMERS.items():
            if not isinstance(config, dict):
                continue

            input_path = EXTRACTORS[name]["output_path"]
            if not Path(input_path).exists():
                logger.warning(f"No data from {name} extractor")
                continue

            with open(input_path) as f:
                jobs = json.load(f)

            cleaner = TRANSFORMERS_MAP.get(name)(extractor_name=name)
            cleaned = cleaner.transform(jobs)

            cleaner.save_jobs(config["output_path"], cleaned)
            logger.info(f"Cleaned {len(cleaned)} jobs from {name}")
        
    except Exception:
        logger.exception(f"Critical error while performing {__name__}")
        overall_success = False

    return overall_success

if __name__ == "__main__":
    main()