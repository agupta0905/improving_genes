#!/bin/bash
DATASET_DIR=/u/sciteam/gupta1/scratch/astral2_dataset
for m in model.200.10000000.0.000001 model.200.10000000.0.0000001 model.200.2000000.0.000001 model.200.2000000.0.0000001
do
	for r in 01 02 03 04 05 06 07 08 09 10
	do
		for s in 200 100 50
		do
			MDIR=$DATASET_DIR"/"$m"/"$r
			~/phylogenetics/FastTree -nt -gtr -nopr -gamma -n 1000 -quiet < $MDIR"/1000g_50t_"$s"s.phylip" > $MDIR"/1000g_50t_"$s"s.trees"
			#python ~/improving_genes/tmp/astral2/sample_data.py $MDIR"/all-genes.phylip" $MDIR"/1000g_50t_"$s"s.phylip" 50 $s 1000
			echo $MDIR "Done" $s "Done"
		done
	done
done