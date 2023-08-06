from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from insurance_claim_model.config.core import DATASET_DIR, config
from insurance_claim_model.pipeline import predict_pipe
from insurance_claim_model.processing.data_manager import load_dataset, save_pipeline


def run_training(*, training_data_file: Path) -> None:
    data = load_dataset(file_name=training_data_file)
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    y_train = np.log(y_train)
    predict_pipe.fit(X_train, y_train)

    save_pipeline(pipeline=predict_pipe)


if __name__ == "__main__":
    training_data_file = DATASET_DIR / config.app_config.training_data_file
    run_training(training_data_file=training_data_file)
