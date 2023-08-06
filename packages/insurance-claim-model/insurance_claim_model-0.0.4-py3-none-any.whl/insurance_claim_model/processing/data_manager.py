import os
from pathlib import Path
from typing import List

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from insurance_claim_model import __version__
from insurance_claim_model.config.core import TRAINED_MODEL_DIR, config


def load_dataset(*, file_name: Path) -> pd.DataFrame:

    data = pd.read_csv(file_name)
    data.drop(["index", "PatientID"], axis=1, inplace=True)

    return data


def save_pipeline(*, pipeline: Pipeline) -> None:

    pipeline_name = f"{config.app_config.pipeline_save_file}-{__version__}.pkl"
    pipeline_to_persist = TRAINED_MODEL_DIR / pipeline_name

    remove_old_pipeline(files_to_keep=[pipeline_name])
    joblib.dump(pipeline, pipeline_to_persist)


def load_pipeline(*, pipeline_save_file: str) -> Pipeline:

    pipeline_path = TRAINED_MODEL_DIR / pipeline_save_file
    pipeline = joblib.load(pipeline_path)

    return pipeline


def remove_old_pipeline(*, files_to_keep: List[str]) -> None:

    files_to_keep = files_to_keep + ["__init__.py"]
    for file in os.listdir(TRAINED_MODEL_DIR):
        if file not in files_to_keep:
            os.unlink(Path(TRAINED_MODEL_DIR / file))
