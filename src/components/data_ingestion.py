import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import configure_logging

configure_logging()


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            data_path = PROJECT_ROOT / 'notebook' / 'data' / 'stud.csv'
            df = pd.read_csv(data_path)
            logging.info('Read the dataset as dataframe')

            os.makedirs(PROJECT_ROOT / 'artifacts', exist_ok=True)

            df.to_csv(PROJECT_ROOT / self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Raw data saved successfully")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(PROJECT_ROOT / self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(PROJECT_ROOT / self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Train and test data saved successfully")

            return (
                str(PROJECT_ROOT / self.ingestion_config.train_data_path),
                str(PROJECT_ROOT / self.ingestion_config.test_data_path)
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()