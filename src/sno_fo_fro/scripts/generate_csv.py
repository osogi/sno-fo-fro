import os
import pandas as pd
from sno_fo_fro.analyzer import ImageAnalyzer


def generate_csv(input_dir="weather-data", output_file="metrics_table.csv"):
    class_directories = {"snow": "snow", "fogsmog": "fogsmog", "frost": "frost"}

    all_dfs = []
    for class_label, subdir in class_directories.items():
        dir_path = os.path.join(input_dir, subdir)
        metrics = ImageAnalyzer.process_images_in_dir(dir_path).values()

        df = pd.DataFrame(metrics)
        df["class_label"] = class_label
        all_dfs.append(df)

    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df = final_df.fillna(0)

    final_df.to_csv(output_file, index=False)
    print(f"CSV file saved: {output_file}")


if __name__ == "__main__":
    generate_csv()
