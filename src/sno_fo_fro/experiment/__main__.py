import random
from scipy import stats
from sno_fo_fro.experiment.experimenter import (
    Experimenter,
    ExperimenterCompareMode,
    ExperimenterWeather,
    SampleAnalyzer,
)
from sno_fo_fro.hypotheses import (
    ImageBlurrinessProcessor,
    ImageLuminanceProcessor,
    ImageContrastProcessor,
    ImageSaturationProcessor,
    ImageSegmentsProcessor,
    ImageWhitenessProcessor,
    ImageWhiteNoiseProcessor,
    ImageColdnessProcessor,
    ImageEdgeDensityProcessor,
)


img_proc_and_idea = [
    # (
    #     ImageBlurrinessProcessor(),
    #     (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS),
    # ),
    # (
    #     ImageLuminanceProcessor(False),
    #     (ExperimenterWeather.FROST, ExperimenterCompareMode.GREATER),
    # ),
    # (
    #     ImageLuminanceProcessor(True),
    #     (ExperimenterWeather.FROST, ExperimenterCompareMode.GREATER),
    # ),
    # (ImageContrastProcessor(), (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS)),
    # (
    #     ImageSaturationProcessor(),
    #     (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS),
    # ),
    # (
    #     ImageWhiteNoiseProcessor(),
    #     (ExperimenterWeather.SNOW, ExperimenterCompareMode.GREATER),
    # ),
    # (
    #     ImageWhitenessProcessor(),
    #     (ExperimenterWeather.SNOW, ExperimenterCompareMode.GREATER),
    # ),
    # (
    #     ImageColdnessProcessor(),
    #     (ExperimenterWeather.FROST, ExperimenterCompareMode.LESS),
    # ),
    # (
    #     ImageEdgeDensityProcessor(),
    #     (ExperimenterWeather.FROST, ExperimenterCompareMode.GREATER),
    # ),
    (
        ImageSegmentsProcessor(),
        (ExperimenterWeather.SNOW, ExperimenterCompareMode.GREATER),
    ),
]


for img_proc, weather_and_mode in img_proc_and_idea:
    e = Experimenter(img_proc)
    e.analyze_samples(weather_and_mode[0], weather_and_mode[1])
