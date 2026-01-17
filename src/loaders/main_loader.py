from typing import List,Dict,Any
import json
from config.settings import LOADERS
from znpg import Database
from dotenv import load_dotenv
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

    def load(self,table , data: List[Dict[str,Any]]):
        conn_string = os.getenv("DATABASE_URL")
        with Database() as db:
            db.url_connect(conn_string=conn_string)
            db.bulk_insert(table=table,data=data)
