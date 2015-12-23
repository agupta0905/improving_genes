#!/bin/bash
DIR=~/scratch/11_taxon_dataset
for m in model.10.1800000.0.000000111 model.10.200000.0.000001000 model.10.5400000.0.000000037 model.10.600000.0.000000333
do
	for r in $(seq 1 10)
	do
		python ~/improving_genes/tools/relabeler_trees.py $DIR"/"$m"/"$r	true.tree $DIR"/taxa_dict.txt" 1000
		echo $m $r "Done"
	done
	
done 