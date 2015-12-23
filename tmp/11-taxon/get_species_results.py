import sys
sys.path.append('/u/sciteam/gupta1/improving_genes/tools')
from get_results import get_fnrate
dataset_dir='/u/sciteam/gupta1/scratch/11_taxon_dataset'
models=['model.10.1800000.0.000000111', 
        'model.10.200000.0.000001000',
        'model.10.5400000.0.000000037',
        'model.10.600000.0.000000333']
parameters=['astral_all_unimproved.trees',
            'astral_all_wqmc_nobinning_withbranches_noupweight.trees',
             'astral_all_wqmc_nobinning_withbranches_withupweight0.1.trees',
              'astral_all_wqmc_nobinning_withbranches_withupweight0.2.trees']
numreplicates=10
for r in range(1,numreplicates+1):
    for m in models:
        modeldir=dataset_dir+'/'+m+'/'+str(r)
        for p in parameters:
            outtreepath=modeldir+'/'+p
            true_species_treepath=modeldir+'/S_relabeled_tree.trees'
            fn_rate=get_fnrate(true_species_treepath, outtreepath)
            f=open(modeldir+'/result_'+p,'w')
            f.write(str(fn_rate)+','+str(fn_rate)+'\n')
            f.close()
            print 'Replicate',r,'Model',m,'Parameter',p,'Done'