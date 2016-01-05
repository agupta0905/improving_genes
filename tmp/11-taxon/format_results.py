import os,re
dataset_dir='/u/sciteam/gupta1/scratch/11_taxon_dataset'
models=['model.10.1800000.0.000000111']#, 
        #'model.10.200000.0.000001000',
        #'model.10.5400000.0.000000037',
        #'model.10.600000.0.000000333']
order=['noupweight','0.1','0.2','unimproved']
def regex_filter(x):
    if re.match('result_*',x):
        return True
    else:
        return False
def fmt(f):
    line = f.readline().strip()
    values=line.split(',')
    mean=round(float(values[0]),3)
    median=round(float(values[1]),3)
    return str(mean)+','+str(median)
for m in models:
    mdir=dataset_dir+'/'+m
    flist=os.listdir(mdir)
    flist=filter(regex_filter,flist)
    species_list=[]
    gene_list=[]
    for element in flist:
        if 'astral' in element:
            species_list.append(element)
        else:
            gene_list.append(element)
    fout=open(mdir+'/all_results_50sites.csv','w')
    for od in order:
        gene=None
        for  g in gene_list:
            if od in g:
                gene=g
                break
        species=None
        for  s in species_list:
            if od in s:
                species=s
                break
        res_line=''
        f=open(mdir+'/'+gene,'r')
        res_line=fmt(f)
        f.close()
        f=open(mdir+'/'+species,'r')
        res_line=res_line+','+fmt(f)
        f.close()
        fout.write(res_line+'\n')
        print 'Model',m,'Order',od,'Done'
    fout.close()