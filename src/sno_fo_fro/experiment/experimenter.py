import numpy as np
from scipy import stats
from enum import StrEnum


class ExperimenterCompareMode(StrEnum):
    """
    Enum for specifying the comparison in tests.

    LESS:  Checks if the chosen (or first) sample is less than the second.
    GREATER: Checks if the  chosen (or first) sample is greater than the second.
    """

    LESS = "less"
    GREATER = "greater"



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
        return stats.ks_2samp(self.sample1, self.sample2, alternative=self.mode)
