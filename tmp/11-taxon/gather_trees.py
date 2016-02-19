import os
numreplicates=10
numgenes=50
dataset_dir='/u/sciteam/gupta1/scratch/11_taxon_dataset'
models=['model.10.1800000.0.000000111', 
        'model.10.200000.0.000001000',
        'model.10.5400000.0.000000037',
        'model.10.600000.0.000000333']
parameters=['nobinning_withbranches_noupweight','nobinning_withbranches_withupweight0.1','nobinning_withbranches_withupweight0.2']
def setGeneOffset(gene_dir):
    flist = os.listdir(gene_dir)
    flist=filter(lambda x: x.isdigit(),flist)
    flist = map(lambda x: int(x) , flist)
    return min(flist)-1 
for i in range(1,numreplicates+1):
    for midx in range(0,len(models)):
        gene_dir=dataset_dir+'/'+models[midx]+'/'+str(i)
        gene_offset=setGeneOffset(gene_dir)
        print "Gene offset set for genedir",gene_dir, 'to', gene_offset
        for p in parameters:
            f=open(gene_dir+'/all_wqmc_'+p+'.trees','w')
            for g in range(1+gene_offset,gene_offset+1+numgenes):
                fipath=gene_dir+'/'+str(g)+'/wqmc_'+p+'.tree'
                try:
                    fi=open(fipath,'r')
                    for line in fi:
                        f.write(line)
                    fi.close()
                except:
                    print "Unable to open file",fipath
            f.close()
        #For unimproved
        f=open(gene_dir+'/all_unimproved'+'.trees','w')
        for g in range(1+gene_offset,gene_offset+1+numgenes):
            fipath=gene_dir+'/'+str(g)+'/fasttree_genetree_relabeled.tree'
            try:
                fi=open(fipath,'r')
                for line in fi:
                    f.write(line)
                fi.close()
            except:
                print "Unable to open file",fipath
        f.close()