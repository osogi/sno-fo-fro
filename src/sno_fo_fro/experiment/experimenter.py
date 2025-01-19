import os
import numpy as np
from scipy import stats
from enum import StrEnum

from sno_fo_fro.core import ImageProcessor


class ExperimenterCompareMode(StrEnum):
    """
    Enum for specifying the comparison in tests.

    LESS:  Checks if the main (or first) sample is less than the other.
    GREATER: Checks if the  main (or first) sample is greater than the oeher.
    """

    LESS = "less"
    GREATER = "greater"

    def invert(self):
        if self == self.LESS:
            return self.GREATER
        elif self == self.GREATER:
            return self.LESS
        else:
            return self


class ExperimenterWeather(StrEnum):
    """
    Enum for specifying the type of weather sample in tests.

    SNOW
    FOG
    FROST
    """

    SNOW = "snow"
    FOG = "fogsmog"
    FROST = "frost"


class Experimenter:
    def __init__(
        self,
        img_proc: ImageProcessor,
        parent_dir: str = "weather-data",
    ):
        self.img_proc = img_proc

        self.weather_samples = {}
        for weather in ExperimenterWeather:
            dir_path = os.path.join(parent_dir, weather)
            sample = img_proc.process_images_in_dir(dir_path)
            self.weather_samples[weather] = np.array(sample)

    def check_test_res(
        self, pval: np.floating, alpha: np.floating = np.float32(0.05)
    ) -> bool:
        return bool(pval < alpha)

    def string_test_res(self, res: bool) -> str:
        if res:
            return "passed"
        else:
            return "failed"

    def analyze_pair_samples(
        self,
        main_sample: np.typing.ArrayLike,
        other_sample: np.typing.ArrayLike,
        mode: ExperimenterCompareMode,
    ) -> bool:
        analyzer = SampleAnalyzer(main_sample, other_sample, mode)
        passed = True

        if analyzer.is_normal():
            print("Both samples have a normal distribution.")

            res = analyzer.t_test()
            cur_pas = self.check_test_res(res.pvalue)
            passed &= cur_pas
            print(f"\n### Two-sample t-test: {self.string_test_res(cur_pas)}")
            print(res)

            res = analyzer.ks_2samp()
            cur_pas = self.check_test_res(res.pvalue)
            passed &= cur_pas
            print(
                f"\n### Two-sample Kolmogorov-Smirnov: {self.string_test_res(cur_pas)}"
            )
            print(res)

        else:
            print("Both samples have not a normal distribution.")

            res = analyzer.mannwhitneyu()
            cur_pas = self.check_test_res(res.pvalue)
            passed &= cur_pas
            print(f"\n### Mann-Whitney U test: {self.string_test_res(cur_pas)}")
            print(res)

            res = analyzer.ks_2samp()
            cur_pas = self.check_test_res(res.pvalue)
            passed &= cur_pas
            print(
                f"\n### Two-sample Kolmogorov-Smirnov: {self.string_test_res(cur_pas)}"
            )
            print(res)

        return passed

    def analyze_samples(
        self, main_weather: ExperimenterWeather, mode: ExperimenterCompareMode
    ):
        print(f"\n# Analyze result for proc '{self.img_proc.__class__.__name__}'")
        passed = True
        for other_weather in ExperimenterWeather:
            if other_weather != main_weather:
                print(f"\n## Analyze '{main_weather}' {mode} '{other_weather}'")
                passed &= self.analyze_pair_samples(
                    self.weather_samples[main_weather],
                    self.weather_samples[other_weather],
                    mode,
                )
        print("\n## Conclusion")
        if passed:
            print(
                f"All tests passed. The hypothesis of ImageProcessor {self.img_proc.__class__.__name__} is accepted."
            )
        else:
            print(
                f"Some tests failed. The hypothesis of ImageProcessor {self.img_proc.__class__.__name__} is rejected."
            )


class SampleAnalyzer:
    """
    Class for performing statistical tests on two samples.

    Allows checking the normality of data distribution in samples,
    and comparing samples using various criteria.
    """

    def __init__(
        self,
        sample1: np.typing.ArrayLike,
        sample2: np.typing.ArrayLike,
        mode: ExperimenterCompareMode,
    ):
        """
        Initializes an instance of the SmallExperimenter class.

        Args:
            sample1: The first data sample (e.g., a NumPy array).
            sample2: The second data sample (e.g., a NumPy array).
            mode: The comparison direction for one-sided tests ('less' or 'greater').
                Defines the alternative hypothesis.
        """
        self.sample1 = np.array(sample1)  # Convert to NumPy arrays for reliability
        self.sample2 = np.array(sample2)
        self.mode = mode

    def is_normal(self) -> bool:
        """
        Checks if both samples are normally distributed.

        Uses a combination of tests: normaltest (D'Agostino-Pearson) and Shapiro-Wilk.
        Samples are considered normally distributed if the p-value of both tests
        for both samples is greater than the significance level alpha (0.05).

        Returns:
            True if both samples meet the normality criteria,
            False otherwise.
        """
        res = True
        alpha = 0.05

        # D'Agostino-Pearson test
        stat_res = stats.normaltest(self.sample1)
        res &= stat_res.pvalue > alpha
        stat_res = stats.normaltest(self.sample2)
        res &= stat_res.pvalue > alpha

        # Shapiro-Wilk test
        stat_res = stats.shapiro(self.sample1)
        res &= stat_res.pvalue > alpha
        stat_res = stats.shapiro(self.sample2)
        res &= stat_res.pvalue > alpha

        return res

    def mannwhitneyu(self):
        """
        Performs the Mann-Whitney U test to compare two independent samples.

        This test is non-parametric and does not require data normality.

        Returns:
            The result of the scipy.stats.mannwhitneyu function.
        """
        return stats.mannwhitneyu(self.sample1, self.sample2, alternative=self.mode)

    def ks_2samp(self):
        """
        Performs the two-sample Kolmogorov-Smirnov test to compare two independent samples.

        This test is non-parametric and does not require data normality.
        Checks if the distribution functions of the two samples differ.

        Returns:
            The result of the scipy.stats.ks_2samp function.
        """
        return stats.ks_2samp(self.sample1, self.sample2, alternative=self.mode.invert())

    def t_test(self):
        """
        Performs the two-sample t-test to compare the means of two independent samples.

        If the normality assumption is not met, consider using a non-parametric test instead.

        Returns:
            The result of the scipy.stats.ttest_ind function.
        """

        return stats.ttest_ind(
            self.sample1, self.sample2, alternative=self.mode, equal_var=False
        )
