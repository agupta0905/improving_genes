import sys
sys.path.append('/u/sciteam/gupta1/improving_genes/tools')
from get_results import get_fnrate
dataset_dir='/u/sciteam/gupta1/scratch/astra2_dataset'
models = ['model.200.10000000.0.0000001','model.200.2000000.0.0000001','model.200.500000.0.0000001']
parameters=['astral_all_unimproved.trees',
            'astral_all_wqmc_nobinning_withbranches_noupweight.trees',
             'astral_all_wqmc_nobinning_withbranches_withupweight0.1.trees',
              'astral_all_wqmc_nobinning_withbranches_withupweight0.2.trees']
numreplicates=10
for r in range(1,numreplicates+1):
    for m in models:
        modeldir=dataset_dir+'/'+m+'/'+str(r).zfill(2)
        for p in parameters:
            outtreepath=modeldir+'/'+p
            true_species_treepath=modeldir+'/s_tree_induced50.tree'
            fn_rate=get_fnrate(true_species_treepath, outtreepath)
            f=open(modeldir+'/result_'+p,'w')
            f.write(str(fn_rate)+','+str(fn_rate)+'\n')
            f.close()
            print 'Replicate',r,'Model',m,'Parameter',p,'Done'