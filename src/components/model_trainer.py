import os
import sys
from dataclasses import dataclass
from pathlib import Path

from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models, save_object

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = str(PROJECT_ROOT / 'artifacts' / 'model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info('Split training and test input data')
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                'Linear Regression': LinearRegression(),
                'Lasso': Lasso(),
                'Ridge': Ridge(),
                'Decision Tree': DecisionTreeRegressor(),
                'Random Forest': RandomForestRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'KNN': KNeighborsRegressor(),
                'SVR': SVR(),
            }

            params = {
                'Linear Regression': {},
                'Lasso': {'alpha': [0.1, 1.0, 10.0]},
                'Ridge': {'alpha': [0.1, 1.0, 10.0]},
                'Decision Tree': {'max_depth': [3, 5, 10]},
                'Random Forest': {'n_estimators': [50, 100, 200]},
                'Gradient Boosting': {'learning_rate': [0.1, 0.05, 0.01]},
                'KNN': {'n_neighbors': [3, 5, 7]},
                'SVR': {'C': [0.1, 1.0, 10.0]},
            }

            logging.info('Starting model training')
            report = evaluate_models(X_train, y_train, X_test, y_test, models, params)
            logging.info(f'Model evaluation report: {report}')

            best_model_name, best_model_score = max(report.items(), key=lambda item: item[1])
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found", sys)

            logging.info("best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square
        except Exception as e:
            raise CustomException(e, sys)
