import json
import os
import re

class Validate:

    # Check if file exists
    @staticmethod
    def validate_file(file_path:str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file not found: {file_path}")
            
    @staticmethod
    def validate_extension(file: str, extension:str):
        if not file.endswith(extension):
            raise ValueError(f"file must be a {extension} file")
        try:
            with open(file,"r") as f:
                f.read()
        except Exception as e:
            raise ValueError(f"Cannot read file: {e}")
        
    @staticmethod
    def sanitize_filename(text: str) -> str:
        return re.sub(r'[ \\\/*?:"<>|/-]', "_", text).strip().lower()