import pandas as pd
import sys

# 📥 Lire les arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# 📄 Charger le fichier TSV
df = pd.read_csv(input_file, sep='\t')

# Extraire les colonnes H37Rv (col 3) et Lx (col 4)
col_h37rv = df.iloc[:, 2].astype(str).str.strip().str.upper()
col_lx    = df.iloc[:, 3].astype(str).str.strip().str.upper()

# Bases valides
valid_bases = {"A", "C", "G", "T"}

# Compteurs des scénarios
counts = {
    "1️⃣ N/N": 0,
    "2️⃣ base/gap": 0,
    "3️⃣ base/base": 0,
    "4️⃣ gap/N": 0,
    "5️⃣ gap/base": 0,
    "6️⃣ N/base": 0,
    "7️⃣ base/N": 0,
    "8️⃣ N/gap": 0
}

# Comparaison position par position
for b1, b2 in zip(col_h37rv, col_lx):
    if b1 == "N" and b2 == "N":
        counts["1️⃣ N/N"] += 1
    elif b1 in valid_bases and b2 == "-":
        counts["2️⃣ base/gap"] += 1
    elif b1 in valid_bases and b2 in valid_bases:
        counts["3️⃣ base/base"] += 1
    elif b1 == "-" and b2 == "N":
        counts["4️⃣ gap/N"] += 1
    elif b1 == "-" and b2 in valid_bases:
        counts["5️⃣ gap/base"] += 1
    elif b1 == "N" and b2 in valid_bases:
        counts["6️⃣ N/base"] += 1
    elif b1 in valid_bases and b2 == "N":
        counts["7️⃣ base/N"] += 1
    elif b1 == "N" and b2 == "-":
        counts["8️⃣ N/gap"] += 1

# Total pour fréquence
total = sum(counts.values())

# DataFrame de sortie
df_out = pd.DataFrame({
    "Scenario": list(counts.keys()),
    "Description": [
        "N et N identiques",
        "Base (A/C/G/T) alignée sur gap (-)",
        "Base alignée sur base",
        "Gap aligné sur N",
        "Gap aligné sur base",
        "N aligné sur base",
        "Base alignée sur N",
        "N aligné sur gap"
    ],
    "H37Rv": [
        "N", "A/C/G/T", "A/C/G/T", "-", "-", "N", "A/C/G/T", "N"
    ],
    "Lx": [
        "N", "-", "A/C/G/T", "N", "A/C/G/T", "A/C/G/T", "N", "-"
    ],
    "Count": list(counts.values()),
    "Frequency (%)": [round((v / total) * 100, 2) if total > 0 else 0 for v in counts.values()]
})

# Export en TSV
df_out.to_csv(output_file, sep='\t', index=False)

print(f"✅ Résultats enregistrés dans {output_file}")
