
import argparse
import os
import pandas as pd
import re

def merge_scenario_tables(output_file):
    folder = "."
    pattern = r"scenarios_table_H37Rv_(.+)_mask\.tsv"
    all_files = [f for f in os.listdir(folder) if re.match(pattern, f)]

    merged_df = None
    for file in all_files:
        sample_name = re.match(pattern, file).group(1)
        df = pd.read_csv(os.path.join(folder, file), sep="\t", usecols=["Scenario", "Count"])
        df.rename(columns={"Count": sample_name}, inplace=True)

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on="Scenario", how="outer")

    merged_df.to_csv(output_file, index=False)
    print(f"✅ Merged scenario table saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='SGLLab-Merge: Merge multiple scenario count files into a summary.')
    parser.add_argument('--output', default='combined_scenarios_counts.csv', help='Output merged CSV file (default: combined_scenarios_counts.csv)')
    args = parser.parse_args()

    merge_scenario_tables(args.output)

if __name__ == '__main__':
    main()
