import shutil
mdir = '/u/sciteam/gupta1/scratch/11_taxon_dataset/model.10.600000.0.000000333/1/relabeled_shortened_data_200_subset_1000'
output_dir= '/u/sciteam/gupta1/scratch/11_taxon_dataset/model.10.600000.0.000000333/1/200_sites'
numgenes=1000;
for i in range(1,numgenes+1):
    otreename= str(i).zfill(4)+'_fasttree_genetree'
    shutil.copy(mdir+'/'+otreename, output_dir+'/'+str(i)+'/fasttree_genetree_relabeled.tree')
    print i,"Done"

print "All Done"
