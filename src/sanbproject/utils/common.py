from pathlib import Path
import yaml
from box import ConfigBox
from ensure import ensure_annotations

@ensure_annoations
def read_yaml(file_path: Path) -> ConfigBox:
    """
    API to read and return a yaml file
    """
    with open(file_path) as yaml_file:
        content = yaml.safe_load(yaml_file)
        return ConfigBox(content)