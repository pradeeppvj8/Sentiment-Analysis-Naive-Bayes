from sanbproject.entity.config_entity import DataIngestionConfig
from zipfile import ZipFile
from sanbproject.utils.common import create_directories
from sanbproject.logger import logging
from sanbproject.exception import CustomException
import sys

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config

    def do_data_ingestion(self):
        try:
            # Create the root directory
            create_directories([self.config.root])

            with ZipFile(self.config.raw_data_path,'r') as zip_file_obj:
                # Extract the zip file into required location
                zip_file_obj.extractall(self.config.extracted_data_path)

            logging.info("Data ingestion completed successfully")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)