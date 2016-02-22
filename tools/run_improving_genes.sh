#!/bin/bash
SRC_FILE=~/improving_genes/src/improving_genes.py
WQMC_BIN=~/improving_genes/tools/max-cut-tree
P_DP_BIN=/u/sciteam/gupta1/phylogenetics/wASTRAL/build/wASTRAL
ASTRAL_JAR=/u/sciteam/gupta1/phylogenetics/Astral/astral.4.7.12.jar
ASTRID_BIN=/u/sciteam/gupta1/phylogenetics/ASTRID/ASTRID
STATISTICAL_BINNING_SCRIPT=~/improving_genes/tools/run_statistical_binning.sh
GENE_OFFSET=100000000
RES_SRC_FILE=~/improving_genes/tools/get_results.py
if [ $# -lt 12 ]
then
	echo "Usage run_improving_genes.sh gene_dir numgenes treefilename weights=[on,off] confidence=[off,value] binning=[off,threshold] true_gene_dir truetreefilename bsrepsfilename=[fname,off] identifier=[value] supertree=[wqmc,pv] truespeciestreepath"
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
	IDENTIFIER=$(echo ${10} | cut -f2 -d=)
	SUPERTREE_METHOD=$(echo ${11} | cut -f2 -d=)
	TRUESPECIESTREEPATH=${12}
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
   			rm -rf $GENE_DIR"/"$TMP_DIRNAME
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
	OUTPUT_PREFIX="quartet_"$IDENTIFIER
	QUARTET_FILENAME="${TMP_DIRNAME/tmp/$OUTPUT_PREFIX}".txt
	ARGUMENTS="${ARGUMENTS/^/$QUARTET_FILENAME}"
	echo "ARGUMENTS: "$ARGUMENTS
	#Create tmp directory 
	mkdir -p $TMP_DIRPATH
	#Launch Python 
	python $SRC_FILE $ARGUMENTS
	echo "[STATUS]: GENE TREES IMPROVED"
	rm -rf $TMP_DIRPATH
############################################################################################################################################
	#Get gene offset
	re='^[0-9]+$'
	for entry in "$GENE_DIR"/*
	do
		gene=$(echo $entry | rev | cut -f1 -d/ | rev)
  		if ! [[ $gene =~ $re ]] ; then
 			:
 		else
 			GENE_OFFSET=$( (( $GENE_OFFSET <= $gene )) && echo "$GENE_OFFSET" || echo "$gene" )
		fi
	done
	GENE_OFFSET=`expr $GENE_OFFSET - 1`
	GENE_BEGIN=`expr $GENE_OFFSET + 1`
	GENE_END=`expr $GENE_OFFSET + $NUMGENES`
############################################################################################################################################	
	ORIG_GENES_FILE=$GENE_DIR"/G_"$NUMGENES"_genes.trees" 
	SETX_FILE=$GENE_DIR"/setX_G"$NUMGENES".tree"
	if ! [ -f $SETX_FILE ];
	then
		rm -f $ORIG_GENES_FILE
		for i in $(seq $GENE_BEGIN $GENE_END)
		do
			cat $GENE_DIR"/"$i"/"$TREEFILENAME >> $ORIG_GENES_FILE
		done
		$ASTRID_BIN -i $ORIG_GENES_FILE -o $GENE_DIR"/astrid_G"$NUMGENES".tree"
		java -jar $ASTRAL_JAR -i $ORIG_GENES_FILE -o $GENE_DIR"/astral_G"$NUMGENES".tree"
		cat $ORIG_GENES_FILE $GENE_DIR"/astrid_G"$NUMGENES".tree" $GENE_DIR"/astral_G"$NUMGENES".tree" > $SETX_FILE
	fi
	if [ $SUPERTREE_METHOD == "wqmc" ]
	then
		WQMC_PREFIX="wqmc_"$IDENTIFIER
		WQMC_FILENAME="${TMP_DIRNAME/tmp/$WQMC_PREFIX}".tree
		for i in $(seq $GENE_BEGIN $GENE_END)
		do
			$WQMC_BIN "qrtt="$GENE_DIR"/"$i"/"$QUARTET_FILENAME weights=on "otre="$GENE_DIR"/"$i"/"$WQMC_FILENAME
			FILE=$GENE_DIR"/"$i"/"$WQMC_FILENAME
			if ! [ -f $FILE ];
			then
				echo "WQMC failed for $i"
   				cp $GENE_DIR"/"$i"/"$TREEFILENAME $GENE_DIR"/"$i"/"$WQMC_FILENAME
			fi
			echo "WQMC run for gene "$i
		done
		echo "[STATUS]: WQMC RUN COMPLETED"
	else
		PV_PREFIX="pv_"$IDENTIFIER
		PV_FILENAME="${TMP_DIRNAME/tmp/$PV_PREFIX}".tree
		for i in $(seq $GENE_BEGIN $GENE_END)
		do
			$P_DP_BIN -c DP -g $SETX_FILE -q $GENE_DIR"/"$i"/"$QUARTET_FILENAME -a $ASTRAL_JAR -o $GENE_DIR"/"$i"/"$PV_FILENAME -v info --maximize
			echo $i" done for PV"
		done
	fi
############################################################################################################################################	
	if [ $SUPERTREE_METHOD == "wqmc" ]
	then
		NEWGENE_TREES_PREFIX="wqmc_"$IDENTIFIER
		NEWGENE_TREES_FILENAME="${TMP_DIRNAME/tmp/$NEWGENE_TREES_PREFIX}".trees
		NEWGENE_ASTRID_PREFIX="astrid_"$IDENTIFIER
		NEWGENE_ASTRID_FILENAME="${TMP_DIRNAME/tmp/$NEWGENE_ASTRID_PREFIX}".trees
		rm -f $GENE_DIR"/"$NEWGENE_TREES_FILENAME
		for i in $(seq $GENE_BEGIN $GENE_END)
		do
			cat $GENE_DIR"/"$i"/"$WQMC_FILENAME >> $GENE_DIR"/"$NEWGENE_TREES_FILENAME
		done
	else
		NEWGENE_TREES_PREFIX="pv_"$IDENTIFIER
		NEWGENE_TREES_FILENAME="${TMP_DIRNAME/tmp/$NEWGENE_TREES_PREFIX}".trees
		rm -f $GENE_DIR"/"$NEWGENE_TREES_FILENAME
		for i in $(seq $GENE_BEGIN $GENE_END)
		do
			cat $GENE_DIR"/"$i"/"$PV_FILENAME >> $GENE_DIR"/"$NEWGENE_TREES_FILENAME
		done
	fi
	NEWGENE_ASTRID_PREFIX="astrid_"$IDENTIFIER
	NEWGENE_ASTRID_FILENAME="${TMP_DIRNAME/tmp/$NEWGENE_ASTRID_PREFIX}".tree
	$ASTRID_BIN -i $GENE_DIR"/"$NEWGENE_TREES_FILENAME -o $GENE_DIR"/"$NEWGENE_ASTRID_FILENAME
	ASTRALSETX_PREFIX="extrasetX_"$IDENTIFIER
	ASTRALSETX_FILENAME="${TMP_DIRNAME/tmp/$ASTRALSETX_PREFIX}".trees
	cat $GENE_DIR"/"$NEWGENE_TREES_FILENAME $GENE_DIR"/"$NEWGENE_ASTRID_FILENAME $SETX_FILE > $GENE_DIR"/"$ASTRALSETX_FILENAME
	SPECIES_PREFIX="astral_"$IDENTIFIER
	SPECIES_FILENAME="${TMP_DIRNAME/tmp/$SPECIES_PREFIX}".tree
	java -jar $ASTRAL_JAR -i $GENE_DIR"/"$NEWGENE_TREES_FILENAME -o $GENE_DIR"/"$SPECIES_FILENAME -e $GENE_DIR"/"$ASTRALSETX_FILENAME
	echo "Computation Done"
############################################################################################################################################	
	if [ $SUPERTREE_METHOD == "wqmc" ]
	then
		RESULT_PREFIX="wqmcresult_"$IDENTIFIER
	else
		RESULT_PREFIX="pvresult_"$IDENTIFIER
	fi
	
	RESULT_FILENAME="${TMP_DIRNAME/tmp/$RESULT_PREFIX}".txt
	RESULT_FILE=$GENE_DIR"/"$RESULT_FILENAME
	rm -f $RESULT_FILE
	python $RES_SRC_FILE $TRUE_GENEDIR $TRUETREEFILENAME $GENE_DIR $TREEFILENAME $NUMGENES resulttmp.txt 
	echo "Original genes vs True genes" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	python $RES_SRC_FILE $TRUESPECIESTREEPATH $GENE_DIR"/astrid_G"$NUMGENES".tree" $GENE_DIR"/resulttmp.txt"
	echo "Original genes ASTRID" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	python $RES_SRC_FILE $TRUESPECIESTREEPATH $GENE_DIR"/astral_G"$NUMGENES".tree" $GENE_DIR"/resulttmp.txt" 
	echo "Original genes ASTRAL" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	if [ $SUPERTREE_METHOD == "wqmc" ]
	then
		python $RES_SRC_FILE $TRUE_GENEDIR $TRUETREEFILENAME $GENE_DIR $WQMC_FILENAME $NUMGENES resulttmp.txt
		echo "Improved genes vs True genes" >> $RESULT_FILE
		cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	else
		python $RES_SRC_FILE $TRUE_GENEDIR $TRUETREEFILENAME $GENE_DIR $PV_FILENAME $NUMGENES resulttmp.txt 
		echo "Improved genes vs True genes" >> $RESULT_FILE
		cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	fi
	python $RES_SRC_FILE $TRUESPECIESTREEPATH $GENE_DIR"/"$NEWGENE_ASTRID_FILENAME $GENE_DIR"/resulttmp.txt" 
	echo "Improved genes ASTRID" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	python $RES_SRC_FILE $TRUESPECIESTREEPATH $GENE_DIR"/"$SPECIES_FILENAME $GENE_DIR"/resulttmp.txt" 
	echo "Improved genes ASTRAL" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
fi
