import json
import os
import re

class Validate:
    @staticmethod
    # Check if file exists and has .json extension
    def validate_file(file_path:str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file not found: {file_path}")

    @staticmethod
    # Validate JSON format
    def validate_json_format(json_file_path:str):
        if not json_file_path.endswith('.json'):
            raise ValueError("file must be a JSON file")
        try:
            with open(json_file_path) as f:
                json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format {json_file_path}")
    
    @staticmethod
    def validate_md_format(md_file: str):
        if not md_file.endswith(".md"):
            raise ValueError("file must be a md file")
        try:
            with open(md_file,"r") as f:
                f.read()
        except Exception as e:
            raise ValueError(f"Cannot read markdown file: {e}")
        
    @staticmethod
    def sanitize_filename(text: str) -> str:
        return re.sub(r'[ \\\/*?:"<>|/-]', "_", text).strip().lower()