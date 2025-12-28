from .base import Extractor
from .roles import one_role
from playwright.sync_api import sync_playwright
from datetime import datetime
import time
import json
import re
import os

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR,exist_ok=True)


class MustakbilExtractor(Extractor):
    def extract_single_job(self):
        job = {}


