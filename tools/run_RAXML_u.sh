#!/bin/bash
RAXML_BIN=~/phylogenetics/RaXML-8.2.7/raxmlHPC-SSE3
if [ $# -lt 2 ]
then
	echo "Usage run_RAXML_u.sh bin_dir replicatenumber"
else
	BIN_DIR=$1
	REP=$2
	for x in `ls $BIN_DIR/bin.*.txt | xargs -n 1 basename`
	do
		BIN_NUMBER=$(echo $x | cut -f2 -d. )
		BIN_IDX="bin."$BIN_NUMBER
		OUTPUT_PREFIX="R"$REP"_supergene_"$BIN_IDX".tree"
		LOGDIR=$BIN_DIR"/RAXML_log_"$BIN_IDX
		rm -rf $LOGDIR
		mkdir $LOGDIR
		rm -f "R"$REP"_copy_supergene_"$BIN_IDX".phylip"
		rm -f RAxML*$OUTPUT_PREFIX*
		cp $BIN_DIR"/supergene_"$BIN_IDX".phylip" "R"$REP"_copy_supergene_"$BIN_IDX".phylip"
		$RAXML_BIN -m GTRGAMMA -s "R"$REP"_copy_supergene_"$BIN_IDX".phylip" -n $OUTPUT_PREFIX -N 20 -p 12345 > "RAxML_stdouterr_"$OUTPUT_PREFIX".txt"
		rm "R"$REP"_copy_supergene_"$BIN_IDX".phylip"
		mv RAxML*$OUTPUT_PREFIX* $LOGDIR/
		cp $LOGDIR"/RAxML_bestTree."$OUTPUT_PREFIX $BIN_DIR/
		echo $REP $BIN_IDX "Done"
	done
fi
