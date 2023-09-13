from sanbproject.config.configuration import ConfigurationManager
from sanbproject.components.data_ingestion import DataIngestion
from sanbproject.logger import logging
from sanbproject.exception import CustomException
import sys

class TrainingPipeline:
    def __init__(self):
        self.configuration_manager = ConfigurationManager()

    def trigger_training_pipeline(self):

        try:
            logging.info("============== Data Ingestion Started =======================")
            # Get data ingestion config
            data_ingestion_config = self.configuration_manager.get_data_ingestion_config()
            # Get data ingestion component
            data_ingestion_obj = DataIngestion(config=data_ingestion_config)
            # Do data ingestion
            data_ingestion_obj.do_data_ingestion()
            logging.info("============== Data Ingestion completed =======================\n\n #################")

            logging.info("============== Data Transformation Started =======================")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)