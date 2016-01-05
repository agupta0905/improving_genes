__author__ = 'ashu'
import sys
def get_totaltaxa(filepath):
    f=open(filepath,'r')
    line=f.readline()
    f.close()
    return int(line.split(' ',1)[0])
def sample_data(filepath,outfilepath,num_taxa,num_sites,num_genes):
    total_taxa=get_totaltaxa(filepath)
    f=open(filepath,'r')
    f_out=open(outfilepath,'w')
    curr_gene=0
    for line in f:
        line=line.strip()
        if line:
            words=line.split(' ',1)
            currtaxa=int(words[0])
            if int(currtaxa==total_taxa):
                curr_gene+=1
                if curr_gene>num_genes:
                    break
                f_out.write(str(num_taxa)+' '+str(num_sites)+'\n')
            elif currtaxa<num_taxa:
                words[1]=words[1].strip()
                f_out.write(str(currtaxa)+' '+words[1][:num_sites]+'\n')
    f.close()
    f_out.close()
                
if __name__ == "__main__":
    filepath = sys.argv[1]
    outfilepath=sys.argv[2]
    num_taxa=int(sys.argv[3])
    num_sites=int(sys.argv[4])
    num_genes=int(sys.argv[5])
    sample_data(filepath,outfilepath,num_taxa,num_sites,num_genes)