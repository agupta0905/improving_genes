import numpy,os,re
dataset_dir='/u/sciteam/gupta1/scratch/mammalian_dataset'
models=['0.5X-200-500','1X-200-500', '1X-200-1000', '2X-200-500']
num_replicates=10
re.compile('result_*')
def regex_filter(x):
    if re.match(x):
        return True
    else:
        return False
for m in models:
    mdir=dataset_dir+'/'+m
    mean_results=[]
    median_results=[]
    flist=os.listdir(mdir+'/R'+str(1))
    flist=filter(regex_filter,flist)
    for p in flist:
        f=open(mdir+'/'+p,'w')
        for r in range(1,num_replicates+1):
            fin=open(mdir+'/R'+str(r)+'/'+p,'r')
            line=fin.readline().strip()
            values= line.split(',')
            mean_results.append(float(values[0]))
            median_results.append(float(values[1]))    
            fin.close()    
        f.write(str(numpy.mean(mean_results))+','+str(numpy.median(median_results))+'\n')
        f.close()
        print 'Model',m,'Parameter',p,'Done'