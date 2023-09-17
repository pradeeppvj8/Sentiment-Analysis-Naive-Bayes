from pathlib import Path
import yaml
from box import ConfigBox
from ensure import ensure_annotations
from sanbproject.logger import logging
import os
import joblib
import json

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

@ensure_annotations
def save_bin(data, path:Path):
    """ 
    Saves binary file

    Args:
        data: data to be saved as binary
        path (Path): path of binary file
    """
    joblib.dump(data, path)
    logging.info(f"Binary file saved at : {path}")

@ensure_annotations
def load_bin(path: Path):
    """
    Loads saved object
    """
    obj = joblib.load(path)
    logging.info(f"Loaded object stored in {path}")
    return obj

@ensure_annotations
def save_json(data ,path: Path):

    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

    logging.info(f"Saved json file in path {path}")