import pandas as pd
import numpy as np
import os
import sys
from src.logger import logging
from src.exception import CustomException


class DataIngestion:
    def __init__(self, file, filename, target_column, reference_value, deviated_value):
        self.file = file
        self.filename = filename
        self.target_column = target_column
        self.reference_value = reference_value
        self.deviated_value = deviated_value

    def load_data(self):
        try:
            file_extension = os.path.splitext(self.filename.lower())[1]

            logging.info(f"Detected file format: {file_extension}")
            if file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(self.file, engine='openpyxl')
            elif file_extension == '.csv':
                df = pd.read_csv(self.file)
            elif file_extension in ['.tsv', '.txt']:
                df = pd.read_csv(self.file, sep='\t')
            else:
                raise CustomException(f"Unsupported file format: {file_extension}")

            feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            df_ref = df[df[self.target_column] == self.reference_value].reset_index(drop=True)
            df_dev = df[df[self.target_column] == self.deviated_value].reset_index(drop=True)

            return df_ref, df_dev, feature_cols

        except Exception as e:
            raise CustomException(e, sys)
