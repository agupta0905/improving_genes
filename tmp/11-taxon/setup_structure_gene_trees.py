import shutil
datasetdir='/u/sciteam/gupta1/scratch/11_taxon_dataset'
#models = ['model.10.1800000.0.000000111','model.10.200000.0.000001000','model.10.5400000.0.000000037','model.10.600000.0.000000333']
models = ['model.10.1800000.0.000000111']
numgenes=1000;
for m in models:
    for r in range(1,11):
        mdir=datasetdir+'/'+m+'/'+str(r)
        for i in range(1,numgenes+1):
            otreename= str(i).zfill(4)+'_fasttree_genetree'
            shutil.copy(mdir+'/relabeled_shortened_data_50_subset_1000/'+otreename, mdir+'/'+str(i)+'/fasttree_genetree_relabeled_50l.tree')
        print m,r,"Done"
print "All Done"
