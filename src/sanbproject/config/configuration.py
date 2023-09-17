from sanbproject.constants import *
from sanbproject.utils.common import read_yaml
from sanbproject.entity.config_entity import (DataIngestionConfig,DataTransformationConfig,
                                              ModelTrainerConfig, ModelEvalConfig)
from pathlib import Path

class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH,
                params_filepath = PARAMS_FILE_PATH, schema_filepath = SCHEMA_FILE_PATH):
        # Contents of 'config' file
        self.config = read_yaml(config_filepath)
        # Contents of 'params' file
        self.params = read_yaml(params_filepath)
        # Contents of 'schema' file
        self.schema = read_yaml(schema_filepath)

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
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Returns all the config data related to data transformation
        """
        config = self.config.data_transformation
        schema = self.schema
        params = self.params

        data_transformation_config = DataTransformationConfig(
            root=Path(config.root),
            full_data_set_path=Path(config.full_data_set_path),
            test_size=params.test_size,
            target_column_name = schema.TARGET_COLUMN_NAME.name,
            all_columns = schema.COLUMNS ,
            tf_idf_vectorizer_path = Path(config.tf_idf_vectorizer_path),
            download_nltk_data = config.download_nltk_data
        )
        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig :
        config = self.config.model_trainer
        
        model_trainer_config = ModelTrainerConfig(
            root= Path(config.root),
            train_x_path= Path(config.train_x_path),
            train_y_path = Path(config.train_y_path),
            model_name = Path(config.model_name)
        )
        return model_trainer_config
    
    def get_model_eval_config(self) -> ModelEvalConfig:
        config = self.config.model_eval

        model_eval_config = ModelEvalConfig(
            root= Path(config.root),
            model_path = Path(config.model_path),
            test_x_path= Path(config.test_x_path),
            test_y_path=Path(config.test_y_path),
            metrics_path=Path(config.metrics_path),
            mlflow_uri=config.mlflow_uri
        )
        return model_eval_config