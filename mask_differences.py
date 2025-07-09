import sys
def load_bed_intervals(bed_file):
    """Charge un fichier BED (avec contig) et retourne une liste de tuples (start, end)"""
    intervals = []
    with open(bed_file) as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue  # ignorer les lignes incomplètes
            start, end = int(parts[1]), int(parts[2])
            intervals.append((start + 1, end))  # convertir en 1-based inclusif
    return intervals

def is_masked(position, intervals):
    """Retourne True si la position est dans un intervalle donné"""
    return any(start <= position <= end for (start, end) in intervals)

def mask_differences(differences_file, bed_ref, bed_query, output_file=sys.argv[4]):
    ref_intervals = load_bed_intervals(bed_ref)
    query_intervals = load_bed_intervals(bed_query)

    with open(differences_file) as fin, open(output_file, 'w') as fout:
        header = fin.readline()
        fout.write(header.strip() + "\n")

        for line in fin:
            fields = line.strip().split('\t')
            if len(fields) != 4:
                continue  # ignorer les lignes mal formées

            pos = int(fields[0])
            typ = fields[1]
            base_ref = fields[2]
            base_query = fields[3]

            if is_masked(pos, ref_intervals):
                base_ref = "N"
            if is_masked(pos, query_intervals):
                base_query = "N"

            fout.write(f"{pos}\t{typ}\t{base_ref}\t{base_query}\n")

    print(f"✅ Fichier masqué généré : {output_file}")

# === Exécution depuis le terminal ===
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage : python mask_differences.py differences.txt H37Rv.bed L6.bed difference_mask.txt")
        sys.exit(1)
    mask_differences(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
