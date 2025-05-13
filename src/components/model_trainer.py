import numpy as np
from sklearn.linear_model import HuberRegressor
from sklearn.metrics import mean_squared_error
from src.components.data_transformation import QuantileMapping, match_reference_stats
from src.logger import logging


class ModelTrainer:
    def __init__(self, X_train, y_train, X_full):
        self.X_train = X_train
        self.y_train = y_train
        self.X_full = X_full

    def train_and_calibrate(self):
        min_len = min(len(self.X_train), len(self.y_train))
        X_sample = self.X_train[:min_len]
        y_sample = self.y_train[:min_len]

        # Huber
        huber_models = [HuberRegressor().fit(X_sample[:, i].reshape(-1, 1), y_sample[:, i]) for i in
                        range(X_sample.shape[1])]
        huber_preds = np.column_stack([
            model.predict(self.X_full[:, i].reshape(-1, 1)) for i, model in enumerate(huber_models)
        ])

        # Quantile Mapping
        qm = QuantileMapping()
        qm.fit(X_sample, y_sample)
        qm_preds = qm.transform(self.X_full)

        # Evaluate
        mse_huber = mean_squared_error(y_sample, huber_preds[:min_len])
        mse_qm = mean_squared_error(y_sample, qm_preds[:min_len])
        logging.info(f"Huber MSE: {mse_huber:.2f}, Quantile Mapping MSE: {mse_qm:.2f}")

        best_preds = huber_preds if mse_huber < mse_qm else qm_preds
        best_preds = match_reference_stats(best_preds, y_sample)
        best_model = 'Huber' if mse_huber < mse_qm else 'Quantile Mapping'

        logging.info(f" Selected Model: {best_model}")
        return best_preds, best_model
