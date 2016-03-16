__author__ = 'ashu'
import sys,re
NUMLINES=7
def filter_res(filepath,parameter_regex,result_regex):
    pregex_compiled=re.compile(parameter_regex)
    rregex_compiled=re.compile(result_regex)
    f=open(filepath,'r')
    for line in f:
        if line.strip():
            if pregex_compiled.match(line):
                #print line, "matched"
                for i in range(7):
                    header=f.next()
                    res=f.next()
                    if rregex_compiled.match(header):
                        print res.replace(',','\t').strip()
if __name__ == "__main__":  
    filepath=sys.argv[1]
    parameter_regex=sys.argv[2]
    result_regex=sys.argv[3]
    filter_res(filepath,parameter_regex,result_regex)