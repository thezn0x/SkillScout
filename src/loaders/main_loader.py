from config.settings import LOADERS
from typing import List,Dict,Any
from dotenv import load_dotenv
from znpg import Database
import json
import os

load_dotenv(LOADERS["dotenv_path"])

class Loader:
    def __init__(self,name:str):
        self.name = name

    @staticmethod
    def get_unique(data:List[Dict[str,Any]],field:str) -> List[Any]:
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
    @staticmethod
    def load_get_keys(table:str, to_load:List[Dict[str,Any]], columns:List[str]) -> List[Dict[str,Any]]:
        with Database() as db:
            db.url_connect(os.getenv("DATABASE_URL"))
            db.bulk_insert(table,to_load)
            keys = db.select(table, columns)
        return keys

    @staticmethod
    def get_data(data_map:Dict[str,Any]) -> List[Dict[str,Any]]:
        data = []
        for name,path in data_map.items():
            with open(path,"r") as f:
                _data = json.load(f)
                data.extend(_data)
        return data

    def load_companies(self,table:str , data: List[Dict[str,Any]]) -> List[Dict[str,Any]]:
        companies = self.get_unique(data,"company")
        loading_list = []
        for company in companies:
            if company != "N/A":
                loading_list.append({"name":company})
        return self.load_get_keys(table,loading_list,["company_id","name"])

    def load_skills(self,table:str ,data:List[Dict[str,Any]]) -> List[Dict[str,Any]]:
        placeholder_skills = self.get_unique(data,"core_skills")
        skills = list(set(placeholder_skills))
        to_load = []
        for skill in skills:
            to_load.append({"skill_name":skill})
        return self.load_get_keys(table,to_load,["skill_id","skill_name"])

    def load_platforms(self, table: str, platforms_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        all_platforms = []
        platforms = platforms_config.get("platforms", platforms_config)
        for platform_name, platform_data in platforms.items():
            if isinstance(platform_data, dict):
                platform_data["platform_name"] = platform_name
                all_platforms.append(platform_data)
        return self.load_get_keys(table,all_platforms,["platform_id", "platform_name"])

    def load_locations(self, table:str, data:List[Dict[str,Any]]):
        locations = self.get_unique(data, "location")
        location_list = []
        for location in locations:
            string_parts = location.split(",")
            location_list.append({"city": string_parts[0].strip(), "country": string_parts[1].strip()})
        return self.load_get_keys(table,location_list,["location_id","city"])