__author__ = 'ashu'
import sys
def split_gene_sequences(inputfilepath,genedir,numtaxa,numsites,outfilename):
    f=open(inputfilepath,'r')
    gene=0
    for line in f:
        if str(numtaxa)+' '+str(numsites) in line:
            flag=1
            gene=gene+1
            alignment_dict={}
            for i in range(1,numtaxa+1):
                pair=f.next().strip().split(' ',1)
                taxa=pair[0]
                sequence=pair[1]
                if(len(sequence)!=numsites):
                    print 'length dont match for gene',gene
                    print taxa,i,sequence
                    flag=0
                    break;
                else:
                    alignment_dict[taxa]=sequence
            if flag!=0:
                fout=open(genedir+'/'+str(gene)+'/'+outfilename,'w')
                fout.write(str(numtaxa)+' '+str(numsites)+'\n')
                for x in range(0,numtaxa):
                    fout.write(str(x)+' '+alignment_dict[str(x)]+'\n')
                fout.close()
                print gene,"Gene Done"
    f.close()
            
if __name__ == "__main__":  
    inputfilepath=sys.argv[1]
    genedir=sys.argv[2]
    numtaxa=int(sys.argv[3])
    numsites=int(sys.argv[4])
    outfilename=sys.argv[5]
    split_gene_sequences(inputfilepath,genedir,numtaxa,numsites,outfilename)