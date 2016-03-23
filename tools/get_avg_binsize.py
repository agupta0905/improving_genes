__author__ = 'ashu'
import sys
def get_avg_binsize(bdir):
    count=0;
    num_genes=0;
    while(True):
        try:
            filepath=bdir+'/bin.'+str(count)+'.txt'
            num_genes+=sum(1 for line in open(filepath,'r') if line.rstrip())
        except:
            break;
        count+=1
    if count==0:
        return 0.0
    else:
        return float(num_genes)/float(count)
     
if __name__ == "__main__":  
    bdir=sys.argv[1]
    print get_avg_binsize(bdir)