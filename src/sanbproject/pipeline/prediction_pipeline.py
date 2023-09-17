from sanbproject.config.configuration import ConfigurationManager
import joblib
from sanbproject.components.data_transformation import DataTransformation
from sanbproject.utils.common import load_bin
from pathlib import Path
import os
import pandas as pd
from sanbproject.logger import logging

class PredictionPipeline:
    def __init__(self):
        # Get model path
        # Load configuration object
        self.config = ConfigurationManager()

    def return_data_transformation_config(self):
        data_transformation_config = self.config.get_data_transformation_config()
        return data_transformation_config

    def perform_text_preprocessing(self, input):
        # Fet data transformation config
        data_transformation_config = self.return_data_transformation_config()
        # Get data transformation object
        data_transformation_obj = DataTransformation(config=data_transformation_config)
        # Prepare the objects required for preprocessing the "review" text
        lemmatizer, punc_to_remove, stop_words, speller = data_transformation_obj.get_required_preprocessing_objects()
        # Perform text preprocessing
        processed_input = data_transformation_obj.perform_text_preprocessing(input, lemmatizer, punc_to_remove,
                                                                             stop_words, speller)
        
        logging.info(f"The review was processed into : {processed_input}")

        # Get tf-idf vectorizor object
        tf_idf_vectorizer = load_bin(Path(os.path.join(data_transformation_config.tf_idf_vectorizer_path,
                                                       "tf_idf_vectorizer_obj")))
        
        processed_input = [str(processed_input)]

        logging.info(f"The input being sent to tf-idf vectorizer {processed_input}")
        
        # Perform tf-idf vectorization
        processed_input = tf_idf_vectorizer.transform(processed_input)

        processed_input = pd.DataFrame(processed_input.toarray())

        processed_input = processed_input.reset_index(drop=True)

        processed_input.columns = processed_input.columns.astype(str)

        logging.info(f"The review after tf-idf vectorization : {processed_input}")
        return processed_input
    
    def return_model_eval_config(self):
        model_eval_config = self.config.get_model_eval_config()
        return model_eval_config

    def perform_prediction(self, input: str):
        logging.info(f"Prediction is starting for review : {input}")
        # Preprocess the input
        processed_input = self.perform_text_preprocessing(input)

        # Load the model
        model_eval_config = self.return_model_eval_config()
        model = joblib.load(model_eval_config.model_path)

        # Perform predictions
        prediction = model.predict(processed_input)[0]

        logging.info(f"Prediction was done successfully and the prediction is {prediction}")
        return prediction