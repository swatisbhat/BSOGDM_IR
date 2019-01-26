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
        #print "i: ",i
        rel_list[int(i[0])-1].append(int(i[2]))
        
    #print rel_list
    return rel_list 

def eval(rel_list,sol,index):
    rd = len(sol)
    ard = len(rel_list[index])
    count = 0
    for i in sol:
        if i in rel_list[index]:
            count += 1
    p = float(count)/rd
    #print 'p ' ,p
    r = float(count)/ard
    if r==0 and p==0:
        return (p, r, 'NaN')
    fscore = float((2*r*p))/(r+p)
    return (p,r,fscore)


if __name__=="__main__":
    rel_list = file2list('./Medline/MED.REL')
    p = []
    r = []
    fm = []
    
    clusters, freq_patterns, doc_transactions, index_terms, queries = bso_ir.load_json_files(['/json_files/doc_clusters','/json_files/cluster_cfi','/json_files/doc_transactions','/json_files/index_terms','/Medline/query'])

    #query = json.load(open('./Medline/query','r'))
    #clusters = json.load(open('pct/doc_clusters','r'))
    #freq_patterns = json.load(open('pct/cluster_cfi','r'))
    sol = []
    solution_size = 8
    max_iter = 100
    b = bso_ir.BSO()
    for q in queries:
        sol = b.bso(clusters,doc_transactions,freq_patterns,q,index_terms,solution_size, max_iter)
        if sol is None:
            p.append(0)
            r.append(0)
            fm.append(None)
            #print 'p ', 0,'\nr ',0,'None'
            continue
        #sol = [j for i in sol for j in i]
        # print sol 

        eval_results_q = eval(rel_list, sol, queries.index(q))
        p.append(eval_results_q[0])
        r.append(eval_results_q[1])
        fm.append(eval_results_q[2])

    print "Precision: ",p,'\n\n'
    print "Recall: ",r,'\n\n'
    print "F-score: ",fm,'\n\n'



