import os,re
dataset_dir='/u/sciteam/gupta1/scratch/mammalian_dataset'
models=['0.5X-200-500','1X-200-500', '1X-200-1000', '2X-200-500']
order=['noupweight','0.1','0.2','unimproved']
def regex_filter(x):
    if re.match('result_*',x) and ('withbinning' in x or 'unimproved' in x):
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
    fout=open(mdir+'/all_results.csv','w')
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