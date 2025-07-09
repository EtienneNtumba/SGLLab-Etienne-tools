from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys

def parse_fasta(fasta_path):
    """Lit un fichier FASTA avec une seule séquence et retourne {id: séquence}"""
    return {record.id: str(record.seq) for record in SeqIO.parse(fasta_path, "fasta")}

def parse_paf(paf_file):
    """Extrait les blocs alignés (query_start, query_end, ref_start, ref_end, strand)"""
    blocks = []
    with open(paf_file) as f:
        for line in f:
            fields = line.strip().split('\t')
            qname, qstart, qend = fields[0], int(fields[7]), int(fields[8])
            tname, tstart, tend = fields[5], int(fields[2]), int(fields[3])
            strand = fields[4]
            blocks.append((qstart, qend, tstart, tend, strand))
    return sorted(blocks, key=lambda x: x[0])  # Trier par position query

def generate_alignment(query_seq, target_seq, blocks):
    """Construit un alignement global à partir des blocs, insère '-' si nécessaire"""
    aligned_q = []
    aligned_t = []
    q_pos = 0
    t_pos = 0

    for qstart, qend, tstart, tend, strand in blocks:
        # Gaps entre blocs
        if qstart > q_pos or tstart > t_pos:
            gap_q = query_seq[q_pos:qstart]
            gap_t = target_seq[t_pos:tstart]
            max_len = max(len(gap_q), len(gap_t))
            aligned_q.append(gap_q.ljust(max_len, '-'))
            aligned_t.append(gap_t.ljust(max_len, '-'))

        # Bloc aligné
        aligned_q.append(query_seq[qstart:qend])
        aligned_t.append(target_seq[tstart:tend])
        q_pos = qend
        t_pos = tend

    # Séquences non alignées en fin de chaîne
    tail_q = query_seq[q_pos:]
    tail_t = target_seq[t_pos:]
    max_len = max(len(tail_q), len(tail_t))
    aligned_q.append(tail_q.ljust(max_len, '-'))
    aligned_t.append(tail_t.ljust(max_len, '-'))

    # Sécurité : égalise les longueurs finales
    aln_q = ''.join(aligned_q)
    aln_t = ''.join(aligned_t)

    if len(aln_q) != len(aln_t):
        print(f"⚠️ Correction : longueurs inégales ({len(aln_q)} vs {len(aln_t)})")
        max_final = max(len(aln_q), len(aln_t))
        aln_q = aln_q.ljust(max_final, '-')
        aln_t = aln_t.ljust(max_final, '-')

    return aln_q, aln_t

def write_fasta(id1, seq1, id2, seq2, output="aligned_genomes.fasta"):
    """Écrit les deux séquences alignées dans un fichier FASTA"""
    records = [
        SeqRecord(Seq(seq1), id=id1, description="aligned"),
        SeqRecord(Seq(seq2), id=id2, description="aligned"),
    ]
    SeqIO.write(records, output, "fasta")
    print(f"✅ Alignement écrit dans : {output}")

def detect_differences(seq1, seq2, id1, id2, output=sys.argv[4]):
    """Compare deux séquences alignées et écrit toutes les positions : matches, SNPs, indels, non-alignés"""
    with open(output, "w") as out:
        out.write("Position\tType\t{}\t{}\n".format(id1, id2))
        ref_pos = 1  # position sur la séquence de référence (1-based)

        max_len = max(len(seq1), len(seq2))
        for i in range(max_len):
            base1 = seq1[i] if i < len(seq1) else "-"
            base2 = seq2[i] if i < len(seq2) else "-"

            if base1 == base2:
                if base1 != "-":
                    out.write(f"{ref_pos}\tMatch\t{base1}\t{base2}\n")
                    ref_pos += 1
                else:
                    out.write(f"{ref_pos}\tUnaligned\t{base1}\t{base2}\n")
            else:
                if base1 == "-":
                    out.write(f"{ref_pos}\tInsertion\t{base1}\t{base2}\n")
                elif base2 == "-":
                    out.write(f"{ref_pos}\tDeletion\t{base1}\t{base2}\n")
                    ref_pos += 1
                else:
                    out.write(f"{ref_pos}\tSNP\t{base1}\t{base2}\n")
                    ref_pos += 1

    print(f"✅ Fichier de différences complet écrit dans : {output}")

def main(ref_fasta, query_fasta, paf_file, diff_output):
    ref_dict = parse_fasta(ref_fasta)
    query_dict = parse_fasta(query_fasta)

    ref_id = list(ref_dict.keys())[0]
    query_id = list(query_dict.keys())[0]
    ref_seq = ref_dict[ref_id]
    query_seq = query_dict[query_id]

    blocks = parse_paf(paf_file)
    aligned_query, aligned_ref = generate_alignment(query_seq, ref_seq, blocks)

    write_fasta(query_id, aligned_query, ref_id, aligned_ref)
    detect_differences(aligned_ref, aligned_query, ref_id, query_id, diff_output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python aligned_genomes_diff.py ref.fasta query.fasta alignment.paf difference.txt")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4])
