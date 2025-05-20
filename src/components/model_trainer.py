from sklearn.linear_model import HuberRegressor
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class ModelTrainer:
    def __init__(self, X_train_dev, y_train_ref, X_full_dev, min_threshold=None, max_threshold=None):
        self.X_train_dev = X_train_dev
        self.y_train_ref = y_train_ref
        self.X_full_dev = X_full_dev
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    def train_and_calibrate(self):
        # Step 1: Scale using MinMax
        self.dev_scaler = MinMaxScaler()
        self.ref_scaler = MinMaxScaler()

        X_dev_scaled = self.dev_scaler.fit_transform(self.X_train_dev)
        y_ref_scaled = self.ref_scaler.fit_transform(self.y_train_ref)

        # Step 2: Train model
        self.models = [HuberRegressor().fit(X_dev_scaled[:, i].reshape(-1, 1), y_ref_scaled[:, i])
                       for i in range(X_dev_scaled.shape[1])]

        # Step 3: Predict on full dev set
        X_full_dev_scaled = self.dev_scaler.transform(self.X_full_dev)
        preds_scaled = np.column_stack([
            model.predict(X_full_dev_scaled[:, i].reshape(-1, 1))
            for i, model in enumerate(self.models)
        ])

        # Step 4: Inverse transform to get original scale
        preds_original = self.ref_scaler.inverse_transform(preds_scaled)

        # Step 5: Optional clipping
        if self.min_threshold is not None and self.max_threshold is not None:
            preds_original = np.clip(preds_original, self.min_threshold, self.max_threshold)

        return preds_original, "Huber (MinMax + Inverse)"
