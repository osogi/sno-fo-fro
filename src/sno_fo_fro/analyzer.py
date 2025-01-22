
from numpy import ndarray
from sno_fo_fro.hypotheses import (
    ImageBlurrinessProcessor,
    ImageColdnessProcessor,
    ImageContrastProcessor,
    ImageEdgeDensityProcessor,
    ImageSaturationProcessor,
    ImageSegmentsSharpnessProcessor,
    ImageWhiteGradientProcessor,
    ImageWhitenessProcessor,
)
from sno_fo_fro.image_processor import ImageProcessor


class Metric:
    def __init__(self, name: str, img_proc: ImageProcessor):
        self.name = name
        self.img_proc = img_proc


METRIC_WHITENESS = Metric("WHITENESS", ImageWhitenessProcessor())
METRIC_BLURRINESS = Metric("BLURRINESS", ImageBlurrinessProcessor())
METRIC_CONTRAST = Metric("CONTRAST", ImageContrastProcessor())
METRIC_SATURATION = Metric("SATURATION", ImageSaturationProcessor())
METRIC_WHITE_GRADIENT = Metric("WHITE_GRADIENT", ImageWhiteGradientProcessor())
METRIC_COLDNESS = Metric("COLDNESS", ImageColdnessProcessor())
METRIC_EDGE_DENSITY = Metric("EDGE_DENSITY", ImageEdgeDensityProcessor())
METRIC_SEGMENTS_SHARPNESS = Metric(
    "SEGMENTS_SHARPNESS", ImageSegmentsSharpnessProcessor()
)


class CombinedImageProcessor[T](ImageProcessor):
    def __init__(self, metrics: list[Metric]):
        self.metrics = metrics

    def process_image(self, image: ndarray) -> dict[str, T]:
        result = {}
        for metric in self.metrics:
            result[metric.name] = metric.img_proc.process_image(image)

        return result


ImageAnalyzer = CombinedImageProcessor[float](
    [
        METRIC_WHITENESS,
        METRIC_BLURRINESS,
        METRIC_CONTRAST,
        METRIC_SATURATION,
        METRIC_WHITE_GRADIENT,
        METRIC_COLDNESS,
        METRIC_EDGE_DENSITY,
        METRIC_SEGMENTS_SHARPNESS,
    ]
)
