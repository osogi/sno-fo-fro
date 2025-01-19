import random
from scipy import stats
from sno_fo_fro.experiment.experimenter import (
    Experimenter,
    ExperimenterCompareMode,
    ExperimenterWeather,
    SampleAnalyzer,
)
from sno_fo_fro.osogi_hypotheses import (
    ImageBlurrinessProcessor,
    ImageLuminanceProcessor,
    ImageContrastProcessor,
    ImageSaturationProcessor,
)


img_proc_and_idea = [
    (
        ImageBlurrinessProcessor(),
        (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS),
    ),
    (
        ImageLuminanceProcessor(),
        (ExperimenterWeather.FROST, ExperimenterCompareMode.GREATER),
    ),
    (ImageContrastProcessor(), (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS)),
    (
        ImageSaturationProcessor(),
        (ExperimenterWeather.FOG, ExperimenterCompareMode.LESS),
    ),
]


for img_proc, weather_and_mode in img_proc_and_idea:
    e = Experimenter(img_proc)
    e.analyze_samples(weather_and_mode[0], weather_and_mode[1])
