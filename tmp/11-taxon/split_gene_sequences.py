__author__ = 'ashu'
import sys,re

def split_gene_sequences(inputfilepath,genedir,numtaxa,numsites,outfilename):
    f=open(inputfilepath,'r')
    gene=0
    for line in f:
        if 'alignement' in line:
            flag=1
            gene=gene+1
            alignment_dict={}
            f.next()
            for i in range(1,numtaxa+1):
                pair=f.next().strip().split('\t',1)
                taxa=pair[0]
                sequence=pair[1]
                if(taxa != (str(i)+'.'+str(i)) or len(sequence)!=numsites):
                    print 'Taxa or length dont match for gene',gene
                    print taxa,i,sequence
                    flag=0
                    break;
                else:
                    alignment_dict[i]=sequence
            if flag!=0:
                fout=open(genedir+'/'+str(gene)+'/'+outfilename,'w')
                fout.write('11 '+str(numsites)+'\n')
                for x in range(1,numtaxa+1):
                    fout.write(str(x)+'\t'+alignment_dict[x]+'\n')
                fout.close()
    f.close()
            
if __name__ == "__main__":  
    inputfilepath=sys.argv[1]
    genedir=sys.argv[2]
    numtaxa=int(sys.argv[3])
    numsites=int(sys.argv[4])
    outfilename=sys.argv[5]
    split_gene_sequences(inputfilepath,genedir,numtaxa,numsites,outfilename)