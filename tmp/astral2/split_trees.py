import os
datasetdir='/u/sciteam/gupta1/scratch/astral2_dataset'
models = ['model.200.10000000.0.0000001','model.200.2000000.0.0000001','model.200.10000000.0.000001','model.200.2000000.0.000001']
numgenes=1000
for m in models:
    for s in [50,100,200]:
        for r in range(1,11):
            mdir = datasetdir+'/'+m+'/'+str(r).zfill(2)
            try:
                f=open(mdir+'/1000g_50t_'+str(s)+'s.trees','r')
                for linenumber,line in enumerate(f):
                    gene = linenumber+1
                    if gene > numgenes:
                        break
                    gene_dir=mdir+'/'+str(gene)
                    if not os.path.exists(gene_dir):
                        os.makedirs(gene_dir)
                    outfile=open(gene_dir+'/50t_'+str(s)+'s.tree','w')
                    outfile.write(line)
                    outfile.close()
                f.close()
            except:
                print mdir,"Not exists"
            print m,r,s,"Done"
print "ALL Done"