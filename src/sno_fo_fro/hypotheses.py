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


class ImageWhitenessProcessor(ImageProcessor):
    """
    Image processor that calculates the relative number of pixels that look white.
    White is defined as pixels with high value (brightness) and low saturation.
    """

    def __init__(self, value_threshold: float = 200, saturation_threshold: float = 50):
        """
        Initializes the ImageWhitenessProcessor.

        Args:
            value_threshold: The minimum value (brightness) for a pixel to be considered white.
            saturation_threshold: The maximum saturation for a pixel to be considered white.
        """
        self.value_threshold = value_threshold
        self.saturation_threshold = saturation_threshold

    def process_image(self, image: np.ndarray) -> np.float32:
        """
        Processes the image to calculate the relative number of white pixels.

        Args:
            image: The input image as a NumPy array (OpenCV format).

        Returns:
            A float value representing the fraction of white pixels in the image.
        """
        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Split the HSV image into hue, saturation, and value channels
        h, s, v = cv2.split(hsv_image)

        # Define a mask for white pixels: high value and low saturation
        white_mask = (v >= self.value_threshold) & (s <= self.saturation_threshold)

        # Calculate the fraction of white pixels
        white_pixel_count = np.sum(white_mask)
        total_pixels = image.shape[0] * image.shape[1]
        white_fraction = white_pixel_count / total_pixels

        return np.float32(white_fraction)


class ImageWhiteNoiseProcessor(ImageBlurrinessProcessor):

    def process_image(self, image: np.ndarray) -> np.float32:

        # 2. Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 3. Extract Saturation and Value channels
        saturation_channel = hsv_image[:, :, 1].astype(
            np.float32
        )  # Channel 1 is Saturation in HSV (OpenCV)
        value_channel = hsv_image[:, :, 2].astype(
            np.float32
        )  # Channel 2 is Value in HSV (OpenCV)

        # 4. Calculate Gradients for Saturation Channel
        # Using Sobel operator for gradient calculation - you can use other methods like Scharr, Prewitt, etc.
        grad_saturation_x = cv2.Sobel(
            saturation_channel, cv2.CV_64F, 1, 0, ksize=3
        )  # Gradient in x-direction
        grad_saturation_y = cv2.Sobel(
            saturation_channel, cv2.CV_64F, 0, 1, ksize=3
        )  # Gradient in y-direction

        # Calculate gradient magnitude for Saturation
        saturation_gradient_magnitude = np.sqrt(
            grad_saturation_x**2 + grad_saturation_y**2
        )

        # 5. Calculate Gradients for Value Channel
        grad_value_x = cv2.Sobel(
            value_channel, cv2.CV_64F, 1, 0, ksize=3
        )  # Gradient in x-direction
        grad_value_y = cv2.Sobel(
            value_channel, cv2.CV_64F, 0, 1, ksize=3
        )  # Gradient in y-direction

        # Calculate gradient magnitude for Value
        value_gradient_magnitude = np.sqrt(grad_value_x**2 + grad_value_y**2)

        whiteness_of_pixel = value_channel / np.maximum(saturation_channel, 1)

        grad_mult = (
            saturation_gradient_magnitude
            * value_gradient_magnitude
            * whiteness_of_pixel
        )
        return grad_mult.std()
