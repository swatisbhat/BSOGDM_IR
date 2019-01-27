from random import SystemRandom
import math, json, nltk, string, os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

Max = 100


class BSO:

    def calc_fitness(self, retrieved_docs, doc_term_indices, query_term_indices):
        fitness_val = 0
        for rd in retrieved_docs:
            num = len(list(set(query_term_indices) & set(doc_term_indices[rd])))
            den = len(query_term_indices) * len(doc_term_indices[rd])
            fitness_val += float(num)/den
        return float(fitness_val)/len(retrieved_docs)

    def tokenize(self, text):
        tokens = []
        for token in nltk.word_tokenize(text.lower()):
            if token not in string.punctuation and token not in stop_words:
                tokens.append(lemmatizer.lemmatize(token))
        tokens = [token for token in tokens if token.isalpha() and len(token)>2]
        return list(set(tokens))



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
        
        doc_probabilities = [(x, 0) for x in xrange(len(doc_term_indices))]
        for i in range(no_of_clusters):
            for j in doc_clusters[i]:
                prob = len(list(set(doc_term_indices[j]) & set(relevant_terms[i])))
                if len(relevant_terms[i])>0:
                    doc_probabilities[j] = (j,\
                            float(prob)/len(relevant_terms[i]))
        doc_probabilities.sort(key= lambda x: x[1], reverse=True)
        BeeInit = [ doc_probabilities[x][0] for x in xrange(solution_size)]
            
        '''
        each_cluster=solution_size/no_of_clusters
        #print each_cluster

        BeeInit=[]
        bees = []
        # TODO : Take care of case when each_cluster > no of elements in the cluster
        for i in doc_clusters:
            j = 0
            k = []
            while j < each_cluster:
                ele = SystemRandom().choice(i)
                if ele not in k:
                    BeeInit.append(ele)
                    k.append(ele)
                    j += 1
            bees.append(k)

        # print "BeeInit: ",BeeInit
        # print "Bees: ",bees 
        number_of_iterations=0
        bee_regions = [i for i in xrange(no_of_clusters)]
        sources = [[i for i in xrange(no_of_clusters)] for j in xrange(no_of_clusters)]
        
        # TODO add fitness func
        fitness_val = 0
        prev_fitness = 0
        while number_of_iterations < Max: # and fitness_val - prev_fitness < 2 * prev_fitness:
            check_sources = 0
            for i in sources:
                if len(i)!=0:
                    check_sources = 1
            if check_sources == 0:
                break

            #print 'Iter: ', number_of_iterations
            #print 'Bees : ', bees
            #print 'Sources: ', sources
            #print 'Bee Regions: ', bee_regions
            #Calculate the probability for each bee and compare with the random number generated 
            for i in range(0,len(bees)):
                if len(sources[i])==0: continue

                for j in range(0,len(bees[i])):#Each Bee Solution 
                    
                            
                    #Random number mu and probability to be compared in ordert update positions 
                    random_number=SystemRandom().uniform(0, 1)
                    #print 'Mu : ',random_number
                    
                    #doc_relevant = doc_term_indices[bees[i][j]]
                    #print "iteration num: {}, doc_relevant: {}".format(number_of_iterations,doc_relevant)
                    #print "relevant_terms: ",relevant_terms[i]

                    probability  = doc_probabilities[bees[i][j]] 
                    #Add case where relevant_terms is empty
                    #if len(relevant_terms[bee_regions.index(i)]) > 0:
                    #   probability=float(num)/len(relevant_terms[bee_regions.index(i)])
                            #print probability
                            
                            #Replace the document if prob < u 
                    if probability < random_number :


                        potential_docs = [k for k in doc_clusters[bee_regions[i]] \
                                        if doc_probabilities[k] > probability]
                        x = 0
                        while len(potential_docs) == 0 and x < len(sources[i])-1:
                            sources[i].remove(bee_regions[i])
                            bee_regions[i] = SystemRandom().choice(sources[i])
                            
                            potential_docs = [k for k in doc_clusters[bee_regions[i]] if \
                                doc_probabilities[k] > probability]
                            x+=1

                        if x == len(sources[i]):
                            break

                        
                        x = 0
                        #To check from document and the bee list for matching documents and selecting the right					
                        while True and x < len(potential_docs):
                            # case when len(bees[i]) = len(clusters[i])
                            

                            my_elem = SystemRandom().choice(potential_docs)	                                      
                            #print "my_elem: ",my_elem	

                            if my_elem not in BeeInit:
                                #print "old bees: {} bees[i]:{}".format(bees,bees[i]) 
                                bees[i][j] = my_elem
                                #print " new bees: ",bees,"new bees[i]: ",bees[i]
                                BeeInit[i*each_cluster+j] = my_elem
                                break
                            x+=1  


            #Merging of Dance Table
            # BeeInit=bees
            # TODO: Update bees after BeeInit is changed every time
            #print "iteration number: ",number_of_iterations 
            number_of_iterations+=1
            #BeeInit = [ j for i in bees for j in i ]
        prev_fitness = fitness_val'''
        fitness_val = self.calc_fitness(BeeInit, doc_term_indices, query_term_indices)
        print 'Fitness Val : ',fitness_val
        print 'BEEinit: ', BeeInit
        print '######################\n'

        return BeeInit

    

def load_json_files(files_list):
    returned_files = ()
    for i in files_list:
        returned_files= returned_files+(json.load(open(os.getcwd()+i,'r')),)
    return returned_files

if __name__=="__main__":
    #Input clusters and frequent patterns from the respective text files and user input is from terminal
    # clusters = [[1,2,6],[3,4,5],[7,8]]
    clusters, freq_patterns, doc_transactions, index_terms = load_json_files(['/json_files/doc_clusters','/json_files/cluster_cfi','/json_files/doc_transactions','/json_files/index_terms'])

    query=raw_input("What is the User Query: ")

    b = BSO()
    docs = b.bso(clusters,doc_transactions, freq_patterns,query,index_terms, 8, 100)
    print docs

