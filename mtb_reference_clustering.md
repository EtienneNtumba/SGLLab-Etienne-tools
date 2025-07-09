# 🧬 Impact of Reference Genome Choice on Clustering Analyses of *Mycobacterium tuberculosis*

> This repository contains a fully automated and reproducible pipeline designed to assess how the selection of different reference genomes influences clustering results derived from whole genome sequencing (WGS) data of *Mycobacterium tuberculosis* (Mtb) isolates.

---

## 📖 Background

Whole genome sequencing (WGS) has significantly enhanced the resolution of molecular epidemiology for infectious diseases, particularly for *Mycobacterium tuberculosis* (Mtb). It enables high-resolution clustering of isolates, which is essential for understanding transmission dynamics. However, the accuracy of these analyses heavily depends on the **choice of reference genome**—a critical yet often underestimated factor.

This project provides a comparative framework to investigate how reference genome selection (e.g., canonical vs lineage-specific genomes) affects genetic diversity detection, allele masking, and ultimately, clustering outcomes.

---

## 🎯 Objective

- Quantify discrepancies in sequence comparison outcomes caused by different reference genomes.
- Categorize observed variants into **eight distinct allele scenarios** based on allele presence/absence, masking, and variability.
- Provide evidence-based guidance for selecting an appropriate reference genome in Mtb genomic epidemiology.

---

## 📁 Repository Structure

```
.
├── sample.txt                          # List of genome pairs (reference vs lineage)
├── *.fasta                             # Genome FASTA files
├── *.bed                               # BED files for masking regions
├── aligned_genomes_diff_same_region.py
├── mask_differences.py
├── count_scenarios_from_table.py
├── merge_scenario_count.py
├── run_pipeline.sh                    # Full execution script
├── combined_scenarios_counts.csv      # Final merged table
├── Scenarios_L1_L8.png                # Visual representation of the 8 scenarios
└── README.md                          # This file
```

---

## ⚙️ Dependencies

- [`minimap2`](https://github.com/lh3/minimap2) – for genome alignment
- Python ≥ 3.7
  - `pandas`, `biopython`, `numpy`
- `bedtools` (optional, for BED file operations)

**Install using Conda:**
```bash
conda create -n refgenome_clustering python=3.10 pandas biopython
conda activate refgenome_clustering
```

---

## 🧪 Execution Pipeline

### 🔁 Automated Bash Script

The `run_pipeline.sh` script orchestrates all steps from alignment to scenario table merging:

```bash
#!/bin/bash

tail -n +2 sample.txt | while IFS=$'\t' read -r ref lx; do
    echo "Processing Reference: $ref, Compared Genome: $lx"

    if [[ ! -f "${ref}.fasta" ]]; then echo "❌ Missing: ${ref}.fasta"; continue; fi
    if [[ ! -f "${lx}.fasta" ]]; then echo "❌ Missing: ${lx}.fasta"; continue; fi

    minimap2 -x asm5 -c "${ref}.fasta" "${lx}.fasta" > "alignment_${ref}_${lx}.paf"

    python aligned_genomes_diff_same_region.py "${ref}.fasta" "${lx}.fasta" \
           "alignment_${ref}_${lx}.paf" "table_${ref}_${lx}.tsv"

    python mask_differences.py "table_${ref}_${lx}.tsv" "${ref}.bed" "${lx}.bed" \
           "table_${ref}_${lx}_mask.tsv"

    python count_scenarios_from_table.py "table_${ref}_${lx}_mask.tsv" \
           "scenarios_table_${ref}_${lx}_mask.tsv"
done

python merge_scenario_count.py
```

Ensure that all `.fasta` and `.bed` files listed in `sample.txt` are present in your directory.

---

## 🔬 Allele Scenarios

Each site is classified into one of eight scenarios based on allele presence in the reference and query genome, masking status, and variability:

| # | Ref | Lx | Mask (Ref) | Mask (Lx) | Discrepancy | Variability |
|---|-----|----|------------|-----------|--------------|-------------|
| 1 | y   | y  | y          | y         | No           | -           |
| 2 | y   | n  | n          | n/a       | No           | -           |
| 3 | y   | y  | n          | n         | No           | -           |
| 4 | n   | y  | n/a        | y         | No           | -           |
| 5 | n   | y  | n/a        | n         | Yes          | Decrease    |
| 6 | y   | y  | y          | n         | Yes          | Decrease    |
| 7 | y   | y  | n          | y         | Yes          | Increase    |
| 8 | y   | n  | y          | n/a       | No           | -           |

![Scenarios](Scenarios_L1_L8.png)

---

## 📊 Summary Output: `combined_scenarios_counts.csv`

| Scenario | L1       | L2       | L3       | L5       | L6       |
|----------|----------|----------|----------|----------|----------|
| 1️⃣ N/N   | 127770   | 114078   | 89334    | 120084   | 89570    |
| 2️⃣ base/gap | 26708 | 24127    | 8053     | 9451     | 50424    |
| 3️⃣ base/base| 3656425| 3638109 | 3614673  | 3645842  | 3594196  |
| 4️⃣ gap/N | 437      | 2035     | 399      | 1233     | 581      |
| 5️⃣ gap/base | 554   | 17350    | 12398    | 2318     | 13220    |
| 6️⃣ N/y   | 3546     | 6642     | 4032     | 1126     | 5266     |
| 7️⃣ y/N   | 5006     | 2702     | 1575     | 5727     | 2125     |
| 8️⃣ y/N   | 29312    | 54414    | 36538    | 21593    | 59777    |

---

## 🧠 Interpretation

- **Scenario 3 (base/base)** dominates, indicating high genomic conservation.
- **Scenarios 5 and 6** highlight cases where lineage-specific references reveal variants that would be missed using a canonical reference.
- **Scenario 7** reflects masked variability in the query genome, possibly indicating reference-driven bias.
- These patterns underscore the non-trivial impact of reference selection on downstream transmission and clustering analyses.

---

## 📚 Key References

- Coll et al. (2014). *A robust SNP barcode for typing Mycobacterium tuberculosis complex strains*. [DOI: 10.1038/ncomms5812](https://doi.org/10.1038/ncomms5812)
- Bradley et al. (2019). *Ultrafast search of all deposited bacterial and viral genomic data*. [DOI: 10.1038/s41592-019-0501-3](https://doi.org/10.1038/s41592-019-0501-3)
- Meehan et al. (2019). *Whole genome sequencing of Mycobacterium tuberculosis: current standards and open issues*. [DOI: 10.1016/j.clinmicnews.2019.03.004](https://doi.org/10.1016/j.clinmicnews.2019.03.004)
- Freschi et al. (2021). *Population structure, biogeography and transmissibility of Mycobacterium tuberculosis*. [DOI: 10.1038/s41586-020-2895-3](https://doi.org/10.1038/s41586-020-2895-3)

---

## 👨‍💻 Author

**Etienne Kabongo Ntumba**  
Bioinformatician – McGill University  
📧 etiennekabongo[at]mail.com  
🗓 Version: `v1.0`

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

