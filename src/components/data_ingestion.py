import pandas as pd
import numpy as np
import os
import sys
from src.logger import logging
from src.exception import CustomException


class DataIngestion:
    def __init__(self, file_path, target_column, reference_value, deviated_value):
        self.file_path = file_path
        self.target_column = target_column
        self.reference_value = reference_value
        self.deviated_value = deviated_value

    def load_data(self):
        try:
            # Get file extension to determine the format
            _, file_extension = os.path.splitext(self.file_path.lower())

            # Load data based on file extension
            if file_extension == '.xlsx' or file_extension == '.xls':
                df = pd.read_excel(self.file_path)
            elif file_extension == '.csv':
                df = pd.read_csv(self.file_path)
            elif file_extension == '.tsv' or file_extension == '.txt':
                df = pd.read_csv(self.file_path, sep='\t')
            else:
                raise CustomException(f"Unsupported file format: {file_extension}")

            feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            df_ref = df[df[self.target_column] == self.reference_value].reset_index(drop=True)
            df_dev = df[df[self.target_column] == self.deviated_value].reset_index(drop=True)

            logging.info(f"Data successfully loaded from {self.file_path}")
            return df_ref, df_dev, feature_cols

        except Exception as e:
            raise CustomException(e,sys)