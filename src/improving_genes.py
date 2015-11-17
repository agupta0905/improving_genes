__author__ = 'ashu'
import argparse
import dendropy
import operator
import math
import os,subprocess
from dendropy.calculate import treemeasure
def read_quartet_dict(dict_path):
    q_dict={}
    f=open(dict_path,'r')
    for line in f:
        quartet=line.split(':',1)[0]
        weight=float(line.split(':',1)[1])
        update(q_dict, quartet, weight)
    f.close()
    return q_dict
def write_quartet_dict(dictionary,outfilepath):
    f=open(outfilepath,'w')
    for key in dictionary:
        f.write(key+':'+("{0:.5f}".format(dictionary[key]))+'\n')
    f.close()
def formatted(i,j,k,l):
    if(j<i):
        i,j=j,i
    if(l<k):
        k,l=l,k
    if(k<i):
        return str(k)+','+str(l)+'|'+str(i)+','+str(j)
    else:
        return str(i)+','+str(j)+'|'+str(k)+','+str(l)
def update(dictionary, key,value):
    if(key in dictionary):
        dictionary[key]+=value
    else:
        dictionary[key]=value
def get_quartet_topology(t1,t2,t3,t4,distmatrix,weighting_quartets):
    sums=[distmatrix(t1,t2)+distmatrix(t3,t4),
          distmatrix(t1,t3)+distmatrix(t2,t4),
          distmatrix(t1,t4)+distmatrix(t2,t3)]
    min_index, min_value = min(enumerate(sums), key=operator.itemgetter(1))
    max_value=max(sums)
    quartet,weight=None,None
    if(min_index==0):
        quartet=formatted(t1.label,t2.label,t3.label,t4.label)   
    elif(min_index==1):
        quartet=formatted(t1.label,t3.label,t2.label,t4.label)
    else:
        quartet=formatted(t1.label,t4.label,t2.label,t3.label)
    
    if(not weighting_quartets):
        weight=1.0
    else :
        if(max_value!=0.0):
            weight=(max_value-min_value)/max_value
        else:
            weight=0.0
    return (quartet,weight)
def get_quartets(treepath,quartet_dict=None,weighting_quarets=False):
    local_dict={}
    tree=dendropy.Tree.get(path=treepath,schema='newick')
    #Update branch lengths
    for edge in tree.preorder_edge_iter():
        if(not weighting_quarets):
            edge.length=1.0
        else:
            if(edge.length==None):
                edge.length=0.0
    pdm = treemeasure.PatristicDistanceMatrix(tree)
    tns=tree.taxon_namespace
    numtaxa=len(tns)
    for t1 in range(0,numtaxa):
        for t2 in range(t1+1,numtaxa):
            for t3 in range(t2+1,numtaxa):
                for t4 in range(t3+1,numtaxa):
                    (quartet,weight)=get_quartet_topology(tns[t1],tns[t2],tns[t3],tns[t4],pdm,weighting_quarets)
                    update(local_dict,quartet,weight)
                    if(quartet_dict!=None):
                        update(quartet_dict,quartet,weight)
    return local_dict
def extractQuartets(gene_dir,numgenes,input_treefilename,output_quartetfilename,tmp_dir,
                    weighted_quartets=False,binning_dir=None,
                    confidence=None):
    #Select Bins
    bins=[]
    if(binning_dir==None):
        bins.append([])
        for i in range(1,numgenes+1):
            bins[0].append(i)
    else:
        if(not os.path.isfile(binning_dir+'/bin.0.txt')):
            bins.append([])
            for i in range(1,numgenes+1):
                bins[0].append(i)
        else:
            for i in range(0,numgenes):
                if(os.path.isfile(binning_dir+'/bin.'+str(i)+'.txt')):
                    bins.append([])
                    f=open(binning_dir+'/bin.'+str(i)+'.txt','r')
                    for line in f:
                        bins[i].append(int(line))
                    f.close()
                else:
                    break
    #Accumulate Quartets
    for bin_index in range(0,len(bins)):
        all_bin_quartets={}
        for i in bins[bin_index]:
            print "Accumulating for gene",i
            quartets_from_gene=get_quartets(gene_dir+'/'+str(i)+'/'+input_treefilename,
                        all_bin_quartets,
                        weighted_quartets)
            write_quartet_dict(quartets_from_gene,tmp_dir+'/quartets_gene_'+str(i)+'.txt')
            print "Quartet written for gene",i
        write_quartet_dict(all_bin_quartets,tmp_dir+'/accumulated_quartets_bin_'+str(bin_index)+'.txt')
        if(confidence!=None):
            upweight=math.ceil(max(confidence*len(bins[bin_index]),2))
            print "Upweight",upweight
            for i in bins[bin_index]:
                print "Adjusting for gene",i
                quartets_from_gene=read_quartet_dict(tmp_dir+'/quartets_gene_'+str(i)+'.txt')
                upweight_quartets=all_bin_quartets.copy()
                for q in quartets_from_gene:
                    upweight_quartets[q]+=((upweight-1)*quartets_from_gene[q])
                write_quartet_dict(upweight_quartets,gene_dir+'/'+str(i)+'/'+output_quartetfilename)
        else:
            for i in bins[bin_index]:
                write_quartet_dict(all_bin_quartets, gene_dir+'/'+str(i)+'/'+output_quartetfilename)               
def runwQMC(wqmc_bin_path,gene_dir,numgenes, output_quartetfilename, output_treefilename):
    cmd=wqmc_bin_path
    for i in range(1,numgenes+1):
        print "Running wqmc for gene",i
        input_quartet_filepath='qrtt='+gene_dir+'/'+str(i)+'/'+output_quartetfilename
        output_tree_filepath='otre='+gene_dir+'/'+str(i)+'/'+output_treefilename
        p= subprocess.Popen([cmd, input_quartet_filepath, 'weights=on', output_tree_filepath], stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
        out, err = p.communicate()
        print "wqmc stdout"
        print out
        print "wqmc stderr"
        print err
def processArguments():
    parser = argparse.ArgumentParser(description='Command Line Options')
    parser.add_argument("gene_dir", help="Path to gene directory")
    parser.add_argument("numgenes", type=int, help="Number of genes")
    parser.add_argument("input_treefilename", help="Filename of the input gene tree")
    parser.add_argument("output_quartetfilename", help="Filename of the weighted quartets of improved gene tree")
    parser.add_argument("tmp_dir", help="Path to tmp directory to store temporary files")
    parser.add_argument("-e","--weighted_quartets", 
                      help="Use branch lengths to get quartet weights",
                      action="store_true"
                      )
    parser.add_argument("-b","--binning_dir",help="Path to bin information")
    parser.add_argument("-c", "--confidence", type=float, 
                        help="Confidence in the initial tree")
    parser.add_argument("-w","--wqmc", nargs=2, help="Run wQMC to get tree", 
                        metavar=('wqmc_binary_path','output_treefilename'))
    return parser.parse_args()
if __name__ == "__main__":
    args=processArguments()
    extractQuartets(args.gene_dir, args.numgenes, args.input_treefilename, 
                    args.output_quartetfilename,
                    args.tmp_dir, weighted_quartets=args.weighted_quartets, 
                    binning_dir=args.binning_dir, 
                    confidence=args.confidence)
    if(args.wqmc!=None):
        runwQMC(args.wqmc[0],args.gene_dir,args.numgenes,args.output_quartetfilename, args.wqmc[1])