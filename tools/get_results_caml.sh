#!/bin/bash
ASTRAL_JAR=/u/sciteam/gupta1/phylogenetics/Astral/astral.4.7.12.jar
ASTRID_BIN=/u/sciteam/gupta1/phylogenetics/ASTRID/ASTRID
GENE_OFFSET=100000000
RES_SRC_FILE=~/improving_genes/tools/get_results.py
if [ $# -lt 6 ]
then
	echo "Usage get_results_caml.sh gene_dir numgenes treefilename true_gene_dir truetreefilename truespeciestreepath"
else
	GENE_DIR=$1
	NUMGENES=$2
	TREEFILENAME=$3
	TRUE_GENEDIR=$4
	TRUETREEFILENAME=$5
	TRUESPECIESTREEPATH=$6
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
	NEWGENE_TREES_FILENAME="CAML_RAXML_WITHBINNING75_G"$NUMGENES".trees"
	rm -f $GENE_DIR"/"$NEWGENE_TREES_FILENAME
	for i in $(seq $GENE_BEGIN $GENE_END)
	do
		cat $GENE_DIR"/"$i"/"$TREEFILENAME >> $GENE_DIR"/"$NEWGENE_TREES_FILENAME
	done
	NEWGENE_ASTRID_FILENAME="astrid_CAML_RAXML_WITHBINNING75_G"$NUMGENES".tree"
	$ASTRID_BIN -i $GENE_DIR"/"$NEWGENE_TREES_FILENAME -o $GENE_DIR"/"$NEWGENE_ASTRID_FILENAME
	SPECIES_FILENAME="astral_CAML_RAXML_WITHBINNING75_G"$NUMGENES".tree"
	java -jar $ASTRAL_JAR -i $GENE_DIR"/"$NEWGENE_TREES_FILENAME -o $GENE_DIR"/"$SPECIES_FILENAME
	echo "Computation Done"
############################################################################################################################################	
	RESULT_FILENAME="result_CAML_RAXML_WITHBINNING75_G"$NUMGENES".txt"
	RESULT_FILE=$GENE_DIR"/"$RESULT_FILENAME
	rm -f $RESULT_FILE
	python $RES_SRC_FILE $TRUE_GENEDIR $TRUETREEFILENAME $GENE_DIR $TREEFILENAME $NUMGENES resulttmp.txt 
	echo "CA-ML genes vs True genes" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	python $RES_SRC_FILE $TRUESPECIESTREEPATH $GENE_DIR"/"$NEWGENE_ASTRID_FILENAME $GENE_DIR"/resulttmp.txt" 
	echo "CA-ML genes ASTRID" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
	python $RES_SRC_FILE $TRUESPECIESTREEPATH $GENE_DIR"/"$SPECIES_FILENAME $GENE_DIR"/resulttmp.txt" 
	echo "CA-ML genes ASTRAL" >> $RESULT_FILE
	cat $GENE_DIR"/resulttmp.txt" >> $RESULT_FILE
fi
