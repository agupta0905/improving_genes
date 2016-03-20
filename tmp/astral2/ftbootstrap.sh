#!/bin/bash
DATASET_DIR=/u/sciteam/gupta1/scratch/astral2_dataset
for m in model.200.10000000.0.000001 model.200.10000000.0.0000001 model.200.2000000.0.000001 model.200.2000000.0.0000001
do
	for r in 01 02 03 04 05 06 07 08 09 10
	do
		MDIR=$DATASET_DIR"/"$m"/"$r
		if [ -d "$MDIR" ]; then
			for g in $(seq 1 200)
			do
				for s in 200 100 50
				do
					python ~/improving_genes/tools/updateftbootstraps.py $MDIR"/"$g"/50t_"$s"s.tree"
					echo $MDIR"/"$g"/50t_"$s"s.tree" "DONE"	
				done
			done		
		fi
	done
done