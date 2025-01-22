import numpy as np
import cv2

from sno_fo_fro.hypotheses import ImageSaturationProcessor
from utils import EPS


def test_black_image():
    processor = ImageSaturationProcessor()
    black_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = processor.process_image(black_img)
    assert abs(result) < EPS


def test_white_image():
    processor = ImageSaturationProcessor()
    white_img = np.full((100, 100, 3), 255, dtype=np.uint8)
    result = processor.process_image(white_img)
    assert abs(result) < EPS


def test_red_image():
    processor = ImageSaturationProcessor()
    red_img = np.zeros((100, 100, 3), dtype=np.uint8)
    red_img[:, :] = (0, 0, 255)
    result = processor.process_image(red_img)
    assert abs(result - 255) < EPS


def test_half_saturated_color():
    processor = ImageSaturationProcessor()
    hsv_pixel = np.array([[[60, 128, 255]]], dtype=np.uint8)
    bgr_pixel = cv2.cvtColor(hsv_pixel, cv2.COLOR_HSV2BGR)
    color_img = np.tile(bgr_pixel, (100, 100, 1))
    result = processor.process_image(color_img)
    assert abs(result - 128) < EPS
