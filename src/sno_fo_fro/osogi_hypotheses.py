import cv2
import numpy as np
from src.sno_fo_fro.core import ImageProcessor


class ImageLuminanceProcessor(ImageProcessor):
    """
    Calculates the average perceived luminance of an image.
    """

    def process_image(self, image: np.ndarray) -> np.float32:
        """
        Calculates the average luminance of the input image.

        Args:
            image: The input image as a NumPy array (OpenCV BGR format).

        Returns:
            The average luminance of the image.  Returns -1 on error.
        """

        if len(image.shape) != 3 or image.shape[2] != 3:
            raise TypeError("Error: Image must have 3 color channels (BGR).")

        # Split the image into its B, G, and R channels (float for accuracy)
        blue_channel = image[:, :, 0].astype(np.float64)
        green_channel = image[:, :, 1].astype(np.float64)
        red_channel = image[:, :, 2].astype(np.float64)

        # Calculate the luminance using the weighted sum formula
        luminance = (
            0.2126 * red_channel + 0.7152 * green_channel + 0.0722 * blue_channel
        )

        # Calculate the average luminance
        average_luminance = np.mean(luminance)

        return average_luminance


class ImageContrastProcessor(ImageProcessor):
    """
    Calculates the contrast of an image.
    """

    def process_image(self, image: np.ndarray) -> np.float32:
        """
        Calculates the contrast of an image by measuring the standard deviation of pixel intensities (Root mean square contrast).

        Args:
            image: The input image as a NumPy array (OpenCV format).

        Returns:
            A float value representing the image contrast. Higher values indicate higher contrast.
        """
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Return the standard deviation as the contrast value
        contrast = gray_image.var()
        return contrast


class ImageSaturationProcessor(ImageProcessor):
    """
    Calculates the average saturation of an image.
    """

    def process_image(self, image: np.ndarray) -> np.float32:
        """
        Calculates the saturation of an image.

        Args:
            image: The input image as a NumPy array (OpenCV format).

        Returns:
            A float value representing the image saturation. Higher values indicate higher saturation.
        """
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        saturation = img_hsv[:, :, 1].mean()
        return saturation


class ImageBlurrinessProcessor(ImageProcessor):
    """
    Calculates the blurriness of an image.
    """

    def process_image(self, image: np.ndarray) -> np.float32:
        """
        Calculates the blurriness of an image.

        Args:
            image: The input image as a NumPy array (OpenCV format).

        Returns:
            A float value representing the image saturation. Higher values indicate less blurriness.
        """
        return cv2.Laplacian(image, cv2.CV_64F).var()
