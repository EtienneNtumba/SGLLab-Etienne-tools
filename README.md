# 🧬 Reference Genome Impact on *Mycobacterium tuberculosis* Clustering

> A reproducible and containerized pipeline to evaluate how the choice of reference genome affects transmission clustering and genetic diversity detection in *Mycobacterium tuberculosis* (Mtb) using whole-genome sequencing (WGS) data.

---

## 📘 Overview

Whole-genome sequencing (WGS) enables high-resolution clustering of *Mycobacterium tuberculosis* (Mtb) isolates, a critical step for understanding transmission dynamics. However, analyses can be biased by the **choice of reference genome**. This pipeline compares canonical and lineage-specific references to:

- Quantify differences in alignment and masked regions
- Classify variation into 8 distinct allele scenarios
- Assess the impact on downstream clustering interpretations

---

## 🎯 Goals

- Perform pairwise genome alignment (reference vs lineage-specific genomes)
- Detect and classify aligned differences
- Apply genomic region masking
- Count allele scenarios per pair
- Merge scenario summaries into a comprehensive matrix

---

## 🔁 Pipeline Summary (Nextflow)

This project is implemented using **Nextflow** and supports containerized execution via **Docker** or **Conda**.

### Steps:
1. Align genomes using `minimap2`
2. Identify differences with `aligned_genomes_diff_same_region.py`
3. Mask based on reference and lineage-specific BED files
4. Count allele scenarios per pair
5. Merge all results into a final CSV summary

---

## 🚀 Quickstart

### 🔹 Requirements
- [Nextflow](https://www.nextflow.io/)
- Docker or Conda (for reproducible environments)

### 🔹 Run the pipeline
```bash
nextflow run main.nf --sample_file sample.txt
```

---

## 🧩 File Structure

```
.
├── main.nf                         # Nextflow pipeline
├── nextflow.config                 # Pipeline configuration
├── sample.txt                      # Tab-separated genome pairs
├── Dockerfile                      # Docker container definition
├── environment.yml                 # Conda environment for bioinformatics tools
├── *.py                            # Custom Python scripts
├── *.fasta / *.bed                 # Input genome and mask files
├── combined_scenarios_counts.csv  # Final merged output
├── scenarios_table_*.tsv          # Scenario counts per comparison
└── Scenarios_L1_L8.png            # Scenario schematic
```

---

## 🔬 Allele Scenarios

Each site is categorized into one of 8 biologically relevant scenarios, based on presence, masking status, and variability:

| # | Ref | Lx | Masked (Ref) | Masked (Lx) | Discrepancy | Variability |
|---|-----|----|---------------|--------------|--------------|-------------|
| 1 | y   | y  | y             | y            | No           | -           |
| 2 | y   | n  | n             | n/a          | No           | -           |
| 3 | y   | y  | n             | n            | No           | -           |
| 4 | n   | y  | n/a           | y            | No           | -           |
| 5 | n   | y  | n/a           | n            | Yes          | Decrease    |
| 6 | y   | y  | y             | n            | Yes          | Decrease    |
| 7 | y   | y  | n             | y            | Yes          | Increase    |
| 8 | y   | n  | y             | n/a          | No           | -           |

![Scenarios](Scenarios_L1_L8.png)

---

## 📊 Example Output

`combined_scenarios_counts.csv` summarizes counts across all genome pairs:

| Scenario      | L1      | L2      | L3      | L5      | L6      |
|---------------|---------|---------|---------|---------|---------|
| 1️⃣ N/N        | 127770  | 114078  | 89334   | 120084  | 89570   |
| 2️⃣ base/gap   | 26708   | 24127   | 8053    | 9451    | 50424   |
| 3️⃣ base/base  | 3656425 | 3638109 | 3614673 | 3645842 | 3594196 |
| 4️⃣ gap/N      | 437     | 2035    | 399     | 1233    | 581     |
| 5️⃣ gap/base   | 554     | 17350   | 12398   | 2318    | 13220   |
| 6️⃣ N/y        | 3546    | 6642    | 4032    | 1126    | 5266    |
| 7️⃣ y/N        | 5006    | 2702    | 1575    | 5727    | 2125    |
| 8️⃣ y/N        | 29312   | 54414   | 36538   | 21593   | 59777   |

---

## 📦 Environments

### Docker
```Dockerfile
FROM continuumio/miniconda3
COPY environment.yml .
RUN conda env create -f environment.yml && conda clean -a
ENV PATH /opt/conda/envs/mtb_refgen_env/bin:$PATH
```

### Conda
```yaml
name: mtb_refgen_env
channels:
  - conda-forge
  - bioconda
dependencies:
  - python=3.10
  - pandas
  - biopython
  - minimap2
  - bedtools
```

---

## 📚 References

- Coll et al. (2014). *A robust SNP barcode for typing Mycobacterium tuberculosis complex strains*. [DOI](https://doi.org/10.1038/ncomms5812)
- Bradley et al. (2019). *Ultrafast search of all deposited bacterial and viral genomic data*. [DOI](https://doi.org/10.1038/s41592-019-0501-3)
- Meehan et al. (2019). *Whole genome sequencing of Mycobacterium tuberculosis: current standards and open issues*. [DOI](https://doi.org/10.1016/j.clinmicnews.2019.03.004)
- Freschi et al. (2021). *Population structure, biogeography and transmissibility of Mycobacterium tuberculosis*. [DOI](https://doi.org/10.1038/s41586-020-2895-3)

---
## Authors

**Etienne Ntumba Kabongo**  
📧 Email: [etienne.ntumba.kabongo@umontreal.ca](mailto:etienne.ntumba.kabongo@umontreal.ca)  
🔗 GitHub: [EtienneNtumba](https://github.com/EtienneNtumba)
** Prof. SIMON GRANDJEAN-LAPIERRE **
Prof. SIMON GRANDJEAN-LAPIERRE - Associate professor in the Microbiology, Infectious Diseases and Immunology Department of Université de Montréal
** Prof.Martin SMITH **
Prof.Martin SMITH - computational biologist specialising in transcriptomics, UNSW Sydney



## 📜 License

MIT License – see `LICENSE` file for details.
