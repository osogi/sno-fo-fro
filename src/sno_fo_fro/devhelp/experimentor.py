import os
from sno_fo_fro.image_processor import ImageProcessor
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from sno_fo_fro.hypotheses import (
    ImageBlurrinessProcessor,
    ImageColdnessProcessor,
    ImageEdgeDensityProcessor,
    ImageLuminanceProcessor,
    ImageContrastProcessor,
    ImageSaturationProcessor,
    ImageSegmentsSharpnessProcessor,
    ImageWhitenessProcessor,
    ImageWhiteGradientProcessor,
)
import sys


class FolderProcessor:
    """
    Processes images in multiple folders using an ImageProcessor and saves the results to text files.
    """

    def __init__(self, processor: ImageProcessor):
        """
        Initializes the FolderProcessor with an ImageProcessor.

        Args:
            processor: An instance of an ImageProcessor subclass.
        """
        self.processor = processor

    def process_folders(self, folder_paths: List[str], output_dir: str = "results"):
        """
        Processes images in the specified folders and saves the results to text files.

        Args:
            folder_paths: A list of paths to the folders containing images.
            output_dir: The directory where the output text files will be saved.
        """
        os.makedirs(output_dir, exist_ok=True)

        for folder_path in folder_paths:
            results = self.processor.process_images_in_dir(folder_path)

            output_filename = f"{os.path.basename(folder_path)}.txt"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "w") as f:
                for result in results:
                    f.write(f"{result}\n")

            print(
                f"Processed {len(results)} images in {folder_path}. Results saved to {output_path}"
            )


class HistogramBuilder:
    """
    Processes text files with numerical data, builds histograms, and calculates basic statistics.
    """

    def build_histograms_for_processor(self, processor_dir: str, bins: int = 20):
        """
        Processes text files for a specific processor, builds histograms for each folder on one figure,
        and calculates statistics.

        Args:
            processor_name: The name of the processor for which to build histograms.
            bins: The number of bins for the histogram.
        """

        processor_name = os.path.basename(processor_dir)

        # Get a list of folders (text files) for the given processor
        if not os.path.isdir(processor_dir):
            print(f"No directory found: {processor_dir}")
            return

        folder_names = [
            os.path.splitext(filename)[0]
            for filename in os.listdir(processor_dir)
            if filename.endswith(".txt")
        ]

        if not folder_names:
            print(f"No data files found for directory: {processor_dir}")
            return

        # Create subplots for each folder
        num_folders = len(folder_names)
        fig, axes = plt.subplots(
            1, num_folders, figsize=(5 * num_folders, 4), squeeze=False
        )
        axes = axes.flatten()  # Flatten for easier indexing

        for i, folder_name in enumerate(folder_names):
            filepath = os.path.join(processor_dir, f"{folder_name}.txt")
            with open(filepath, "r") as f:
                data = [float(line.strip()) for line in f if line.strip()]

            if not data:
                print(f"No data found in {filepath}. Skipping.")
                continue

            # Plot histogram on the corresponding subplot
            ax = axes[i]
            ax.hist(data, bins=bins, edgecolor="black")
            ax.set_title(f"{folder_name}")
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            ax.grid(True)

            # Print statistics
            self.print_statistics(data, (processor_name), folder_name)

        # Set overall title and adjust layout
        fig.suptitle(f"Histograms for {processor_name}", fontsize=16)
        plt.tight_layout(
            rect=(0.0, 0.03, 1.0, 0.95)
        )  # Adjust to prevent overlap with suptitle
        plt.savefig(f"{processor_dir}/histograms.png")
        # plt.show()

    def print_statistics(
        self, data: List[float], processor_name: str, folder_name: str
    ):
        """
        Calculates and prints basic statistics for the given data.

        Args:
            data: A list of numerical data.
            processor_name: The name of the processor.
            folder_name: The name of the folder.
        """
        mean = np.mean(data)
        min_val = np.min(data)
        max_val = np.max(data)
        std_dev = np.std(data)
        median = np.median(data)

        print(f"Statistics for {processor_name} on {folder_name}:")
        print(f"  Mean: {mean:.4f}")
        print(f"  Median: {median:.4f}")
        print(f"  Min: {min_val:.4f}")
        print(f"  Max: {max_val:.4f}")
        print(f"  Standard Deviation: {std_dev:.4f}")
        print("-" * 20)


# using: cd <project_dir>
# rye run python -m src.sno_fo_fro.devhelp.experimentor
if __name__ == "__main__":
    img_proc = ImageSegmentsSharpnessProcessor()
    outputfolder = f"result/{img_proc.__class__.__name__}"

    parent_dir = "weather-data"
    if len(sys.argv) > 1:
        parent_dir = sys.argv[1]
    subs = ["fogsmog", "frost", "snow"]
    target_dirs = [os.path.join(parent_dir, sub_dir) for sub_dir in subs]

    dir_proc = FolderProcessor(img_proc)
    dir_proc.process_folders(target_dirs, outputfolder)

    hd = HistogramBuilder()
    hd.build_histograms_for_processor(outputfolder)
