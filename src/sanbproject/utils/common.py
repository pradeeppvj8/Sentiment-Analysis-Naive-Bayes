from pathlib import Path
import yaml
from box import ConfigBox
from ensure import ensure_annotations
from sanbproject.logger import logging
import os

@ensure_annotations
def read_yaml(file_path: Path) -> ConfigBox:
    """
    API to read and return a yaml file
    """
    with open(file_path) as yaml_file:
        content = None

        try:
            content = yaml.safe_load(yaml_file)

            if content :
                content = ConfigBox(content)

            logging.info(f"Yaml file {file_path} loaded successfully")
        except Exception as e:
            logging.error(f"Error while loading {file_path} - {e}")
            
        return content
    
@ensure_annotations
def create_directories(paths : list):
    """
    API to create directories
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Created directory {path} successfully")