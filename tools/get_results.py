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
def decode_bipartition(bp,tlist):
    res=''
    num_taxa=len(tlist)
    one_set=set()
    zero_set=set()
    for i in range(0,len(bp)):
        if bp[i]=='1':
            one_set.add(tlist[num_taxa-i-1])
        else:
            zero_set.add(tlist[num_taxa-i-1])
    for m in one_set:
        res+=(m+' ')
    res+='|'
    for m in zero_set:
        res+=(m+' ')
    return res

def get_bipartitions(tree):
    tns=tree.taxon_namespace
    bset=set()
    for n in tree.preorder_node_iter():
        if (n.is_internal() and (n.parent_node!=None)):
            bipartition=str(n.edge.bipartition)
            bset.add(decode_bipartition(bipartition,tns.labels()))
    return bset
             
def get_fnrate(reftreepath,outtreepath):
    tns = dendropy.TaxonNamespace()
    rtree = dendropy.Tree.get(path=reftreepath,schema='newick',
    taxon_namespace=tns)
    otree = dendropy.Tree.get(path=outtreepath,schema='newick',
    taxon_namespace=tns)
    rtree.encode_bipartitions()
    otree.encode_bipartitions()
    fn_rate=treecompare.false_positives_and_negatives(rtree, otree)[1]/float(len(tns)-3)
    return fn_rate

def get_results(rgenedir, reftreefilename,ogenedir,outputtreefilename,numgenes,outputfilename):
    gene_offset=setGeneOffset(rgenedir)
    print "Gene offset: ",gene_offset
    res=[]
    for i in range(1+gene_offset,gene_offset+numgenes+1):
        try:
            reftreepath=rgenedir+'/'+str(i)+'/'+reftreefilename
            outtreepath=ogenedir+'/'+str(i)+'/'+outputtreefilename
            fn_rate=get_fnrate(reftreepath, outtreepath)
            res.append(fn_rate)
            print "Result for",i,"Done"
        except:
            print '[ERROR][get_results.py] Unable to get result for',reftreepath,outtreepath
    res_mean,res_median=mean(res),median(res)
    f=open(ogenedir+'/'+outputfilename,'w')
    f.write(str(res_mean)+','+str(res_median)+'\n')
    f.close()
def get_results2(reftreepath,otreepath,outfilepath):
    fn_rate=get_fnrate(reftreepath, otreepath)
    f=open(outfilepath,'w')
    f.write(str(fn_rate)+'\n')
    f.close()
if __name__ == "__main__":
    if(len(sys.argv)==4):
        reftreepath=sys.argv[1]
        otreepath=sys.argv[2]
        outfilepath=sys.argv[3]
        get_results2(reftreepath,otreepath,outfilepath)
    else:
        rgenedir=sys.argv[1]
        reftreefilename=sys.argv[2]
        ogenedir=sys.argv[3]
        outputtreefilename=sys.argv[4]
        numgenes=int(sys.argv[5])
        outputfilename=sys.argv[6]
        get_results(rgenedir, reftreefilename,ogenedir,outputtreefilename,numgenes,outputfilename)    
    
