import random
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Dict


class WeatherClass(StrEnum):
    SNOW = "Snow"
    FOG = "Fog"
    FROST = "Frost"


class ImageClassifier(ABC):
    """
    Abstract base class for image classification.
    """

    @abstractmethod
    def classify(self, image_params: Dict[str, float]) -> WeatherClass:
        """
        Abstract method to classify an image based on its parameters.

        :param image_params: A dictionary of image metrics (e.g., {"whiteness": 0.85, "blurriness": 0.4})
        :return: WeatherClass enum value indicating the classification.
        """
        pass


class MockImageClassifier(ImageClassifier):
    """
    A concrete implementation of AbstractImageClassifier that randomly classifies images.
    """

    def classify(self, image_params: Dict[str, float]) -> WeatherClass:

        return random.choice(list(WeatherClass))
