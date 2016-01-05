import numpy,os,re
dataset_dir='/u/sciteam/gupta1/scratch/11_taxon_dataset'
models=['model.10.1800000.0.000000111']#, 
        #'model.10.200000.0.000001000',
        #'model.10.5400000.0.000000037',
        #'model.10.600000.0.000000333']
num_replicates=10
def regex_filter(x):
    if re.match('result_*',x):
        return True
    else:
        return False
for m in models:
    mdir=dataset_dir+'/'+m
    flist=os.listdir(mdir+'/'+str(1))
    flist=filter(regex_filter,flist)
    for p in flist:
        mean_results=[]
        median_results=[]
        f=open(mdir+'/'+p,'w')
        for r in range(1,num_replicates+1):
            fin=open(mdir+'/'+str(r)+'/'+p,'r')
            line=fin.readline().strip()
            values= line.split(',')
            mean_results.append(float(values[0]))
            median_results.append(float(values[1]))    
            fin.close()    
        f.write(str(numpy.mean(mean_results))+','+str(numpy.median(median_results))+'\n')
        f.close()
        print 'Model',m,'Parameter',p,'Done'
        #print mean_results