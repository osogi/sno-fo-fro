from abc import ABC, abstractmethod
import os
from typing import Dict
import cv2
import numpy as np


class ImageProcessor[T](ABC):
    """
    Abstract base class (interface) for image processors that take an image
    and return some metric value.
    """

    @abstractmethod
    def process_image(self, image: np.ndarray) -> T:
        """
        Processes the input image and returns some metric.

        Args:
            image: The input image as a NumPy array (OpenCV format).

        Returns:
            A metric value representing the result of the image processing.
        """
        pass  # This makes it an abstract method

    def process_image_by_path(self, path: str) -> T:
        img = cv2.imread(path)
        if img is None:
            print(f"Error: Could not read image at {path}")
        return self.process_image(img)

    def process_images_in_dir(self, dir_path: str) -> Dict[str, T]:
        results = {}
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")
            ):
                image_path = os.path.join(dir_path, filename)
                result = self.process_image_by_path(image_path)
                if result is not None:
                    results[image_path] = result

        return results
