import json
from util.validate import Validate

class Profile:
    def __init__(self, profile_path: str) -> None:
        Validate.validate_file(profile_path)
        Validate.validate_extension(profile_path, ".json")
        with open(profile_path) as f:
            self.profile_data = json.load(f)
        self.experience = self.set_data("experiences")
        self.skills = self.set_data("skills")
        self.projects = self.set_data("projects")
        self.detailed_education = self.profile_data["detailed_education"]
        self.simple_education = self.profile_data["simple_education"]

    def set_data(self, key:str):
        try:
            return "\n".join(self.profile_data.get(key, []))
        except Exception as e:
            raise e