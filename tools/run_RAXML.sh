#!/bin/bash
RAXML_BIN=~/phylogenetics/RaXML-8.2.7/raxmlHPC-PTHREADS-SSE3
if [ $# -lt 1 ]
then
	echo "Usage run_RAXML.sh bin_dir"
else
	OLD_DIR=`pwd`
	BIN_DIR=$1
	cd $BIN_DIR
	for x in `ls bin.0.txt`
	do
		BIN_NUMBER=$(echo $x | cut -f2 -d. )
		BIN_IDX="bin."$BIN_NUMBER
		LOGDIR=$BIN_DIR"/RAXML_log_"$BIN_IDX
		mkdir -p $LOGDIR
		cd $LOGDIR
		cp $BIN_DIR"/supergene_"$BIN_IDX".phylip" .
		cp $BIN_DIR"/partition_"$BIN_IDX".txt" .
		$RAXML_BIN -m GTRGAMMA -s "supergene_"$BIN_IDX".phylip" -n "supergene_"$BIN_IDX".tree" -N 20 -M -q "partition_"$BIN_IDX".txt" -p 12345 -T 5 > stdouterr.txt
		cd ..
		cp $LOGDIR"/RAxML_bestTree.supergene_"$BIN_IDX".tree" .
		echo $BIN_IDX "Done"
	done
	cd $OLD_DIR
fi