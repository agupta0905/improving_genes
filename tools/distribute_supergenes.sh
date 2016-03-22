#!/bin/bash
if [ $# -lt 4 ]
then
	echo "Usage distribute_supergenes.sh bin_dir gene_dir supertree_prefix outputtreename"
else
	BIN_DIR=$1
	GENE_DIR=$2
	SUPERTREE_PREFIX=$3
	OUTPUTTREENAME=$4
	for x in `ls $BIN_DIR/bin.*.txt | xargs -n 1 basename`
	do
		BIN_NUMBER=$(echo $x | cut -f2 -d. )
		BIN_IDX="bin."$BIN_NUMBER
		for g in `cat $BIN_DIR"/"$BIN_IDX".txt"`
		do
			cp $BIN_DIR"/"$SUPERTREE_PREFIX"_"$BIN_IDX".tree" $GENE_DIR"/"$g"/"$OUTPUTTREENAME
		done
		echo $BIN_IDX "Done"
	done
fi
