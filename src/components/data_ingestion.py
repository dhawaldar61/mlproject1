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
from src.logger import configure_logging, logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv(PROJECT_ROOT / 'notebook' / 'data' / 'stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(PROJECT_ROOT / 'artifacts', exist_ok=True)

            df.to_csv(PROJECT_ROOT / self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(PROJECT_ROOT / self.ingestion_config.train_data_path, index=False, header=True)

            test_set.to_csv(PROJECT_ROOT / self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Inmgestion of the data iss completed")

            return (
                str(PROJECT_ROOT / self.ingestion_config.train_data_path),
                str(PROJECT_ROOT / self.ingestion_config.test_data_path)
            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    configure_logging()
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))


