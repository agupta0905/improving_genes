import os
datasetdir='/u/sciteam/gupta1/scratch/astra2_dataset'
models = ['model.200.10000000.0.0000001','model.200.2000000.0.0000001','model.200.500000.0.0000001']
numgenes=50
for m in models:
    for r in range(1,11):
        mdir = datasetdir+'/'+m+'/'+str(r).zfill(2)
        f=open(mdir+'/50g_50t_50s_fasttree.tree','r')
        for linenumber,line in enumerate(f):
            gene = linenumber+1
            if gene > numgenes:
                break
            gene_dir=mdir+'/'+str(gene)
            if not os.path.exists(gene_dir):
                os.makedirs(gene_dir)
            outfile=open(gene_dir+'/50t_50s_fasttree.tree','w')
            outfile.write(line)
            outfile.close()
            #print gene,"Done"
        f.close()
        print m,r,"Done"
print "ALL Done"