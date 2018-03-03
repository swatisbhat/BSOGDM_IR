import os
import re

f = open(os.getcwd()+'/Medline/MED.ALL','r').read()
documents = re.split('[\r\n]?\.I [0-9]+\r\n\.W\r\n',f)


count = 0
for doc in documents:
    
    s = open(os.getcwd()+'/Medline/text_files/doc'+str(count),'w')
    s.write(doc)
    s.close()
    count += 1
