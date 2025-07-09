
#!/bin/bash

# Lire le fichier ligne par ligne, en ignorant l'entête
tail -n +2 sample.txt | while IFS=$'\t' read -r ref lx; do
    echo "Traitement de Référence: $ref, Comparé: $lx"

    # Vérification de l'existence des fichiers
    if [[ ! -f "${ref}.fasta" ]]; then
        echo "❌ Fichier ${ref}.fasta introuvable"; continue
    fi

    if [[ ! -f "${lx}.fasta" ]]; then
        echo "❌ Fichier ${lx}.fasta introuvable"; continue
    fi

    # Alignement
    minimap2 -x asm5 -c "${ref}.fasta" "${lx}.fasta" > "alignment_${ref}_${lx}.paf"
    echo "✅ Alignement produit : alignment_${ref}_${lx}.paf"
  
   # Tranformation de paf en fasta et table
    python aligned_genomes_diff_same_region.py "${ref}.fasta" "${lx}.fasta" "alignment_${ref}_${lx}.paf" "table_${ref}_${lx}.tsv"
    echo "✅ Transformation paf to fasta and table : alignment_${ref}_${lx}.paf"
  
  # Mask la table  
    python mask_differences.py "table_${ref}_${lx}.tsv" "${ref}.bed" "${lx}.bed" "table_${ref}_${lx}_mask.tsv"  
    echo "✅ Mask sur la table : table_${ref}_${lx}_mask.tsv"
 ## Comptage de scenarios
    python count_scenarios_from_table.py "table_${ref}_${lx}_mask.tsv" "scenarios_table_${ref}_${lx}_mask.tsv"
   echo "Enfin, on a notre table avec les scenarios "
done
python merge_scenario_count.py
