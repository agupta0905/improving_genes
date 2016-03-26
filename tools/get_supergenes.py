__author__ = 'ashu'
import sys
def get_alignment_dict(alignmentfilepath,numtaxa,numsites):
    f=open(alignmentfilepath,'r')
    header=f.next().strip().split(' ',1)
    alignment_dict={}
    if int(header[0])!=numtaxa or int(header[1])!=numsites:
        print 'ERROR numtaxa or numsites donot match'
        exit()
    for line in f:
        line=line.strip()
        if line:
            pair=line.split(' ',1)
            if(len(pair[1])!=numsites):
                print "Error numsites dont match"
                print "Found",len(pair[1]),"Expected",numsites
            alignment_dict[pair[0]]=pair[1]
            
    f.close()
    return alignment_dict

def get_supergenes(binning_dir,bindef_filename,gene_dir,alignment_filename, numtaxa, numsites):
    pairs=bindef_filename.rsplit('.',1)
    supergene_file=open(binning_dir+'/supergene_'+pairs[0]+'.phylip','w')
    partition_file=open(binning_dir+'/partition_'+pairs[0]+'.txt','w')
    bin_file=open(binning_dir+'/'+bindef_filename,'r')
    genes=[]
    supergene_alignment_dict={}
    for line in bin_file:
        if line.strip():
            genes.append(line.strip())
    bin_file.close()
    for g in genes:
        gene_alignment_dict=get_alignment_dict(gene_dir+'/'+g+'/'+alignment_filename, numtaxa, numsites)
        if not supergene_alignment_dict:
            supergene_alignment_dict=gene_alignment_dict
        else:
            for k in gene_alignment_dict:
                supergene_alignment_dict[k]=supergene_alignment_dict[k]+gene_alignment_dict[k]
    supergene_file.write(str(numtaxa)+' '+str(numsites*len(genes))+'\n')
    for k in supergene_alignment_dict:
        supergene_file.write(k+'\t'+supergene_alignment_dict[k]+'\n')
    supergene_file.close()
    for idx,g in enumerate(genes):
        start=idx*numsites+1
        end=start+numsites-1
        partition_file.write('DNA, gene'+g+'='+str(start)+'-'+str(end)+'\n')
    partition_file.close()
if __name__ == "__main__":
    binning_dir=sys.argv[1]
    bindef_filename=sys.argv[2]
    gene_dir=sys.argv[3]
    alignment_filename=sys.argv[4]
    numtaxa=int(sys.argv[5])
    numsites=int(sys.argv[6])
    get_supergenes(binning_dir,bindef_filename,gene_dir,alignment_filename,numtaxa,numsites)