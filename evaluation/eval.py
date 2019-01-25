import sys
import json
import os
sys.path.insert(0,os.getcwd())

import bso_ir

def file2list(f):
    file = open(f,'r').read()
    files = [x.split() for x in file.split('\n')]
    #print files
    last_query = int(files[-2][0])
    rel_list = [[] for i in xrange(last_query)]
    for i in files[:-1]:
        print "i: ",i
        rel_list[int(i[0])-1].append(int(i[2]))
        
    #print rel_list
    return rel_list 

def precision(rel_list,sol,index):
    rd = len(sol)
    count = 0
    for i in sol:
        if i in rel_list[index]:
            count += 1
    p = float(count)/rd
    return p

def recall(rel_list,sol,index):
    ard = len(rel_list[index])
    count = 0
    for i in sol:
        if i in rel_list[index]:
            count += 1
    r = float(count)/ard
    return r

def fmeasure(precision,recall):
    return float((2*recall*precision))/(recall+precision)


if __name__=="__main__":
    rel_list = file2list('./Medline/MED.REL')
    p = []
    r = []
    fm = []
    query = json.load(open('./Medline/query','r'))
    clusters = json.load(open('pct/doc_clusters','r'))
    freq_patterns = json.load(open('pct/cluster_cfi','r'))
    sol = []
    for q in query:
        sol = bso_ir.BSO(clusters,freq_patterns,q)
        sol = [j for i in sol for j in i]
        print sol 
        p.append(precision(rel_list,sol,query.index(q)))
        r.append(recall(rel_list,sol,query.index(q)))
        fm.append(fmeasure(p[query.index(q)],r[query.index(q)]))
    print "precision: ",p
    print "recall: ",r
    print "fm: ",fm


