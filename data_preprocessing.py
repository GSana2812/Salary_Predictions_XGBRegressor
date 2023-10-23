import pandas as pd
from typing import Type, Dict, List
from descriptions import COMPANY_LOCATION, EMPLOYMENT_TYPE, EXPERIENCE_LEVEL, COMPANY_SIZE, EXPERIENCE_LEVEL_MAPPER, COMPANY_SIZE_MAPPER
from sklearn.preprocessing import OneHotEncoder
import warnings
from sklearn.model_selection import train_test_split
warnings.filterwarnings('ignore')
from xgboost import XGBRegressor
# Model Performance
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np


class DataPreprocessor:
    """
        DataPreprocessor class for data preprocessing operations.

        Parameters:
            data (pd.DataFrame): The input data for preprocessing.

        Methods:
            - top_10_countries(column: str) -> Type['DataPreprocessor']:
                Filters the data to include only the top 10 countries based on the given column.

            - select_salaries(column: str) -> Type['DataPreprocessor']:
                Filters the data to include only salary values within the range of 10,000 to 250,000.

            - reset_index() -> Type['DataPreprocessor']:
                Resets the index of the data.

            - map_column(col: str, updated_col: Dict[str,str]) -> None:
                Maps values in the specified column to the values in the provided dictionary.

            - drop_unnecessary_columns(cols: List[str]) -> Type['DataPreprocessor']:
                Drops the specified columns from the data.

            - get_unique_values(col: str) -> List[str]:
                Returns a list of unique values in the specified column.

            - one_hot_encode_df(cols: List[str]) -> Type['DataPreprocessor']:
                Performs one-hot encoding on the specified columns.

            - rename_columns(col_name: str, df_columns: List[str]) -> None:
                Renames columns based on the provided mapping.

            - concat_dataframes(data_1: pd.DataFrame, data_2: pd.DataFrame) -> pd.DataFrame:
                Concatenates two dataframes side by side.

            - print() -> None:
                Prints the first few rows of the preprocessed data.

        """

    def __init__(self, data):
        self.data = data

    def top_10_countries(self, column: str)-> Type['DataPreprocessor']:

        top_10_countries: pd.Series = self.data[column].value_counts().head(10).index
        filtered_data = self.data [self.data [column].isin(top_10_countries)]
        return DataPreprocessor(data = filtered_data)

    def select_salaries(self, column: str)-> Type['DataPreprocessor']:

        filtered_data: pd.DataFrame = self.data[(self.data[column] >= 10000) & (self.data[column] <= 250000)]
        return DataPreprocessor(data = filtered_data)

    def reset_index(self)-> Type['DataPreprocessor']:

        return DataPreprocessor(data = self.data.reset_index(drop=True))

    def map_column(self, col: str, updated_col: Dict[str,str])-> None:

        self.data[col] = self.data[col].map(updated_col)
        DataPreprocessor(data = self.data)

    def drop_unnecessary_columns(self, cols: List[str])-> Type['DataPreprocessor']:

        return DataPreprocessor(data = self.data.drop(columns = cols, axis=1))


    def get_unique_values(self, col: str)-> List[str]:

        return list(self.data[col].unique())

    def one_hot_encode_df(self, cols: List[str])-> Type['DataPreprocessor']:

        one_hot_encoder = OneHotEncoder(sparse=False)
        one_hot_encoder.fit(self.data[cols])
        transformed_data = one_hot_encoder.transform(self.data[cols])
        return  DataPreprocessor(data = pd.DataFrame(transformed_data, columns=one_hot_encoder.get_feature_names_out(cols)))

    def rename_columns(self, col_name: str, df_columns: List[str])-> None:

        DataPreprocessor(data = self.data.rename(columns={f'{df_columns}_{col}':col for col in col_name}, inplace=True))

    @staticmethod
    def concat_dataframes(data_1: pd.DataFrame, data_2: pd.DataFrame)-> pd.DataFrame:

        return DataPreprocessor(data = pd.concat([data_1, data_2], axis=1))


    def print(self):
        return self.data.head()




















