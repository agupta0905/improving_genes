m1='model.10.5400000.0.000000037'
m3='model.10.600000.0.000000333'
presentmodel=m3
truegenesfile='/u/sciteam/gupta1/scratch/11_taxon_dataset/'+presentmodel+'/1/truegenetrees'
output_dir='/u/sciteam/gupta1/scratch/11_taxon_dataset/'+presentmodel+'/1/true_gene_trees'
f=open(truegenesfile,'r')
for linenumber,line in enumerate(f):
    gene = linenumber+1
    outfile=open(output_dir+'/'+str(gene)+'/true.tree','w')
    outfile.write(line)
    outfile.close()
    print gene,"Done"

print "ALL Done"