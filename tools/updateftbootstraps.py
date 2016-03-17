__author__ = 'ashu'
import dendropy,numpy,sys
def updateftbootstraps(treepath):
    t=dendropy.Tree.get(path=treepath,schema='newick')
    for n in t.preorder_node_iter():
        if n.label!=None:
            x=float(n.label)*100
            n.label=str(int(x))
    outtreepath=treepath.rsplit('.',1)[0]+'_ftbootstraps'+treepath.rsplit('.',1)[1]
    t.write(path=outtreepath,schema='newick')
if __name__ == "__main__":
    treepath=sys.argv[1]
    updateftbootstraps(treepath)
