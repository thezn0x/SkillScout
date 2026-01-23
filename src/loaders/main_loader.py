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
            db.bulk_insert(table,to_load,"DO NOTHING")
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

    def load_locations(self, table:str, data:List[Dict[str,Any]]) -> List[Dict[str, Any]]:
        locations = self.get_unique(data, "location")
        location_list = []
        for location in locations:
            string_parts = location.split(",")
            if len(string_parts) > 1:
                location_list.append({"city": string_parts[0].strip(), "country": string_parts[1].strip()})
            else:
                location_list.append({"city":string_parts[0].strip(),"country":"Pakistan"})
        return self.load_get_keys(table,location_list,["location_id","city","country"])

    def load_jobs(self, table:str, data:List[Dict[str,Any]], company_keys:List[Dict[str,Any]]) -> List[Dict[str, Any]]:
        jobs_list = []
        company_map = {c["name"]: c["company_id"] for c in company_keys}
        for job in data:
            if job["company"] not in company_map:
                continue
            job_data = {
                "title": job["title"],
                "company_id": company_map[job["company"]],
                "description": job.get("description"),
                "application_url": job.get("application_url"),
                "min_salary": job.get("min_salary"),
                "max_salary": job.get("max_salary"),
                "posted_date": job.get("posted_date"),
                "min_experience": job.get("min_experience"),
                "salary_currency": "PKR",
                "scraped_date": job.get("scraped_date")
            }
            jobs_list.append(job_data)
        return self.load_get_keys(table,jobs_list,['job_id',"title","application_url"])

    def load_job_skills(self, table:str, data:List[Dict[str,Any]], job_keys:List[Dict[str,Any]], skill_keys:List[Dict[str,Any]]) -> List[Dict[str,Any]]:
        job_lookup = {job["application_url"]:job["job_id"] for job in job_keys}
        skill_lookup = {skill["skill_name"]:skill["skill_id"] for skill in skill_keys}
        junc_list = []
        for job in data:
            if job.get("application_url") not in job_lookup:
                continue
            job_id = job_lookup.get("application_url")
            for skill in job.get("skills",[]):
                if skill not in skill_lookup:
                    continue
                skill_id = skill_lookup.get("skill_name")
                junc_list.append({job_id:skill_id})
        return self.load_get_keys(table,junc_list,["job_id","skill_id"])

    def load_job_locations(self, table:str, data:List[Dict[str,Any]],job_keys:List[Dict[str,Any]], location_keys:List[Dict[str,Any]]) -> List[Dict[str,Any]]:
        job_lookup = {job["application_url"]:job["job_id"] for job in job_keys}
        location_lookup = {(location["city"],location["country"]):location["location_id"] for location in location_keys}
        jun_list = []
        for job in data:
            job_id = job_lookup[job["application_url"]]
            location_str = job.get('location')
            parts = location_str.split(",")
            city = parts[0]
            country = parts[1] if len(parts)>1 else "Pakistan"
            loc = (city, country)
            if loc in location_lookup:
                loc_id = location_lookup[loc]
                jun_list.append({job_id:loc_id})
        return self.load_get_keys(table,jun_list,["job_id","location_id"])