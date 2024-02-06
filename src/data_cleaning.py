import logging
from abc import ABC, abstractmethod 
from typing import Union
import numpy as np 
import pandas as pd
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split


class DataStrategy(ABC):
    """
    Abstract class for handling data
    """
    @abstractmethod
    def handle_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass

class CleanData(DataStrategy):
    """
    Class for cleaning data
    """
    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data
        """
        try:
            encoder = LabelEncoder()

            # Encoding 'sex' and 'smoker' columns
            data['sex'] = encoder.fit_transform(data['sex'])
            data['smoker'] = encoder.fit_transform(data['smoker'])
            
            # One hot encoding for 'region' column
            data = pd.get_dummies(data, columns=['region'], prefix='region')

            # Dropping less correlated columns based on the correlation matrix
            data = data.drop(
                ['region_southeast', 'region_southwest', 'region_northeast', 'region_northwest', 'children', 'sex'],
                axis=1
            )

            return data
        except Exception as e:
            logging.error(f"Error in cleaning data: {e}")
            raise e
        
class SplitData(DataStrategy):
    """
    Split the data into train and test sets
    """
    def handle_data(self, data: pd.DataFrame) -> Union[tuple, None]:
        """
        Split the data into training and test sets and return them.
        """
        try:
            y = data['charges']  # Target column
            X = data[['smoker', 'age', 'bmi']]  # Features
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error(f"Error in splitting data: {e}")
            raise e
