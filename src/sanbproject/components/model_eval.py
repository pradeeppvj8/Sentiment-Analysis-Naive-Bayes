from sanbproject.entity.config_entity import ModelEvalConfig
from sanbproject.logger import logging
from sanbproject.utils.common import load_bin, save_json, create_directories
import pandas as pd
from sklearn import metrics
import mlflow
from urllib.parse import urlparse

class ModelEvaluation:
    def __init__(self, config:ModelEvalConfig):
        self.config = config

    def evaluate_metrics(self, y_test, y_test_pred):
        accuracy = metrics.accuracy_score(y_test, y_test_pred)
        mlflow.log_metric("accuracy" , accuracy)

        precision = metrics.precision_score(y_test, y_test_pred)
        mlflow.log_metric("precision" , precision)

        recall = metrics.recall_score(y_test, y_test_pred)
        mlflow.log_metric("recall" , recall)
        
        f1_score = metrics.f1_score(y_test, y_test_pred)
        mlflow.log_metric("f1_score" , f1_score)

        scores = {"accuracy" : accuracy,
                  "precision" : precision,
                  "recall" : recall,
                  "f1_score" : f1_score
                 }
        return scores

    def perform_model_evaluation(self):
        """
        set MLFLOW_TRACKING_URI=https://dagshub.com/pradeeppvj8/Sentiment-Analysis-Naive-Bayes.mlflow
        set MLFLOW_TRACKING_USERNAME=pradeeppvj8
        set MLFLOW_TRACKING_PASSWORD=f831428c26a708547e8a1e4d90cb85cbeb9bdce3
        """
         
        logging.info("Model Evaluation started")

        # Get the model
        model = load_bin(self.config.model_path)

        # Get the test data
        X_test = pd.read_csv(self.config.test_x_path)
        y_test = pd.read_csv(self.config.test_y_path)
    
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            # Predict the rating of test data
            y_test_pred = model.predict(X_test)

            # Calculate the evaluation metrics
            scores = self.evaluate_metrics(y_test, y_test_pred)

            # Save metrics data into a file
            create_directories([self.config.root])
            save_json(scores, self.config.metrics_path)

            if tracking_url_type_store != "File":
                mlflow.sklearn.log_model(model, "model", registered_model_name = "Multinomial Naive Bayes")
            else:
                mlflow.sklearn.log_model(model, "model")

        logging.info("Model Evaluation has ended")