from src.transformers.cleaner import Cleaner
import json 
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    jobs_cleaner = Cleaner()
    try:
        with open("data/raw/careerjet.json") as f:
            careerjet_job_data = json.load(f)
        cleaned_careerjet_jobs = jobs_cleaner.clean_jobs(careerjet_job_data)

        with open("data/raw/rozee.json") as f:
            rozee_job_data = json.load(f)
        cleaned_rozee_jobs = jobs_cleaner.clean_jobs(rozee_job_data)

        if cleaned_careerjet_jobs:
            jobs_cleaner.save_jobs("data/curated/cleaned_careerjet.json",cleaned_careerjet_jobs)

        if cleaned_rozee_jobs:
            jobs_cleaner.save_jobs("data/curated/cleaned_rozee.json",cleaned_rozee_jobs)
        return True

    except Exception:
        logger.exception("Error while performing %s",__name__)
        return False

if __name__ == "__main__":
    main()