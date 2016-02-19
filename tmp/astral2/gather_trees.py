import os
numreplicates=10
numgenes=50
dataset_dir='/u/sciteam/gupta1/scratch/astra2_dataset'
models = ['model.200.10000000.0.0000001','model.200.2000000.0.0000001','model.200.500000.0.0000001']
parameters=['nobinning_withbranches_noupweight','nobinning_withbranches_withupweight0.1','nobinning_withbranches_withupweight0.2']
def setGeneOffset(gene_dir):
    flist = os.listdir(gene_dir)
    flist=filter(lambda x: x.isdigit(),flist)
    flist = map(lambda x: int(x) , flist)
    return min(flist)-1 
for i in range(1,numreplicates+1):
    for midx in range(0,len(models)):
        gene_dir=dataset_dir+'/'+models[midx]+'/'+str(i).zfill(2)
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
            fipath=gene_dir+'/'+str(g)+'/50t_50s_fasttree.tree'
            try:
                fi=open(fipath,'r')
                for line in fi:
                    f.write(line)
                fi.close()
            except:
                print "Unable to open file",fipath
        f.close()