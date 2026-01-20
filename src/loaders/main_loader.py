from config.settings import TRANSFORMERS
from config.settings import LOADERS
from typing import List,Dict,Any
from dotenv import load_dotenv
from znpg import Database
import json
import os

load_dotenv(LOADERS["dotenv_path"])

class Loader:
    def __init__(self,name):
        self.name = name

    def get_data(self, data_map):
        data = []
        for name,path in data_map.items():
            with open(path,"r") as f:
                _data = json.load(f)
                data.extend(_data)
        return data

    def load_companies(self,table , data: List[Dict[str,Any]]):
        companies = []
        for job in data:
            company= job.get("company",None)
            companies.append(company)

        unique_companies = list(set(companies))
        loading_list = []
        for comp in unique_companies:
            loading_list.append({"name":comp})

        with Database() as db:
            db.url_connect(os.getenv("DATABASE_URL"))
            db.bulk_insert(table,loading_list)
            keys = db.select(table,["company_id","name"])
        return keys


# test:
if __name__ == "__main__":
    loader = Loader("loader")
    with open(TRANSFORMERS["rozee"]["output_path"],"r") as f:
        data = json.load(f)
    loader.load_companies("companies",data)