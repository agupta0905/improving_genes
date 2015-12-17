__author__ = 'ashu'
import os,sys
import dendropy
def relabel(tdict,tfilepath):
    toutfilepath=tfilepath.rsplit('.',1)[0]+'_relabeled'+'.'+tfilepath.rsplit('.',1)[1]
    tt=dendropy.Tree.get(
        path=tfilepath,
        schema='newick')
    for i in range(0,len(tt.taxon_namespace)):
        tt.taxon_namespace[i].label=tdict[tt.taxon_namespace[i].label]
    tt.write(path=toutfilepath,schema='newick')

def setGeneOffset(gene_dir):
    flist = os.listdir(gene_dir)
    flist=filter(lambda x: x.isdigit(),flist)
    flist = map(lambda x: int(x) , flist)
    return min(flist)-1  
    
def relabeler_trees(genedir,treefilename,t_dict_path,g):
    gene_offset = setGeneOffset(genedir)
    print "Gene offset set: ", gene_offset
    mapping={}
    f=open(t_dict_path,'r')
    for line in f:
        key=line.split(' ',1)[0]
        value=line.split(' ',1)[1].replace('\n','')
        mapping[key]=value
    f.close()
    for i in range(1+gene_offset,g+1+gene_offset):
        relabel(mapping, genedir+'/'+str(i)+'/'+treefilename)
        print i," Relabeled"

if __name__ == "__main__":
    genedir=sys.argv[1]
    treefilename=sys.argv[2]
    taxa_dict_path=sys.argv[3]
    numgenes=int(sys.argv[4])
    relabeler_trees(genedir, treefilename,taxa_dict_path,numgenes)    
    
