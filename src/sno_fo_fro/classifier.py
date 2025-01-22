import random
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Dict
import h2o
import pandas as pd

PATH_TO_MODEL = "pretrained/GBM_2_AutoML_1_20250122_184812"


class WeatherClass(StrEnum):
    SNOW = "Snow"
    FOG = "Fog"
    FROST = "Frost"


class ImageClassifier(ABC):
    """
    Abstract base class for image classification.
    """

    @abstractmethod
    def classify(self, image_params: Dict[str, float]) -> str:
        """
        Abstract method to classify an image based on its parameters.

        :param image_params: A dictionary of image metrics (e.g., {"whiteness": 0.85, "blurriness": 0.4})
        :return: str value indicating the classification.
        """
        pass


class MockImageClassifier(ImageClassifier):
    """
    A concrete implementation of AbstractImageClassifier that randomly classifies images.
    """

    def classify(self, image_params: Dict[str, float]) -> str:
        return random.choice(list(WeatherClass))


class H2OMLClassifier(ImageClassifier):
    def __init__(self, model_path: str = PATH_TO_MODEL):
        """
        Initializes the H2OMLClassifier.

        :param model_path: The path to the saved H2O model (default is the path to the model saved in the repository)
        """
        self.model_path = model_path
        h2o.init()

    def format_dataframe(self, df):
        res = df.as_data_frame().to_dict()
        pred: str = res["predict"][0]
        fog = res["fogsmog"][0] * 100
        frost = res["frost"][0] * 100
        snow = res["snow"][0] * 100

        header = f"--- {pred.upper()} ---"
        ln = len(header)
        formatted_string = (
            f"{header}\n"
            f"snow: {snow:>{ln-6}.1f}%\n"
            f"frost: {frost:>{ln-7}.1f}%\n"
            f"fog: {fog:>{ln-5}.1f}%"
        )
        return formatted_string

    def classify(self, image_params: Dict[str, float]) -> str:
        loaded_model = h2o.load_model(self.model_path)
        pandas_df = pd.DataFrame(image_params, index=[0])
        h2o_df = h2o.H2OFrame(pandas_df)
        new_preds = loaded_model.predict(h2o_df)
        return self.format_dataframe(new_preds)
