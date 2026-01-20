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

    @staticmethod
    def get_unique(data,field):
        non_unique = []
        for one in data:
            non_unique.append(one.get(field,None))
        if isinstance(non_unique[0],list):
            unique_data = []
            for one in non_unique:
                unique_data.extend(one)
        else:
            unique_data = list(set(non_unique))
        return unique_data


    def get_data(self, data_map):
        data = []
        for name,path in data_map.items():
            with open(path,"r") as f:
                _data = json.load(f)
                data.extend(_data)
        return data

    def load_companies(self,table , data: List[Dict[str,Any]]):
        companies = self.get_unique(data,"company")
        loading_list = []
        for company in companies:
            loading_list.append({"name":company})
        with Database() as db:
            db.url_connect(os.getenv("DATABASE_URL"))
            db.bulk_insert(table,loading_list)
            keys = db.select(table,["company_id","name"])
        return keys
    
    def load_skills(self,table,data):
        placeholder_skills = self.get_unique(data,"core_skills")
        skills = list(set(placeholder_skills))
        to_load = []
        for skill in skills:
            to_load.append({"skill_name":skill})
        with Database() as db:
            db.url_connect(os.getenv("DATABASE_URL"))
            db.bulk_insert(table,to_load)
            keys = db.select(table,["skill_id","skill_name"])
        return keys


# test:
if __name__ == "__main__":
    loader = Loader("loader")
    with open(TRANSFORMERS["rozee"]["output_path"],"r") as f:
        data = json.load(f)
    loader.load_companies("companies",data)
    loader.load_skills("skills",data)