# BETA TEST

from config.settings import TRANSFORMERS
import json
from src.loaders.main_loader import Loader
from config.settings import LOADERS

loader = Loader("loader")
with open(TRANSFORMERS["rozee"]["output_path"],"r") as f:
    data = json.load(f)
    loader.load_companies("companies",data)
    loader.load_skills("skills",data)
        
loader = Loader(__name__)
loader.load_platforms("platforms",LOADERS)