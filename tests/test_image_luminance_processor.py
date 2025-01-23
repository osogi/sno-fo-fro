import numpy as np
from sno_fo_fro.hypotheses import ImageLuminanceProcessor
from utils import EPS


def test_black_image_default():
    black_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = ImageLuminanceProcessor().process_image(black_img)
    assert abs(result) < EPS


def test_white_image_default():
    white_img = np.full((100, 100, 3), 255, dtype=np.uint8)
    result = ImageLuminanceProcessor().process_image(white_img)
    assert abs(result - 255.0) < EPS


def test_mid_gray_image_default():
    gray_img = np.full((100, 100, 3), 128, dtype=np.uint8)
    result = ImageLuminanceProcessor().process_image(gray_img)
    assert abs(result - 128.0) < EPS
