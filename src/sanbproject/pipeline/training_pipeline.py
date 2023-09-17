from sanbproject.config.configuration import ConfigurationManager
from sanbproject.components.data_ingestion import DataIngestion
from sanbproject.components.data_transformation import DataTransformation
from sanbproject.components.model_trainer import ModelTrainer
from sanbproject.logger import logging
from sanbproject.exception import CustomException
import sys

class TrainingPipeline:
    def __init__(self):
        self.configuration_manager = ConfigurationManager()

    def trigger_training_pipeline(self):

        try:
            logging.info("\n\n============== Data Ingestion Started =======================")
            # Get data ingestion config
            data_ingestion_config = self.configuration_manager.get_data_ingestion_config()
            # Get data ingestion component
            data_ingestion_obj = DataIngestion(config=data_ingestion_config)
            # Do data ingestion
            data_ingestion_obj.do_data_ingestion()
            logging.info("\n\n============== Data Ingestion completed =======================\n\n #################")

            logging.info("\n\n============== Data Transformation Started =======================")
            # Get data transformation config
            data_transformation_config = self.configuration_manager.get_data_transformation_config()
            # Get data transformation component
            data_transformation_obj = DataTransformation(config = data_transformation_config)
            # Do data transformation
            data_transformation_obj.perform_data_transformation()
            logging.info("\n\n============== Data Transformation completed =======================\n\n #################")

            logging.info("\n\n============== Model Training Started =======================")
            # Get model trainer config
            model_trainer_config = self.configuration_manager.get_model_trainer_config()
            # Get model trainer component
            model_trainer_obj = ModelTrainer(config = model_trainer_config)
            # Do model training
            model_trainer_obj.perform_model_training()
            logging.info("\n\n============== Model Training completed =======================\n\n #################")

            logging.info("\n\n============== Model Evaluation Started =======================")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)