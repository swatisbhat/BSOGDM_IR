import os
import re
import json

f = open(os.getcwd()+'/Medline/MED.QRY','r').read()
queries = re.split('[\r\n]?\.I [0-9]+\r\n\.W\r\n',f)

query = []

for q in queries:
    q = re.sub('\r\n|\r','  ',q)
    query.append(q)
    
json.dump(query[1:],open(os.getcwd()+"/Medline/query",'w'))

    


