__author__ = 'ashu'
import sys
def filter_genes_binning(genedir,treefilename,tmpfilename,numgenes):
    f=open(tmpfilename,'r')
    if(genedir[-1]=='/'):
        genedir=genedir[0:-1]
    genes=[]
    for line in f:
        #print "Line",line
        #print "genedir",genedir
        line = line[len(genedir)+1:]
        if line[0]=='/':
            line=line[1:]
        genes.append(int(line.split('/',1)[0]))
    f.close()
    genes.sort()
    f=open(tmpfilename,'w')
    fgenes=open(tmpfilename+'.genes','w')
    for g in genes[:numgenes]:
        f.write(genedir+'/'+str(g)+'/'+treefilename+'\n')
        fgenes.write(str(g)+'\n')
    f.close()
    fgenes.close()
if __name__ == "__main__":
    genedir=sys.argv[1]
    treefilename=sys.argv[2]
    tmpfilename=sys.argv[3]
    numgenes=int(sys.argv[4])
    filter_genes_binning(genedir,treefilename,tmpfilename,numgenes)
    
