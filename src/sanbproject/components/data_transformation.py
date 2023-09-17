from sanbproject.entity.config_entity import DataTransformationConfig
import pandas as pd
from nltk.stem import WordNetLemmatizer
import string
from nltk.corpus import stopwords
import nltk
from autocorrect import Speller
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
import os
from sanbproject.utils.common import create_directories
from sanbproject.logger import logging
from sanbproject.exception import CustomException
import sys
from sanbproject.utils.common import save_bin
from pathlib import Path

class DataTransformation:
    def __init__(self, config:DataTransformationConfig) -> None:
        self.config = config

        if self.config.download_nltk_data:
            # Download all the stopwords
            nltk.download('stopwords')
            # Download wordnet
            nltk.download('wordnet')

    def perform_data_transformation(self):
        try:
            logging.info("Data transformation has started")
            # Get the data set
            data = pd.read_csv(self.config.full_data_set_path, sep='\t')

            data = self.simplify_data_set(data=data)

            lemmatizer, punc_to_remove, stop_words, speller = self.get_required_preprocessing_objects()

            logging.info("Reviews text preprocessing started")
            
            data.loc[ : , ["preprocessed_review"]] = data["verified_reviews"].apply(lambda text: self.perform_text_preprocessing(text, lemmatizer, punc_to_remove, stop_words, speller))
            
            logging.info("Reviews text preprocessing ended")

            X_train, X_test, y_train, y_test = self.perform_train_test_split(data)

            X_train_tf_idf, X_test_tf_idf = self.perform_tf_idf_vectorization(X_train, X_test)

            X_train_bal, y_train_bal = self.handle_class_imbalance(X_train_tf_idf, y_train)

            self.create_train_test_csv_files(X_train_bal, y_train_bal,X_test_tf_idf, y_test)

            logging.info("Data transformation has ended")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)

    def create_train_test_csv_files(self, X_train_bal, y_train_bal,X_test_tf_idf, y_test):
        create_directories([self.config.root])

        (pd.DataFrame(X_train_bal.toarray())).to_csv(os.path.join(self.config.root, "train_x.csv") , index = False)
        (pd.DataFrame(X_test_tf_idf.toarray())).to_csv(os.path.join(self.config.root, "test_x.csv") , index = False)
        
        y_train_bal.to_csv(os.path.join(self.config.root, "train_y.csv"), index = False)
        y_test.to_csv(os.path.join(self.config.root, "test_y.csv") , index = False)

        logging.info("Created train & test csv files")
        
    def handle_class_imbalance(self, X_train_tf_idf, y_train):
        smote = SMOTE(random_state=42)

        # Handle class imbalance
        X_train_bal, y_train_bal = smote.fit_resample(X_train_tf_idf, y_train)

        logging.info("Class imbalance handled")
        return(X_train_bal, y_train_bal)

    def perform_tf_idf_vectorization(self, X_train, X_test):
        # Instantiating tf_idf vectorizer
        tf_idf_vectorizer = TfidfVectorizer()

        # Fit and transform train data
        X_train_tf_idf = tf_idf_vectorizer.fit_transform(X_train['preprocessed_review'])
        # Only transform test data
        X_test_tf_idf = tf_idf_vectorizer.transform(X_test['preprocessed_review'])
        
        logging.info("TF-IDF vectorization complete")

        create_directories([self.config.tf_idf_vectorizer_path])
        save_bin(tf_idf_vectorizer, Path(os.path.join(self.config.tf_idf_vectorizer_path,"tf_idf_vectorizer_obj")))
        
        return (X_train_tf_idf, X_test_tf_idf)

    def perform_train_test_split(self, data):
        # Creating X and y data frames
        y = pd.DataFrame(data[self.config.target_column_name], columns=[self.config.target_column_name])
        X = pd.DataFrame(data["preprocessed_review"], columns=["preprocessed_review"])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = self.config.test_size, random_state=42)
        
        logging.info("Train test split complete")
        return (X_train, X_test, y_train, y_test)   

    def simplify_data_set(self, data):
        # Retain only 'ratings' & 'verified_reviews' columns
        data = data[[self.config.target_column_name,'verified_reviews']]
        # Ratings from 1 to 3 are mapped to 0 and rating 4 & 5 are mapped to 1
        data.loc[ : , [self.config.target_column_name]] = data[self.config.target_column_name].apply(lambda val : 0 if val <=3 else 1)
        
        logging.info("Simplifying the data set is done")
        return data
    
    def perform_text_preprocessing(self,text, lemmatizer, punc_to_remove, stop_words, speller):
        text = str(text)
        # Convert the text to lower case
        text = str(text.lower())
        # Remove punctutations
        text = str(" ".join([self.remove_punctuations(word, punc_to_remove) for word in text.split()]))
        # Remove stop words in the text
        text = str(" ".join([word for word in text.split() if word not in stop_words]))
        # Performing lemmatization on the text
        text = str(" ".join([lemmatizer.lemmatize(word) for word in text.split()]))
        # Perform spelling check
        text = str(" ".join([speller(word) for word in text.split()]))
        return text
    
    def get_required_preprocessing_objects(self):
        # Instantiating WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        # Contains all the punctuations that need to be removed
        punc_to_remove = list(string.punctuation)
        # Contains all the stop words that need to be removed
        stop_words = set(stopwords.words("English"))
        # Helps with correct spellings
        speller = Speller("en")
        logging.info("Fetched required preprocessing objects")
        return (lemmatizer, punc_to_remove, stop_words, speller)
    
    def remove_punctuations(self, word, punc_to_remove):
        cleaned_word = list()

        for letter in list(word):
            if letter not in punc_to_remove:
                cleaned_word.append(letter)
            
        return "".join(cleaned_word) 

        