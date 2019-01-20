import random
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
	solution_size=6
	each_cluster=solution_size/no_of_clusters
	#print each_cluster
	
	BeeInit=[]
        bees = []
        # TODO : Take care of case when each_cluster > no of elements in the cluster
        for i in clusters:
            j = 0
            k = []
            while j < each_cluster:
                ele = random.choice(i)
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
		random_number=random.uniform(0, 1)
		print random_number
	
		#Calculate the probability for each bee and compare with the random number generated 
		for i in range(0,len(bees)):
			for j in bees[i]:#Each Bee Solution 
				num=0
				#Read all the terms from file name into a list called doc_relevant to compare with the relevant_terms
				filename = "doc%s" % j
                                with open("Medline/text_files/"+filename) as f:
                                    """
                                    for line in f:
                                        # TODO clean this part
                                        l = line.replace('.','').replace(',','')
                                        a = l.split('  ')
                                        a = filter(None,a)
                                        a = [i for i in a if i != '\r']
                                    """
                                    s = f.read()
                                s = s.replace('.','').replace(',','').replace('\r\n','').replace('\r','')
                                doc_relevant = s.split()
				print doc_relevant
				print relevant_terms[i]
			
                                num = len(list(set(doc_relevant) & set(relevant_terms[i])))
                                # TODO: Add case where relevant_terms is empty
                                probability=float(num)/len(relevant_terms[i])
				#print probability
				
 				temp=[] #Temporary list to hold the document to be changed
				#Replace the document if prob < u 
				if probability < random_number :
                                        #To check from document and the bee list for matching documents and selecting the right					
					while (1):
						my_elem = random.choice(clusters[i])		
						if my_elem not in bees[i]:
							temp.append(my_elem)
							break
				#Else just append the document to the temp list
				else:
					temp.append(y)
			#Remove the old bee solution
			#Add the new bee solution 		
			bees.remove(bees[i])
                        # to make sure new bees[i] is placed at i index itself
			bees.insert(i,temp)
			print bees
		
		#Merging of Dance Table
		BeeInit=bees
                # TODO: Update bees after BeeInit is changed every time

	number_of_iterations+=1

	print "Final Sloution is ",BeeInit

#Input clusters and frequent patterns from the respective text files and user input is from terminal
clusters = [[1,2,6],[3,4,5],[7,8]]
freq_patterns =[[['hello','hi'],['hi']],[['i','am'],['busy']],['hi']]
query=raw_input("What is the User Query: ")

BSO(clusters,freq_patterns,query)

