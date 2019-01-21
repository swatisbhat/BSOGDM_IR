from random import SystemRandom
import math

Max = 1000

# Function to calculatethe relevant terms between the closed frequent pattern and users request. 
def find_relevant(no):
	sl=query.split(' ')
	result=[]
        #print "freq_patterns ",freq_patterns,"  sl:  ",sl 
        result = [i for x in freq_patterns[no] for i in x if i in sl]
        result = list(set(result))
        print "result:  ",result 
	return result

#Main BSO Function 
def BSO(clusters,freq_patterns,query):

	relevant_terms=[]
	no_of_clusters=len(clusters)
 
	#Find relevant terms w.r.t each cluster
	for i in range(0,no_of_clusters):
		relevant_terms.append(find_relevant(i))
	#print relevant_terms

	#BeeIniT: Solution of this problem
	#Initialize BeeInit : such that equal number of documents from each cluster.
	solution_size=8
	each_cluster=solution_size/no_of_clusters
	#print each_cluster
	
	BeeInit=[]
        bees = []
        # TODO : Take care of case when each_cluster > no of elements in the cluster
        for i in clusters:
            j = 0
            k = []
            while j < each_cluster:
                ele = SystemRandom().choice(i)
                if ele not in BeeInit:
                    BeeInit.append(ele)
                    k.append(ele)
                    j += 1
            bees.append(k)

        print "BeeInit: ",BeeInit
        print "Bees: ",bees 
	number_of_iterations=0
	while number_of_iterations < Max :

		#Random number u and probability to be compared in ordert update positions 
		random_number=SystemRandom().uniform(0, 1)
		print random_number
	
		#Calculate the probability for each bee and compare with the random number generated 
		for i in range(0,len(bees)):
			for j in range(0,len(bees[i])):#Each Bee Solution 
				num=0
				#Read all the terms from file name into a list called doc_relevant to compare with the relevant_terms
				filename = "doc%s" % bees[i][j]
                                with open("Medline/text_files/"+filename) as f:
                                    s = f.read()
                                s = s.replace('.','').replace(',','').replace('\r\n','').replace('\r','')
                                doc_relevant = s.split()
                                #print "iteration num: {}, doc_relevant: {}".format(number_of_iterations,doc_relevant)
                                #print "relevant_terms: ",relevant_terms[i]
			
                                num = len(list(set(doc_relevant) & set(relevant_terms[i])))
                                # TODO: Add case where relevant_terms is empty
                                if len(relevant_terms[i]) > 0:
                                    probability=float(num)/len(relevant_terms[i])
				#print probability
				
				#Replace the document if prob < u 
				if probability < random_number or len(relevant_terms[i]) < 1 :
                                        #To check from document and the bee list for matching documents and selecting the right					
					while (1):
                                                # case when len(bees[i]) = len(clusters[i])
                                                if len(bees[i]) == len(clusters[i]):
                                                    break 
                                                my_elem = SystemRandom().choice(clusters[i])	                                      
                                                print "my_elem: ",my_elem	
						if my_elem not in bees[i]:
                                                    print "old bees: {} bees[i]:{}".format(bees,bees[i]) 
						    bees[i].remove(bees[i][j])
                                                    bees[i].insert(j,my_elem)
                                                    print " new bees: ",bees,"new bees[i]: ",bees[i]
						    break
                                                #print "inwhile "
		#Merging of Dance Table
		BeeInit=bees
                # TODO: Update bees after BeeInit is changed every time
                print "iteration number: ",number_of_iterations 
	        number_of_iterations+=1

	print "Final Sloution is ",BeeInit

#Input clusters and frequent patterns from the respective text files and user input is from terminal
clusters = [[1,2,6],[3,4,5],[7,8]]
freq_patterns =[[['hello','hi'],['hi']],[['i','am'],['busy']],['hi']]
query=raw_input("What is the User Query: ")

BSO(clusters,freq_patterns,query)

