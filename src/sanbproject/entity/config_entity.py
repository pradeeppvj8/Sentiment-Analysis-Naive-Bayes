from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root: Path
    raw_data_path: Path 
    extracted_data_path : Path