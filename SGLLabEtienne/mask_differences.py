
import argparse

def load_bed_intervals(bed_file):
    intervals = []
    with open(bed_file) as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            start, end = int(parts[1]), int(parts[2])
            intervals.append((start + 1, end))
    return intervals

def is_masked(position, intervals):
    return any(start <= position <= end for (start, end) in intervals)

def mask_differences(differences_file, bed_ref, bed_query, output_file):
    ref_intervals = load_bed_intervals(bed_ref)
    query_intervals = load_bed_intervals(bed_query)

    with open(differences_file) as fin, open(output_file, 'w') as fout:
        header = fin.readline()
        fout.write(header.strip() + "\n")

        for line in fin:
            fields = line.strip().split('\t')
            if len(fields) != 4:
                continue

            pos = int(fields[0])
            typ = fields[1]
            base_ref = fields[2]
            base_query = fields[3]

            if is_masked(pos, ref_intervals):
                base_ref = "N"
            if is_masked(pos, query_intervals):
                base_query = "N"

            fout.write(f"{pos}\t{typ}\t{base_ref}\t{base_query}\n")

    print(f"✅ Masked differences written to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='SGLLab-Mask: Mask differences using BED annotations.')
    parser.add_argument('input_table', help='Input TSV file with differences')
    parser.add_argument('ref_bed', help='BED file for reference genome')
    parser.add_argument('lx_bed', help='BED file for query genome')
    parser.add_argument('output_file', help='Output masked TSV file')
    args = parser.parse_args()

    mask_differences(args.input_table, args.ref_bed, args.lx_bed, args.output_file)

if __name__ == '__main__':
    main()
