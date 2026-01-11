from src.transformers.cleaner import Cleaner
import json 
from src.utils.logger import get_logger
from pathlib import Path
from config.settings import TRANSFORMERS,EXTRACTORS

rozee_cfg = TRANSFORMERS["rozee"]
careerjet_cfg = TRANSFORMERS["careerjet"]
rozee_cfg_ex = EXTRACTORS["rozee"]["output_path"]
careerjet_cfg_ex = EXTRACTORS["careerjet"]["output_path"]


# Logger
logger = get_logger(__name__)

def main():
    try:
        careerjet_path = Path(careerjet_cfg_ex)
        rozee_path = Path(rozee_cfg_ex)
        cleaned_careerjet_jobs = []
        cleaned_rozee_jobs = []

        if careerjet_path.exists():
            careerjet_cleaner = Cleaner(extractor_name='careerjet')
            with open(careerjet_cfg_ex) as f:
                careerjet_job_data = json.load(f)
            cleaned_careerjet_jobs = careerjet_cleaner.clean_jobs(careerjet_job_data)
        else:
            logger.error(f"Careerjet jobs not found in {careerjet_cfg_ex}")
        if rozee_path.exists():
            rozee_cleaner = Cleaner(extractor_name='rozee')
            with open(rozee_cfg_ex) as f:
                rozee_job_data = json.load(f)
            cleaned_rozee_jobs = rozee_cleaner.clean_jobs(rozee_job_data)
        else:
            logger.error(f"Rozee jobs not found in {rozee_cfg_ex}")

        if cleaned_careerjet_jobs:
            careerjet_cleaner.save_jobs(careerjet_cfg["output_path"],cleaned_careerjet_jobs)

        if cleaned_rozee_jobs:
            rozee_cleaner.save_jobs(rozee_cfg["output_path"],cleaned_rozee_jobs)
        return True

    except Exception:
        logger.exception("Error while performing %s",__name__)
        return False

if __name__ == "__main__":
    main()