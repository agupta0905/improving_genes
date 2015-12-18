__author__ = 'ashu'
import sys,os
import dendropy
from dendropy.calculate import treecompare
from numpy import mean,median
def setGeneOffset(gene_dir):
    flist = os.listdir(gene_dir)
    flist=filter(lambda x: x.isdigit(),flist)
    flist = map(lambda x: int(x) , flist)
    return min(flist)-1  
def get_results(rgenedir, reftreefilename,ogenedir,outputtreefilename,numgenes,outputfilename):
    gene_offset=setGeneOffset(rgenedir)
    print "Gene offset: ",gene_offset
    res=[]
    for i in range(1+gene_offset,gene_offset+numgenes+1):
        tns = dendropy.TaxonNamespace()
        reftreepath=rgenedir+'/'+str(i)+'/'+reftreefilename
        outtreepath=ogenedir+'/'+str(i)+'/'+outputtreefilename
        rtree = dendropy.Tree.get(path=reftreepath,schema='newick',
        taxon_namespace=tns)
        otree = dendropy.Tree.get(path=outtreepath,schema='newick',
        taxon_namespace=tns)
        rtree.encode_bipartitions()
        otree.encode_bipartitions()
        fn_rate=treecompare.false_positives_and_negatives(rtree, otree)[1]/float(len(tns)-3)
        res.append(fn_rate)
        print "Result for",i,"Done"
    res_mean,res_median=mean(res),median(res)
    f=open(ogenedir+'/'+outputfilename,'w')
    f.write(str(res_mean)+','+str(res_median)+'\n')
    f.close()
if __name__ == "__main__":
    rgenedir=sys.argv[1]
    reftreefilename=sys.argv[2]
    ogenedir=sys.argv[3]
    outputtreefilename=sys.argv[4]
    numgenes=int(sys.argv[5])
    outputfilename=sys.argv[6]
    get_results(rgenedir, reftreefilename,ogenedir,outputtreefilename,numgenes,outputfilename)    
    
