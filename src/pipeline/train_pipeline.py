from src.components.data_ingestion import DataIngestion
from src.components.model_trainer import ModelTrainer
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class TrainPipeline:
    def __init__(self, uploaded_file, target_column, reference_value, deviated_value, min_threshold=None,
                 max_threshold=None, output_path='calibrated_output.xlsx'):
        self.uploaded_file = uploaded_file
        self.target_column = target_column
        self.reference_value = reference_value
        self.deviated_value = deviated_value
        self.output_path = output_path
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    def run_pipeline(self):
        data_loader = DataIngestion(
            file=self.uploaded_file,
            filename=self.uploaded_file.name,
            target_column=self.target_column,
            reference_value=self.reference_value,
            deviated_value=self.deviated_value
        )

        df_ref, df_dev, feature_cols = data_loader.load_data()

        X_train = df_dev[feature_cols].values
        y_train = df_ref[feature_cols].values

        trainer = ModelTrainer(
            X_train_dev=X_train,
            y_train_ref=y_train,
            X_full_dev=df_dev[feature_cols].values,
            min_threshold=self.min_threshold,
            max_threshold=self.max_threshold
        )

        calibrated_data, best_model = trainer.train_and_calibrate()

        # Change threshold for users to make it dynamic

        # Final DataFrame
        df_calibrated = df_dev.copy()
        df_calibrated[feature_cols] = calibrated_data
        df_calibrated[self.target_column] = f'Calibrated({self.deviated_value})'

        df_export = pd.concat([df_ref, df_calibrated], ignore_index=True)
        df_export.to_excel(self.output_path, index=False)

        # Generating distribution plots per feature
        figures = []
        for col in feature_cols:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.kdeplot(df_dev[col], label="Original Deviated", ax=ax)
            sns.kdeplot(df_calibrated[col], label="Calibrated", ax=ax, color='black', linestyle=':')
            sns.kdeplot(df_ref[col], label="Reference", ax=ax, color='r', alpha=0.5)
            ax.set_title(f"{col} - Calibration Comparison")
            ax.legend()
            plt.tight_layout()
            figures.append(fig)

        return df_export, best_model, figures
