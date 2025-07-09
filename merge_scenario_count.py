import os
import pandas as pd
import re
import sys

# 🔁 Dossier à scanner ('.' = courant, ou adapte vers './results/', etc.)
folder = "."
pattern = r"scenarios_table_H37Rv_(.+)_mask\.tsv"

# Lister les fichiers correspondant au motif
all_files = [f for f in os.listdir(folder) if re.match(pattern, f)]

merged_df = None

for file in all_files:
    # Extraire le suffixe (ex: L1, L2, L6)
    sample_name = re.match(pattern, file).group(1)

    # Lire uniquement Scenario + Count
    df = pd.read_csv(os.path.join(folder, file), sep="\t", usecols=["Scenario", "Count"])
    df.rename(columns={"Count": sample_name}, inplace=True)

    # Fusion progressive sur la colonne 'Scenario'
    if merged_df is None:
        merged_df = df
    else:
        merged_df = pd.merge(merged_df, df, on="Scenario", how="outer")

# Sauvegarde du résultat
output_file = sys.argv[1] # "combined_scenarios_counts.csv"
merged_df.to_csv(output_file, index=False)
print(f"✅ Fichier fusionné sauvegardé : {output_file}")
