from random import SystemRandom
import math, json, nltk, string, os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

Max = 100

class BSO:

    def tokenize(self, text):
        tokens = []
        for token in nltk.word_tokenize(text.lower()):
            if token not in string.punctuation and token not in stop_words:
                tokens.append(lemmatizer.lemmatize(token))
        tokens = [token for token in tokens if token.isalpha() and len(token)>2]
        return tokens


    # CHECK imdex terms file
    def map_to_index(self, query, terms_map):

        #terms_map = json.load(open('index_terms','r'))
        query_term_indices = []
        for i in self.tokenize(query):
            if i not in terms_map.keys():
                continue
            query_term_indices.append(terms_map[i])

        return query_term_indices

        

    # Function to calculatethe relevant terms between the closed frequent pattern and users request. 
    def find_relevant(self, cluster_index, query_term_indices, freq_patterns):
        
        result=[]
        #print "freq_patterns ",freq_patterns,"  sl:  ",sl 
        result = [j for x in freq_patterns[cluster_index] for j in x if j in query_term_indices]
        result = list(set(result))
        #print "result:  ",result 
        return result


    #Main BSO Function 
    def bso(self, doc_clusters, doc_term_indices, freq_patterns,query,terms_map, solution_size, max_iter):

        #doc_term_indices = json.load(open('doc_transactions','r'))
        relevant_terms=[]
        no_of_clusters=len(doc_clusters)

        #Find relevant terms w.r.t each cluster
        for i in range(no_of_clusters):
            query_term_indices = self.map_to_index(query, terms_map)
            relevant_terms.append(self.find_relevant(i, query_term_indices, freq_patterns))
        #print relevant_terms
        if len(relevant_terms)==0:
            return None
        #BeeIniT: Solution of this problem
        #Initialize BeeInit : such that equal number of documents from each cluster.
        
        each_cluster=solution_size/no_of_clusters
        #print each_cluster

        # BeeInit=[]
        bees = []
        # TODO : Take care of case when each_cluster > no of elements in the cluster
        for i in doc_clusters:
            j = 0
            k = []
            while j < each_cluster:
                ele = SystemRandom().choice(i)
                if ele not in k:
                    # BeeInit.append(ele)
                    k.append(ele)
                    j += 1
            bees.append(k)

        # print "BeeInit: ",BeeInit
        # print "Bees: ",bees 
        number_of_iterations=0
        while number_of_iterations < Max :

            #Random number mu and probability to be compared in ordert update positions 
            random_number=SystemRandom().uniform(0, 1)
            #print random_number

            #Calculate the probability for each bee and compare with the random number generated 
            for i in range(0,len(bees)):
                for j in range(0,len(bees[i])):#Each Bee Solution 
                    num=0
                            #Read all the terms from file name into a list called doc_relevant to compare with the relevant_terms
                            
                    doc_relevant = doc_term_indices[bees[i][j]]
                    #print "iteration num: {}, doc_relevant: {}".format(number_of_iterations,doc_relevant)
                    #print "relevant_terms: ",relevant_terms[i]

                    num = len(list(set(doc_relevant) & set(relevant_terms[i])))
                    # TODO: Add case where relevant_terms is empty
                    if len(relevant_terms[i]) > 0:
                        probability=float(num)/len(relevant_terms[i])
                            #print probability
                            
                            #Replace the document if prob < u 
                    if len(relevant_terms[i]) < 1  or probability < random_number :
                        #To check from document and the bee list for matching documents and selecting the right					
                        while (1):
                            # case when len(bees[i]) = len(clusters[i])
                            if len(bees[i]) == len(doc_clusters[i]):
                                break 
                            my_elem = SystemRandom().choice(doc_clusters[i])	                                      
                            #print "my_elem: ",my_elem	
                            if my_elem not in bees[i]:
                                #print "old bees: {} bees[i]:{}".format(bees,bees[i]) 
                                bees[i].remove(bees[i][j])
                                bees[i].insert(j,my_elem)
                                #print " new bees: ",bees,"new bees[i]: ",bees[i]
                                break
                                
            #Merging of Dance Table
            # BeeInit=bees
            # TODO: Update bees after BeeInit is changed every time
            #print "iteration number: ",number_of_iterations 
            number_of_iterations+=1
        
        #print "Final Sloution is ",bees
        bees = [ j for i in bees for j in i ]
        return bees 
    

def load_json_files(files_list):
    returned_files = ()
    for i in files_list:
        returned_files= returned_files+(json.load(open(os.getcwd()+i,'r')),)
    return returned_files

if __name__=="__main__":
    #Input clusters and frequent patterns from the respective text files and user input is from terminal
    # clusters = [[1,2,6],[3,4,5],[7,8]]
    clusters, freq_patterns, doc_transactions, index_terms = load_json_files(['/json_files/doc_clusters','/json_files/cluster_cfi','/json_files/doc_transactions','/json_files/index_terms'])

    #clusters = json.load(open('json_files/doc_clusters','r'))
    #freq_patterns = json.load(open('json_files/cluster_cfi','r'))
    #doc_transactions = json.load(open('json_files/doc_transactions','r'))
    #index_terms = json.load(open('json_files/index_terms','r'))
    # freq_patterns =[[['hello','hi'],['hi']],[['i','am'],['busy']],['hi']]
    query=raw_input("What is the User Query: ")

    b = BSO()
    docs = b.bso(clusters,doc_transactions, freq_patterns,query,index_terms, 8, 100)
    print docs

