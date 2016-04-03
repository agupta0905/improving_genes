__author__ = 'ashu'
import sys,dendropy
def change_to_fasta( sequence_file_path):
    dna1 = dendropy.DnaCharacterMatrix.get(path=sequence_file_path, schema='phylip')
    pair=sequence_file_path.rsplit('.',1)
    outfilepath=pair[0]+'.fasta'
    dna1.write(path=outfilepath,schema='fasta')
if __name__ == "__main__":  
    sequence_file_path=sys.argv[1]
    change_to_fasta( sequence_file_path)