import os,dendropy
datasetdir='/u/sciteam/gupta1/scratch/astra2_dataset'
models = ['model.200.10000000.0.0000001','model.200.2000000.0.0000001','model.200.500000.0.0000001']
numtaxa=50
numgenes=50
input_treename='true.tree'
out_treename='true_induced50.tree'
for m in models:
    for r in range(1,11):
        mdir = datasetdir+'/'+m+'/'+str(r).zfill(2)
        tree=dendropy.Tree.get(path=mdir+'/s_tree.trees', schema='newick')
        tree.retain_taxa_with_labels(map(lambda x: str(x), range(0,numtaxa)))
        f = open(mdir+'/s_tree_induced50.tree','w')
        f.write(tree.as_string('newick'))
        f.close()
#         for g in range(1,numgenes+1):
#             gene_dir=mdir+'/'+str(g)
#             tree=dendropy.Tree.get(path=gene_dir+'/'+input_treename, schema='newick')
#             tree.retain_taxa_with_labels(map(lambda x: str(x), range(0,numtaxa)))
#             f = open(gene_dir+'/'+out_treename,'w')
#             f.write(tree.as_string('newick'))
#             f.close()
        print m,r,"Done"
print "ALL Done"