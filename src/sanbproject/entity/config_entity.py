from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root: Path
    raw_data_path: Path 
    extracted_data_path : Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root: Path
    full_data_set_path: Path
    test_size: float
    target_column_name: str
    all_columns: dict
    tf_idf_vectorizer_path: Path
    download_nltk_data: bool

@dataclass(frozen=True)
class ModelTrainerConfig:
    root: Path
    train_x_path: Path
    train_y_path: Path
    model_name: Path