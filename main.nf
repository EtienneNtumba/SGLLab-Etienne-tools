// main.nf

params.sample_file = "sample.txt"

Channel.fromPath(params.sample_file)
    .splitCsv(header: true, sep: '\t')
    .set { pairs }

process align {
    tag "${ref}_${lx}"

    input:
    val ref from pairs.map { it.ref }
    val lx  from pairs.map { it.lx }

    output:
    path "alignment_${ref}_${lx}.paf" into pafs

    script:
    """
    minimap2 -x asm5 -c ${ref}.fasta ${lx}.fasta > alignment_${ref}_${lx}.paf
    """
}

process diff_table {
    tag "${ref}_${lx}"

    input:
    val ref from pairs.map { it.ref }
    val lx  from pairs.map { it.lx }
    path "alignment_${ref}_${lx}.paf" from pafs

    output:
    path "table_${ref}_${lx}.tsv" into tables

    script:
    """
    python aligned_genomes_diff_same_region.py ${ref}.fasta ${lx}.fasta \
      alignment_${ref}_${lx}.paf table_${ref}_${lx}.tsv
    """
}

process mask_table {
    tag "${ref}_${lx}"

    input:
    val ref from pairs.map { it.ref }
    val lx  from pairs.map { it.lx }
    path "table_${ref}_${lx}.tsv" from tables

    output:
    path "table_${ref}_${lx}_mask.tsv" into masked_tables

    script:
    """
    python mask_differences.py table_${ref}_${lx}.tsv ${ref}.bed ${lx}.bed \
      table_${ref}_${lx}_mask.tsv
    """
}

process count_scenarios {
    tag "${ref}_${lx}"

    input:
    val ref from pairs.map { it.ref }
    val lx  from pairs.map { it.lx }
    path "table_${ref}_${lx}_mask.tsv" from masked_tables

    output:
    path "scenarios_table_${ref}_${lx}_mask.tsv" into scenario_tables

    script:
    """
    python count_scenarios_from_table.py table_${ref}_${lx}_mask.tsv \
      scenarios_table_${ref}_${lx}_mask.tsv
    """
}

process merge_scenarios {
    input:
    path scenario_tables.collect() flatten: true

    output:
    path "combined_scenarios_counts.csv"

    script:
    """
    python merge_scenario_count.py
    """
}"
