from typing import Tuple
from sno_fo_fro.experiment.experimenter import (
    Experimenter,
    ExperimenterCompareMode,
    ExperimenterWeather,
)
from sno_fo_fro.hypotheses import (
    ImageBlurrinessProcessor,
    ImageLuminanceProcessor,
    ImageContrastProcessor,
    ImageSaturationProcessor,
    ImageSegmentsSharpnessProcessor,
    ImageWhitenessProcessor,
    ImageWhiteGradientProcessor,
    ImageColdnessProcessor,
    ImageEdgeDensityProcessor,
)
from sno_fo_fro.image_processor import ImageProcessor


img_proc_and_idea: list[
    Tuple[ImageProcessor, Tuple[ExperimenterWeather, ExperimenterCompareMode]]
] = [
    (
        ImageBlurrinessProcessor(),
        (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS),
    ),
    (
        ImageLuminanceProcessor(False),
        (ExperimenterWeather.FROST, ExperimenterCompareMode.GREATER),
    ),
    (
        ImageLuminanceProcessor(True),
        (ExperimenterWeather.FROST, ExperimenterCompareMode.GREATER),
    ),
    (ImageContrastProcessor(), (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS)),
    (
        ImageSaturationProcessor(),
        (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS),
    ),
    (
        ImageWhiteGradientProcessor(),
        (ExperimenterWeather.SNOW, ExperimenterCompareMode.GREATER),
    ),
    (
        ImageWhitenessProcessor(),
        (ExperimenterWeather.SNOW, ExperimenterCompareMode.GREATER),
    ),
    (
        ImageColdnessProcessor(),
        (ExperimenterWeather.FROST, ExperimenterCompareMode.LESS),
    ),
    (
        ImageEdgeDensityProcessor(),
        (ExperimenterWeather.FROST, ExperimenterCompareMode.GREATER),
    ),
    (
        ImageSegmentsSharpnessProcessor(),
        (ExperimenterWeather.SNOW, ExperimenterCompareMode.GREATER),
    ),
]


for img_proc, weather_and_mode in img_proc_and_idea:
    e = Experimenter(img_proc)
    e.analyze_samples(weather_and_mode[0], weather_and_mode[1])
