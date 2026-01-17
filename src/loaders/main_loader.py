from typing import List,Dict,Any
from config.settings import TRANSFORMERS
import json


DATA_MAP={
    "rozee": TRANSFORMERS["rozee"]["output_file"],
    "careerjet": TRANSFORMERS["careerjet"]["output_file"]
}

data = []

for name,path in DATA_MAP.items():
    with open(path,"r") as f:
        _data = json.load(f)
        data.extend(_data)

print(len(data))

class Loader:
    def __init__(self,name):
        self.name = name

    def load(self, data: List[Dict[str,Any]]):
        pass