import re
from typing import List,Set
import json

class JobTransformer:
    def __init__(self):
        self.skill_library = [
            "Python", "JavaScript", "React", "Node.js", "SQL", 
            "PostgreSQL", "Docker", "AWS", "Git", "HTML", "CSS"
        ]

    

if __name__ == "__main__":
    tr = JobTransformer()
    tr.extract_skills()
