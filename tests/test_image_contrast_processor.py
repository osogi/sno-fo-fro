import numpy as np
import cv2

from sno_fo_fro.hypotheses import ImageContrastProcessor
from utils import EPS


def test_black_image():
    black_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = ImageContrastProcessor().process_image(black_img)
    assert abs(result) < EPS


def test_white_image():
    white_img = np.full((100, 100, 3), 255, dtype=np.uint8)
    result = ImageContrastProcessor().process_image(white_img)
    assert abs(result) < EPS


def test_gradient_image():
    gradient_img = np.tile(np.arange(256, dtype=np.uint8), (100, 1))
    gradient_img_bgr = cv2.merge([gradient_img, gradient_img, gradient_img])

    result = ImageContrastProcessor().process_image(gradient_img_bgr)
    print(result)
    assert result > 5000  # big value greater than 0
