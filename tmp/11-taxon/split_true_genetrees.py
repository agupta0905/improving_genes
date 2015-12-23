datasetdir='/u/sciteam/gupta1/scratch/11_taxon_dataset'
models = ['model.10.1800000.0.000000111','model.10.200000.0.000001000','model.10.5400000.0.000000037','model.10.600000.0.000000333']
numgenes=1000
for m in models:
    for r in range(1,11):
        mdir = datasetdir+'/'+m+'/'+str(r)
        f=open(mdir+'/truegenetrees','r')
        for linenumber,line in enumerate(f):
            gene = linenumber+1
            outfile=open(mdir+'/'+str(gene)+'/true.tree','w')
            outfile.write(line)
            outfile.close()
            #print gene,"Done"
        f.close()
        print m,r,"Done"
print "ALL Done"