import random
import math

#Function to remove duplicate values from the relevant terms 
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

# Function to calculatethe relevant terms between the closed frequent pattern and users request. 
def find_relevant(no):
	sl=query.split(' ')
	#print "----------- SL : ",sl
	result=[]
	for x in freq_patterns[no]:
		#print "x:",x
		for y in sl:
			#print "*** y : ",y
			if (y in x):
				result.append(y)
	#print "-----RESULT1 : ",result
	result = Remove(result)
	#print "-----RESULT2 : ",result
	return result

#Main BSO Function 
def BSO(clusters,freq_patterns,query):

	relevant_terms=[]
	cluster_length=len(clusters)
 
	#Find relevant terms w.r.t each cluster
	for i in range(0,cluster_length):
		relevant_terms.append(find_relevant(i))
	#print relevant_terms

	#BeeIniT: Solution of this problem
	#Initialize BeeInit : such that equal number of documents from each cluster.
	solution_size=6
	each_cluster=solution_size/cluster_length
	#print each_cluster
	
	BeeInit=[]
	for x in clusters:
		bee_len=len(BeeInit)
		compar=bee_len+each_cluster
		while bee_len!=compar:
			my_elem = random.choice(x)
			#print my_elem	
			if my_elem not in BeeInit:
				BeeInit.append(my_elem)
				bee_len+=1
							
	#print BeeInit
	number_of_iterations=0
	while number_of_iterations ! = Max :
		#Each Bee gets One cluster for searching 
		no_of_bees=cluster_length
		bees=[]
	
		#Each bee should be allocated its region according to the cluster 
		for y in clusters:
			bee_dummy_list=[]
			for x in BeeInit:	
				if x in y:
					bee_dummy_list.append(x)
				#print bee_dummy_list
			bees.append(bee_dummy_list)
		#print bees
		
		#Random number u and probability to be compared in ordert update positions 
		random_number=random.uniform(0, 1)
		print random_number
		
	
		#Calculate the probability for each bee and compare with the random number generated 
		for x in bees:
			for y in x:#Each Bee Solution 
				num=0
				indexes=bees.index(x)
				den=len(relevant_terms[indexes])
				#Read all the terms from file name into a list called doc_relevant to compare with the relevant_terms
				filename = "%s.txt" % y
				f = open(filename , 'r')
				doc_relevant=[]
				s=f.readline()
				while (s):
    					doc_relevant=s.split(',')
    					s=f.readline()
				print doc_relevant
				print relevant_terms[indexes]
			
				if doc_relevant in relevant_terms[indexes]:
					num+=1
				#print den,num
				probability=float(num)/den
				#print probability
				
 				temp=[] #Temporary list to hold the document to be changed
				
				#Replace the document if prob < u 
				if probability < random_number :
					#bees[i].remove(y)
					#Replace This x with a new document from that cluster
					indexes=bees.index(x)
					#To check from document and the bee list for matching documents and selecting the right					
					while (1):
						my_elem = random.choice(clusters[indexes])		
						if my_elem not in x:
							temp.append(my_elem)
							break
				#Else just append the document to the temp list
				else:
					temp.append(y)
			#Remove the old bee solution
			#Add the new bee solution 		
			bees.remove(x)
			bees.append(temp)
			print bees
		
		#Merging of Dance Table
		BeeInit=bees
	number_of_iterations+=1

	print "Final Sloution is ",BeeInit

				
				
		
			
		



#Input clusters and frequent patterns from the respective text files and user input is from terminal
clusters = [[1,2,6],[3,4,5],[6,7,8]]
freq_patterns =[[['hello','hi'],['hi']],[['i','am'],['busy']],['hi']]
query=raw_input("What is the User Query: ")

BSO(clusters,freq_patterns,query)

