__author__ = 'ashu'
import dendropy,numpy,sys
def printbootsraps(treepath):
    t=dendropy.Tree.get(path=treepath,schema='newick')
    bslist=[]
    for n in t.preorder_node_iter():
        if n.label!=None:
            print n.label
            bslist.append(float(n.label))
    print "Avg bootstrap", numpy.mean(bslist)

if __name__ == "__main__":
    treepath=sys.argv[1]
    printbootsraps(treepath)
