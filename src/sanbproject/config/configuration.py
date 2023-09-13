from sanbproject.constants import *
from sanbproject.utils.common import read_yaml
from sanbproject.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH,
                params_filepath = PARAMS_FILE_PATH, schema_filepath = SCHEMA_FILE_PATH):
        # Contents of 'config' file
        self.config = read_yaml(config_filepath)
        # Contents of 'params' file
        self.params = read_yaml(params_filepath)
        # Contents of 'schema' file
        self.schema = schema_filepath

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Returns all the config data related to data ingestion
        """
        config = self.config.data_ingestion

        data_ingestion_config = DataIngestionConfig(
            root=Path(config.root),
            raw_data_path=Path(config.raw_data_path),
            extracted_data_path=Path(config.extracted_data_path)
        )
        return data_ingestion_config
