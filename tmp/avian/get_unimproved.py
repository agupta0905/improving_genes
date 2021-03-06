import os
import sys
sys.path.append('/u/sciteam/gupta1/improving_genes/tools')
from get_results import get_results
numreplicates=10
numgenes=50
dataset_dir='/u/sciteam/gupta1/scratch/avian_dataset'
models=['0.5X-1000-500','1X-1000-250', '1X-1000-500', '2X-1000-500']
tmodels=['0.5X-1000-true','1X-1000-true', '1X-1000-true', '2X-1000-true']
parameters=['unimproved']
for i in range(1,numreplicates+1):
    for midx in range(0,len(models)):
        for p in parameters:
            result_filepath=dataset_dir+'/'+models[midx]+'/R'+str(i)+'/result_'+p+'.txt'
            #if not os.path.isfile(result_filepath) :
            if True:   
                print result_filepath," Not found"
                rgenedir=dataset_dir+'/'+tmodels[midx]+'/R'+str(i)
                reftreefilename='true_relabeled.gt'
                ogenedir=dataset_dir+'/'+models[midx]+'/R'+str(i)
                outputtreefilename='raxmlboot.gtrgamma/RAxML_bipartitions.final_relabeled.f200'
                outputfilename='/result_'+p+'.txt'
                get_results(rgenedir, reftreefilename,ogenedir,outputtreefilename,numgenes,outputfilename)