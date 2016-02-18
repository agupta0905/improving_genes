#!/bin/bash
if [ $# -lt 4 ]
then
	echo "Usage run_statistical_binning.sh gene_dir numgenes support_threshold tree_filename"
else
	GENE_DIR=$1
	NUMGENES=$2
	SUPPORT_THRESHOLD=$3
	TREEFILENAME=$4
	PAIRWISEDIR=$GENE_DIR"/BINS_"$NUMGENES"_"$SUPPORT_THRESHOLD
	mkdir -p $PAIRWISEDIR
	mkdir -p $GENE_DIR"/tmp_binning"
	cd $GENE_DIR"/tmp_binning"
	$BINNING_HOME/makecommands.compatibility.sh $GENE_DIR $SUPPORT_THRESHOLD $PAIRWISEDIR $TREEFILENAME $NUMGENES
	COMMAND_FILE=commands.compat.$NUMGENES.$SUPPORT_THRESHOLD
	chmod +x $COMMAND_FILE
	./$COMMAND_FILE
	cd $PAIRWISEDIR
	ls | grep "[0-9]*\.$SUPPORT_THRESHOLD" | cut -d. -f 1 > genes
	python $BINNING_HOME/cluster_genetrees.py genes $SUPPORT_THRESHOLD
fi