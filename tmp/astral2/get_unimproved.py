import os
import sys
sys.path.append('/u/sciteam/gupta1/improving_genes/tools')
from get_results import get_results
numreplicates=10
numgenes=50
dataset_dir='/u/sciteam/gupta1/scratch/astra2_dataset'
models = ['model.200.10000000.0.0000001','model.200.2000000.0.0000001','model.200.500000.0.0000001']
parameters=['unimproved']
for i in range(1,numreplicates+1):
    for midx in range(0,len(models)):
        for p in parameters:
            result_filepath=dataset_dir+'/'+models[midx]+'/'+str(i).zfill(2)+'/result_'+p+'.txt'
            #if not os.path.isfile(result_filepath) :
            if True:
                print result_filepath," Not found"
                rgenedir=dataset_dir+'/'+models[midx]+'/'+str(i).zfill(2)
                reftreefilename='true_induced50.tree'
                ogenedir=dataset_dir+'/'+models[midx]+'/'+str(i).zfill(2)
                outputtreefilename='50t_50s_fasttree.tree'
                outputfilename='/result_'+p+'.txt'
                get_results(rgenedir, reftreefilename,ogenedir,outputtreefilename,numgenes,outputfilename)