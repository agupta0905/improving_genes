truegenesfile='/u/sciteam/gupta1/scratch/11_taxon_dataset/model.10.5400000.0.000000037/1/truegenetrees'
output_dir='/u/sciteam/gupta1/scratch/11_taxon_dataset/model.10.5400000.0.000000037/1/true_gene_trees'
f=open(truegenesfile,'r')
for linenumber,line in enumerate(f):
    gene = linenumber+1
    outfile=open(output_dir+'/'+str(gene)+'/true.tree','w')
    outfile.write(line)
    outfile.close()
    print gene,"Done"

print "ALL Done"