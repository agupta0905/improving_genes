__author__ = 'ashu'
import sys
from numpy import mean,median
def summarize(mdir,rprefix,numreplicates, filename):
    values_dict={}
    for i in range(1,numreplicates+1):
        try:
            f=open(mdir+'/'+rprefix+str(i)+'/'+filename,'r')
            for line in f:
                nextline =f.next()
                errorval=nextline.split(',')
                if line not in values_dict:
                    values_dict[line]=[[],[]]
                if len(errorval)==2:
                    values_dict[line][0].append(float(errorval[0]))
                    values_dict[line][1].append(float(errorval[1]))
                else:
                    values_dict[line][0].append(float(errorval[0]))
                    values_dict[line][1].append(float(errorval[0]))
            f.close()
        except:
            print mdir+'/'+rprefix+str(i)+'/'+filename,"Doesn't exist"
    
    f=open(mdir+'/'+filename,'w')
    for key in values_dict.keys():
        f.write(key)
        f.write(str(mean(values_dict[key][0]))+','+str(median(values_dict[key][1]))+'\n')
    f.close()
if __name__ == "__main__":  
    mdir=sys.argv[1]
    rprefix=sys.argv[2]
    numreplicates=int(sys.argv[3])
    filename=sys.argv[4]
    summarize(mdir,rprefix,numreplicates, filename) 