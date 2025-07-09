
import argparse
import pandas as pd

def count_scenarios(input_file, output_file):
    df = pd.read_csv(input_file, sep='\t')
    col_h37rv = df.iloc[:, 2].astype(str).str.strip().str.upper()
    col_lx    = df.iloc[:, 3].astype(str).str.strip().str.upper()

    valid_bases = {"A", "C", "G", "T"}
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

    total = sum(counts.values())
    df_out = pd.DataFrame({
        "Scenario": list(counts.keys()),
        "Description": [
            "N and N", "Base aligned to gap", "Base aligned to base", "Gap aligned to N",
            "Gap aligned to base", "N aligned to base", "Base aligned to N", "N aligned to gap"
        ],
        "H37Rv": ["N", "A/C/G/T", "A/C/G/T", "-", "-", "N", "A/C/G/T", "N"],
        "Lx": ["N", "-", "A/C/G/T", "N", "A/C/G/T", "A/C/G/T", "N", "-"],
        "Count": list(counts.values()),
        "Frequency (%)": [round((v / total) * 100, 2) if total > 0 else 0 for v in counts.values()]
    })
    df_out.to_csv(output_file, sep='\t', index=False)
    print(f"✅ Scenario counts saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='SGLLab-Count: Count allele scenarios from masked comparison table.')
    parser.add_argument('input_file', help='Masked input TSV file')
    parser.add_argument('output_file', help='Output TSV file with scenario counts')
    args = parser.parse_args()

    count_scenarios(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
