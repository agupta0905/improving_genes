__author__ = 'ashu'
import sys,re
import dendropy
def relabel_alignment(inputfilepath,taxa_dictpath):
    mapping={}
    f=open(taxa_dictpath,'r')
    for line in f:
        key=line.split(' ',1)[0]
        value=line.split(' ',1)[1].replace('\n','')
        mapping[key]=value
    f.close()     
    tns=dendropy.TaxonNamespace()
    d1 = dendropy.DnaCharacterMatrix.get(path=inputfilepath, schema="fasta", taxon_namespace=tns)
    for t in tns:
        t.label=mapping[t.label]
    outfilepath=inputfilepath.rsplit('.',1)[0]+'_relabeled.phylip'
    d1.write(path=outfilepath,schema='phylip')
if __name__ == "__main__":  
    inputfilepath=sys.argv[1]
    taxa_dictpath=sys.argv[2]
    relabel_alignment(inputfilepath,taxa_dictpath)