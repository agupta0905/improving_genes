#!/bin/bash
RAXML_BIN=~/phylogenetics/RaXML-8.2.7/raxmlHPC-PTHREADS-SSE3
if [ $# -lt 1 ]
then
	echo "Usage run_RAXML.sh bin_dir"
else
	BIN_DIR=$1
	for x in `ls $BIN_DIR/bin.0.txt | xargs -n 1 basename`
	do
		BIN_NUMBER=$(echo $x | cut -f2 -d. )
		BIN_IDX="bin."$BIN_NUMBER
		LOGDIR=$BIN_DIR"/RAXML_log_"$BIN_IDX
		mkdir -p $LOGDIR
		cp $BIN_DIR"/supergene_"$BIN_IDX".phylip" "copy_supergene_"$BIN_IDX".phylip"
		cp $BIN_DIR"/partition_"$BIN_IDX".txt" "copy_partition_"$BIN_IDX".txt"
		OUTPUT_PREFIX="supergene_"$BIN_IDX".tree"
		$RAXML_BIN -m GTRGAMMA -s "copy_supergene_"$BIN_IDX".phylip" -n $OUTPUT_PREFIX -N 20 -M -q "copy_partition_"$BIN_IDX".txt" -p 12345 -T 5 > "RAxML_stdouterr_"$OUTPUT_PREFIX".txt"
		rm "copy_supergene_"$BIN_IDX".phylip"
		rm "copy_partition_"$BIN_IDX".txt"
		mv RAxML*$OUTOUT_PREFIX* $LOGDIR/
		cp $LOGDIR"/RAxML_bestTree."$OUTPUT_PREFIX $BIN_DIR/
		echo $BIN_IDX "Done"
	done
fi
