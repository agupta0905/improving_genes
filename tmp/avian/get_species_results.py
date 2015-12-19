import sys
sys.path.append('/u/sciteam/gupta1/improving_genes/tools')
from get_results import get_fnrate
dataset_dir='/u/sciteam/gupta1/scratch/avian_dataset'
true_species_treepath='/u/sciteam/gupta1/scratch/avian_dataset/species_relabeled.tree'
models=['0.5X-1000-500','1X-1000-250', '1X-1000-500', '2X-1000-500']
parameters=['astral_all_unimproved.trees',
            'astral_all_wqmc_nobinning_withbranches_noupweight.trees',
             'astral_all_wqmc_nobinning_withbranches_withupweight0.1.trees',
              'astral_all_wqmc_nobinning_withbranches_withupweight0.1.trees']
numreplicates=10
for r in range(1,numreplicates+1):
    for m in models:
        modeldir=dataset_dir+'/'+m+'/R'+r
        for p in parameters:
            outtreepath=modeldir+'/'+p
            fn_rate=get_fnrate(true_species_treepath, outtreepath)
            f=open(modeldir+'/result_'+p,'w')
            f.write(str(fn_rate)+','+str(fn_rate)+'\n')
            f.close()
            print 'Replicate',r,'Model',m,'Parameter',p,'Done'