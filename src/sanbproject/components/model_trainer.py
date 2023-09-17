from sanbproject.config.configuration import ModelTrainerConfig
from sanbproject.logger import logging
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sanbproject.utils.common import save_bin
from pathlib import Path
import os
from sanbproject.utils.common import create_directories
import numpy as np

class ModelTrainer:
    def __init__(self,config:ModelTrainerConfig):
        self.config = config

    def perform_model_training(self):
        logging.info("Model training has started")

        # Model instantiation
        nb_model = MultinomialNB()

        X_train = pd.read_csv(self.config.train_x_path)
        y_train = np.ravel(pd.read_csv(self.config.train_y_path))

        # Fitting the training data
        nb_model.fit(X_train, y_train)

        # Save model
        create_directories([self.config.root])
        save_bin(nb_model, Path(os.path.join(self.config.root,self.config.model_name)))