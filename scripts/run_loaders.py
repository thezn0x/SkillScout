from config.settings import TRANSFORMERS
from src.loaders.main_loader import Loader
from config.settings import LOADERS
from typing import Dict,Any,Union
from src.utils.logger import get_logger

logger = get_logger(__name__)
DATA_MAP = {
    "rozee" : TRANSFORMERS["rozee"]["output_path"],
    "careerjet" : TRANSFORMERS["careerjet"]["output_path"]
}

def main() -> Union[Dict[str,Any],None]:
    logger.info("Starting Loader...")
    try:
        loader = Loader(__name__)
        data = loader.get_data(DATA_MAP)
        skill_keys = loader.load_skills("skills",data)
        location_keys = loader.load_locations("locations",data)
        company_keys = loader.load_companies("companies",data)
        platform_keys = loader.load_platforms("platforms",LOADERS)
        job_keys = loader.load_jobs("jobs",data,company_keys)
        job_skills_keys = loader.load_job_skills("job_skills",data,job_keys,skill_keys)
        job_location_keys = loader.load_job_locations("job_locations",data,job_keys, location_keys)
        job_platform_keys = loader.load_job_platforms("job_platforms",data,job_keys, platform_keys)
        keys = {
            'skill_keys' : skill_keys,
            'location_keys' : location_keys,
            'company_keys' : company_keys,
            'platform_keys' : platform_keys,
            'job_keys' : job_keys,
            'job_skills_keys' : job_skills_keys,
            'job_location_keys' : job_location_keys,
            'job_platform_keys' : job_platform_keys
        }
        logger.info("Loaded all data successfully")
        return keys
    except Exception as e:
        logger.error("Error while performing %s: %s",__name__,e)
        return None

if __name__ == "__main__":
    main()