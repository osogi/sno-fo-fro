from abc import ABC, abstractmethod
import cv2
import numpy as np


class ImageProcessor(ABC):
    """
    Abstract base class (interface) for image processors that take an image
    and return a single float value.
    """

    @abstractmethod
    def process_image(self, image: np.ndarray) -> np.float32:
        """
        Processes the input image and returns a float value.

        Args:
            image: The input image as a NumPy array (OpenCV format).

        Returns:
            A float value representing the result of the image processing.
        """
        pass  # This makes it an abstract method

    def process_image_by_path(self, path: str) -> np.float32:
        img = cv2.imread(path)
        if img is None:
            print(f"Error: Could not read image at {path}")
        return self.process_image(img)
