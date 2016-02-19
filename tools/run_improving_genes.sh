#!/bin/bash
SRC_FILE=~/improving_genes/src/improving_genes.py
WQMC_BIN=~/improving_genes/tools/max-cut-tree
P_DP_BIN=/u/sciteam/gupta1/phylogenetics/wASTRAL/build/wASTRAL
ASTRAL_JAR=/u/sciteam/gupta1/phylogenetics/Astral/astral.4.7.12.jar
ASTRID_BIN=/u/sciteam/gupta1/phylogenetics/ASTRID/ASTRID
STATISTICAL_BINNING_SCRIPT=~/improving_genes/tools/run_statistical_binning.sh
GENE_OFFSET=100000000
RES_SRC_FILE=~/improving_genes/tools/get_results.py
if [ $# -lt 9 ]
then
	echo "Usage run_improving_genes.sh gene_dir numgenes treefilename weights=[on,off] confidence=[off,value] binning=[off,threshold] true_gene_dir truetreefilename bsrepsfilename=[fname,off]"
else
	GENE_DIR=$1
	NUMGENES=$2
	TREEFILENAME=$3
	WEIGHTS=$(echo $4 | cut -f2 -d=)
	CONF=$(echo $5 | cut -f2 -d=)
	BINNING_T=$(echo $6 | cut -f2 -d=)
	TRUE_GENEDIR=$7
	TRUETREEFILENAME=$8
	BSREPSFILENAME=$(echo $9 | cut -f2 -d=)
	ARGUMENTS="$1 $2 $3 ^ @"
	TMP_DIRNAME="tmp_G"$NUMGENES
	if [ $BINNING_T == "off" ]
	then
		TMP_DIRNAME="$TMP_DIRNAME"_nobinning""
	else
		TMP_DIRNAME="$TMP_DIRNAME"_withbinning"$BINNING_T"
		BINNING_DIR=$GENE_DIR"/BINS_"$NUMGENES"_"$BINNING_T
		if ! [ -f $BINNING_DIR"/bin.0.txt" ];
		then
			echo "No previous bins detected"
			PP=$PYTHONPATH
			PP="${PP/4.0.3/3.12.0}"
			export PYTHONPATH=$PP
   			$STATISTICAL_BINNING_SCRIPT $GENE_DIR $NUMGENES $BINNING_T $TREEFILENAME $TMP_DIRNAME
   			PP="${PP/3.12.0/4.0.3}"
			export PYTHONPATH=$PP
		fi
		ARGUMENTS="$ARGUMENTS -b $BINNING_DIR"
	fi
	if [ $WEIGHTS == "off" ]
	then
		TMP_DIRNAME="$TMP_DIRNAME"_nobranches""
	else
		ARGUMENTS="$ARGUMENTS -e"
		TMP_DIRNAME="$TMP_DIRNAME"_withbranches""
	fi
	if [ $CONF == "off" ]
	then
		TMP_DIRNAME="$TMP_DIRNAME"_noupweight""
	else
		ARGUMENTS="$ARGUMENTS -c $CONF"
		TMP_DIRNAME="$TMP_DIRNAME"_withupweight"$CONF"
	fi
	
	TMP_DIRPATH=$GENE_DIR"/"$TMP_DIRNAME
	ARGUMENTS="${ARGUMENTS/@/$TMP_DIRPATH}"
	OUTPUT_PREFIX=quartet
	WQMC_PREFIX=wqmc
	RESULT_PREFIX=result
	QUARTET_FILENAME="${TMP_DIRNAME/tmp/$OUTPUT_PREFIX}".txt
	WQMC_FILENAME="${TMP_DIRNAME/tmp/$WQMC_PREFIX}".tree
	RESULT_FILENAME="${TMP_DIRNAME/tmp/$RESULT_PREFIX}".txt
	
	ARGUMENTS="${ARGUMENTS/^/$QUARTET_FILENAME}"
	echo "ARGUMENTS: "$ARGUMENTS
	#Create tmp directory 
	mkdir -p $TMP_DIRPATH
	#Launch Python 
	python $SRC_FILE $ARGUMENTS
	echo "[STATUS]: GENE TREES IMPROVED"
	rm -rf tmp_*
	###################################
fi
