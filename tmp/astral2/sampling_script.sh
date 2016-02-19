#!/bin/bash
DATASET_DIR=/u/sciteam/gupta1/scratch/astra2_dataset
for m in model.200.10000000.0.0000001 model.200.2000000.0.0000001 model.200.500000.0.0000001
do
	for r in 01 02 03 04 05 06 07 08 09 10
	do
		MDIR=$DATASET_DIR"/"$m"/"$r
		~/phylogenetics/FastTree -nt -gtr -nopr -gamma -n 50 < $MDIR"/50g_50t_50s.phylip" > $MDIR"/50g_50t_50s_fasttree.tree"
		#python ~/improving_genes/tmp/astral2/sample_data.py $MDIR"/all-genes.phylip" $MDIR"/50g_50t_50s.phylip" 50 50 50
		echo $MDIR" Done"
	done
	
done