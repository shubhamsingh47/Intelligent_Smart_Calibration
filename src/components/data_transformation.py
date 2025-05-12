import numpy as np
from sklearn.preprocessing import QuantileTransformer


class QuantileMapping:
    def __init__(self):
        self.transformer = None
        self.source_scaler = None

    def fit(self, X_source, X_target):
        self.transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        self.transformer.fit(X_target)
        self.source_scaler = QuantileTransformer(output_distribution='normal', random_state=42)
        self.source_scaler.fit(X_source)

    def transform(self, X):
        normalized = self.source_scaler.transform(X)
        return self.transformer.inverse_transform(normalized)


def match_reference_stats(calibrated_data, reference_data):
    final_adjusted = np.zeros_like(calibrated_data)
    for i in range(calibrated_data.shape[1]):
        cal_mean, cal_std = np.mean(calibrated_data[:, i]), np.std(calibrated_data[:, i])
        ref_mean, ref_std = np.mean(reference_data[:, i]), np.std(reference_data[:, i])
        final_adjusted[:, i] = ((calibrated_data[:, i] - cal_mean) / (cal_std + 1e-8)) * ref_std + ref_mean
    return final_adjusted
