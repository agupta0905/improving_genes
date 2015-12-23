import os
import sys
sys.path.append('/u/sciteam/gupta1/improving_genes/tools')
from get_results import get_results
numreplicates=10
numgenes=1000
dataset_dir='/u/sciteam/gupta1/scratch/11_taxon_dataset'
models=['model.10.1800000.0.000000111', 
        'model.10.200000.0.000001000',
        'model.10.5400000.0.000000037',
        'model.10.600000.0.000000333']
parameters=['unimproved']
for i in range(1,numreplicates+1):
    for midx in range(0,len(models)):
        for p in parameters:
            result_filepath=dataset_dir+'/'+models[midx]+'/'+str(i)+'/result_'+p+'.txt'
            if not os.path.isfile(result_filepath) :
                print result_filepath," Not found"
                rgenedir=dataset_dir+'/'+models[midx]+'/'+str(i)
                reftreefilename='true_relabeled.tree'
                ogenedir=dataset_dir+'/'+models[midx]+'/'+str(i)
                outputtreefilename='fasttree_genetree_relabeled.tree'
                outputfilename='/result_'+p+'.txt'
                get_results(rgenedir, reftreefilename,ogenedir,outputtreefilename,numgenes,outputfilename)