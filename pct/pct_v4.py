import json

class Node(object):

    def __init__(self, data=None, count=0):
        self.child = None
        self.sibling = None
        self.data = data
        self.count = count

# transactions = [[1, 5, 6, 8], [2, 4, 8], [4, 5, 7], [2, 3], [5, 6, 7], [2, 3, 4], [
#    2, 6, 7, 9], [5], [8], [3, 5, 7], [3, 5, 7], [5, 6, 8], [2, 4, 6, 7], [1, 3, 5, 7], [2, 3, 9]]




# pct construction

# import ast
# with open("../transactions") as t:
#     transactions = ast.literal_eval(t.read())

# r2=len(transactions)

# print 'Transactions'
# for i in transactions:
#     print i
# print 'PC-Tree Construction'

# main_root = root

class RPCTree:
	def __init__(self, transactions, min_sup):
		self.transactions = transactions
		# get number of distinct items and max item val
		items = []
		max_val = 0
		distinct_items = 0
		for i in self.transactions:
		    for j in i:
		        if j not in items:
		            distinct_items += 1
		            items.append(j)
		        if j > max_val:
		            max_val = j

		# # max_val = maximum value item ( 9 in the above)
		self.count = [0 for i in range(max_val+1) ]
		# print len(count)
		self.min_sup = min_sup
		self.main_root = Node()



	def construct(self):

	    root = self.main_root
	    transactions = self.transactions
	    count = self.count

	    for i in range(0, len(transactions)):
	        for j in range(0, len(transactions[i])):
	            ## print transactions[i][j]
	            ## print len(count)
	            count[transactions[i][j]] += 1
	            # case 1 : empty sub tree
	            if root.child == None:
	                root.child = Node(transactions[i][j], count=1)
	                root = root.child

	            # case 2 : repeating subtree
	            elif root.child.data == transactions[i][j]:
	                root.child.count += 1
	                ## print 'data {} count {}'.format(root.child.data, root.child.count) 
	                root = root.child

	            # case 3 : non repeating subtree (=>sibling)
	            else:
	                root = root.child
	                flag = 0 # no sibling with the same item val
	                while(root.sibling is not None):
	                    if root.sibling.data != transactions[i][j]:
	                        root = root.sibling
	                    else:
	                        root.sibling.count += 1
	                        ## print 'data {} count {}'.format(root.sibling.data,root.sibling.count) 
	                        root = root.sibling
	                        flag = 1
	                        break
	                if flag == 0:
	                    root.sibling = Node(transactions[i][j], count=1)
	                    root = root.sibling
	        root = self.main_root

# # print "----------------------------------"
# # print main_root.child.data
# # print "----------------------------------"



	# pct traversal
	def traverse(self):
	    nodes = []
	    root = self.main_root.child
	    nodes.append(root)
	    while len(nodes)!=0:
	        while root.child is not None:
	            root = root.child
	            nodes.append(root)
	            
	        x = nodes.pop()
	        while x.sibling is None:
	            print '({}, {})'.format(x.data, x.count)
	            if len(nodes) == 0:
	                return
	            x = nodes.pop()

	        print '({}, {})'.format(x.data, x.count)
	        root = x.sibling
	        nodes.append(root)


# traverse()

	def get_paths(self):
	    nodes = []
	    paths = []
	    root = self.main_root.child
	    nodes.append(root)
	    while len(nodes)!=0:
	        while root.child is not None:
	            root = root.child
	            nodes.append(root)
	            
	        x = nodes.pop()
	        if x.child is None:
	            nodes_data = [x.count] + [ (i.data, i.count) for i in nodes] + [(x.data, x.count)]
	            
	            # print nodes_data
	            paths.append(nodes_data)



	        while x.sibling is None:
	            ## print '({}, {})'.format(x.data, x.count)

	            if len(nodes) == 0:
	                # # print paths
	                return paths
	            x = nodes.pop()

	        ## print '({}, {})'.format(x.data, x.count)

	        root = x.sibling
	        nodes.append(root)
	    # # print 'hey;'
	    # # print paths 
	    # self.paths = paths
	    return paths

# get_paths()


	# deleting infrequent items
	def delete_infrequent_nodes(self):
	    # print 'Min Support {}'.format(min_sup)    
	    nodes = []
	    root = self.main_root
	    min_sup = self.min_sup
	    count = self.count

	    parent = self.main_root
	    #flag_switch = 0
	    while True:
	        #if flag_switch == 0:
	        while root.child is not None:
	            ## print 'root.child at the beginning of the while loop {}'.format(root.child.data)
	            ## print 'count(root child data) {} min sup {}'.format(count[root.child.data],min_sup) 
	            if count[root.child.data] < min_sup:
	                # delete
	                temp = root.child
	                root.child = temp.child

	                if temp.child is None:
	                    root.child = temp.sibling
	                    ## print '{} temp.sibling {} root.child'.format(temp.sibling.data,root.child.data)
	                elif temp.sibling is not None:

	                    last_sibling = temp.child
	                    while last_sibling.sibling is not None:
	                        last_sibling = last_sibling.sibling
	                    last_sibling.sibling = temp.sibling
	                    # free memory

	                del(temp)
	            else:

	                nodes.append(root.child)
	                root = root.child

	        if nodes[-1] != root:
	            nodes.append(root)

	            
	        flag = 0
	        while flag == 0:
	            if len(nodes)==0:
	                
	                nodes.append(root)
	            x = nodes.pop()
	            
	            while x.sibling is None:
	                ## print '({}, {})'.format(x.data, x.count)
	                
	                if len(nodes) == 0:
	                    return True
	                x = nodes.pop()

	            root = x
	            if count[root.sibling.data] < min_sup:
	                temp = root.sibling
	                if temp.child is None and temp.sibling is None:
	                    root.sibling = None
	                elif temp.child is not None:
	                    root.sibling = temp.child
	                    if temp.sibling is not None:
	                        last_sibling = temp.child
	                        while last_sibling.sibling is not None:
	                            last_sibling = last_sibling.sibling
	                        last_sibling.sibling = temp.sibling
	                elif temp.child is None:
	                    root.sibling = temp.sibling
	                #### bug edit
	                # root = root.sibling 
	                nodes.append(root)
	                #### bug edit
	                del(temp)

	            ## print '({}, {})'.format(x.data, x.count)
	            else:
	                flag = 1
	                root = root.sibling
	            
	        nodes.append(root)
	    return True
# status = False
# status = delete_infrequent_nodes(3)
# # print 'Deleted infrequent nodes: {}'.format(status)
# traverse()
## print count

	# merging repeating heads
	def merge_repeating_siblings(self):
	    root = self.main_root.child
	    head = root.sibling
	    head_parent = root
	    sibling_check = []
	    sibling_check.append(root)
	    while len(sibling_check) != 0:

	        while root.sibling is not None:
	            while head is not None:
	                ## print 'root {}, head {}'.format(root.data,head.data)
	                if head.data != root.data:
	                    head = head.sibling
	                    head_parent = head_parent.sibling
	                    continue
	                else:
	                    # merge
	                    if root != sibling_check[-1]:
	                        sibling_check.append(root)
	                    root_ptr = root
	                    head_ptr = head
	                    #while head_ptr is not None or root_ptr is not None:
	                    while head_ptr.data == root_ptr.data :
	                        if head_ptr.child is not None and root_ptr.child is not None:
	                            root_ptr.count = root_ptr.count + head_ptr.count
	                            if head_ptr.sibling is not None and head_ptr.sibling != head.sibling:
	                                last_sibling = root_ptr.sibling
	                                # BUG EDIT - added last_sibling to while
	                                while last_sibling and last_sibling.sibling is not None:
	                                    last_sibling = last_sibling.sibling
	                                # BUG EDIT - added if to check if last_sibling is not None
	                                if last_sibling:
	                                    last_sibling.sibling = head_ptr.sibling
	                            root_ptr = root_ptr.child
	                            head_ptr = head_ptr.child
	                        
	                        if root_ptr.child is None and head_ptr.child is not None:
	                            root_ptr.child = head_ptr.child
	                            if root_ptr.data == head_ptr.data:
	                                root_ptr.count = root_ptr.count + head_ptr.count
	                            break
	                        if head_ptr.child is None:
	                            head_ptr_sibling = head_ptr
	                            if root_ptr.data == head_ptr.data:
	                                root_ptr.count = root_ptr.count + head_ptr.count
	                                head_ptr_sibling = head_ptr.sibling
	                            last_sibling = root_ptr
	                            while last_sibling.sibling is not None:
	                                last_sibling = last_sibling.sibling
	                            last_sibling.sibling = head_ptr_sibling
	                            break

	                    head_parent.sibling = head.sibling
	                    head = head_parent.sibling
	            if root.sibling is None:
	            	break

	            root = root.sibling
	            head = root.sibling
	            head_parent = root
	        if len(sibling_check) == 0:
	            return True
	        #x = sibling_check.pop()
	        #sibling_check.append(x.child)
	        #root = x.child
	        #while root.sibling is not None:
	        #head = root.sibling
	        #head_parent = root

	        x = sibling_check.pop()
	        root = x.child
	        while root is None or root.sibling is None:
	            if root is None:
	                if len(sibling_check) == 0:
	                    return True
	                x = sibling_check.pop()
	                root = x.child
	            else:
	                root = root.child
	                #sibling_check.append(root)
	        sibling_check.append(root)
	        head = root.sibling
	        head_parent = root
	    return True

# status_2 = False
# status_2 = merge_repeating_siblings()
# # print 'Merged repeating heads and siblings : {}'.format(status_2)
# traverse()

## print [ i for i in range(len(count)) if count[i]>=2] 

# traverse()
# print '-------------------------------'
# print 'All paths: '
# get_paths()
# all_paths = get_paths()

	def cfpm(self):
		self.delete_infrequent_nodes()
		self.merge_repeating_siblings()
		min_sup = self.min_sup
		count = self.count
		# reverse array of frequent 1-itemsets
		all_paths = self.get_paths()
		cfi = []
		freq_one_itemsets = [i for i in xrange(len(count)) if count[i]>=min_sup]
		freq_one_itemsets.sort()
		freq_one_itemsets.reverse()
		# print 'frequent one itemsets = {}'.format(freq_one_itemsets)
		for i in freq_one_itemsets:



			# print '######################################'
			# print 'i = {}\n'.format(i)

			# get paths ending with I
			# example - paths = [[count , e1, e2, e3, ...]]
			# paths = [[1,2,4,6,7],[1,2,6,7], [1,4,5,7], [1,5,6,7],[3,3,5,7]]

			# paths = [[1,4088,9278],[1,6151,9278]]
			# list containing all other elements

			# deleting paths starting with i
			# print 'All paths before removing head - ',all_paths,'\n'

			# print 'Removing paths starting with ',i
			j=0
			while j < len(all_paths):
			    if all_paths[j][1][0] == i:
			        
			        all_paths.remove(all_paths[j])
			        j-=1
			    j+=1
			    

			# print 'All paths - ',all_paths,'\n'

			# print 'paths after removing head - ',all_paths

			# getting paths ending with i
			# TODO : simplify below code using list comprehension
			paths_ending_with_i = []
			for path in all_paths:

			    if path[-1][0] == i:
			        ## print 'i = {}'.format(i)
			        ## print 'path = {}'.format(path)
			        # paths_ending_with_i.append(list(path))
			        add_path = [path[0]] + [k[0] for k in path[1:]]
			        if add_path not in paths_ending_with_i:
			        	paths_ending_with_i.append(add_path)

			# print 'Paths ending with {} - {}\n'.format(i,paths_ending_with_i)


			# removing infrequent elements from paths
			count_in_paths = {}
			for j in paths_ending_with_i:
			    for k in j[1:-1]:
			        if k not in count_in_paths:
			            count_in_paths[k] = j[0]
			        else:
			            count_in_paths[k] += j[0]
			T = []
			# TODO : sort the dict - easier
			# else
			for key,val in count_in_paths.iteritems():
			    if val >= min_sup:
			        T.append(key)

			# print 'T: {}\n'.format(T)


			if len(T) != 0:
			    # removing elements from paths that are not in T
			    # # print 'All paths before removal: ',all_paths,'\n'
			    for l in paths_ending_with_i:
			        for m in l[1:-1]:
			            # # print 'm = {} l = {}'.format(m,l)
			            if m not in T:
			                # l.remove(m)
			                paths_ending_with_i[paths_ending_with_i.index(l)].remove(m)
			            # # print 'm = {} l = {}'.format(m,l)
			            # # print 'bug # print ', all_paths,'\n'

			    # print 'Removed elements : {}\n'.format(paths_ending_with_i)
			    # print 'All paths before removal: ',all_paths,'\n'
			    # # print 'Paths after removing head - ',all_paths
			    
			    # merging duplicate reduced paths
			    index = 1

			    while index < len(paths_ending_with_i):
			        curr_path = paths_ending_with_i[index]
			        index2 = index
			        for j in range(index2):
			            if curr_path[1:] == paths_ending_with_i[j][1:]:
			                paths_ending_with_i[j][0]+=curr_path[0]
			                paths_ending_with_i.remove(curr_path)
			                index-=1
			                # # print 'curr path {}, index {}'.format(curr_path, index+1)

			        index +=1 

			    # print 'Merged duplicates\n All paths - ',paths_ending_with_i,'\n'
			    # # print 'All paths before removal: ',all_paths,'\n'

			    # final reduced paths (update count considering subsets)
			    index =1

			    while index < len(paths_ending_with_i):
			        curr_path = paths_ending_with_i[index]
			        
			        for j in range(index):
			            
			            if set(curr_path[1:]).issubset(paths_ending_with_i[j][1:]):
			                paths_ending_with_i[index][0]+=paths_ending_with_i[j][0]
			                # # print 'curr path {}, index {}'.format(curr_path, index)

			        index+=1
			    # print 'Final reduced paths - ', paths_ending_with_i,'\n'

			# deleting items that are already processed to give paths ending with smaller elements
			# # print 'All paths before removal: ',all_paths,'\n'
			j=0
			while j<len(all_paths):
			    if all_paths[j][-1][0] == i:
			        all_paths[j].remove(all_paths[j][-1])
			        all_paths[j][0] = all_paths[j][-1][1]
			        if len(all_paths[j]) == 1:
			            all_paths.remove(all_paths[j])
			    j += 1
			# all_paths = 
			# print 'All paths after removal: ',all_paths,'\n'
			# print '############################################'



			# cfi = []
			for j in paths_ending_with_i:
				if j[0] >= min_sup:
					cfi.append(list(j))

		# print '##############\nPotential Closed Frequent Itemsets: ',cfi,'\n'
		   	

		cfi.sort(key = lambda x: len(x), reverse=True )

		index =1

		while index < len(cfi):
		    curr_cfi = cfi[index]
		    # print (curr_cfi in cfi)
		    for j in range(index):
		        
		        if set(curr_cfi[1:]).issubset(cfi[j][1:]) and curr_cfi[0] == cfi[j][0]:
		        	# print (curr_cfi in cfi)
		            cfi.remove(curr_cfi)
		            index -= 1
		            break
		            # # print 'curr path {}, index {}'.format(curr_path, index)

		    index+=1

		# print '##############\nClosed Frequent Itemsets: ',cfi,'\n'
		print 'Number of documents - ', len(self.transactions)
		print 'Number of closed frequent itemsets - ', len(cfi)

		return cfi

	# def __del__(self):
	# 	pass





if __name__=="__main__":

	all_transactions = json.load(open('../doc_transactions','r'))
	cluster_labels = json.load(open('../cluster_labels','r'))

	# create list of clusters
	doc_clusters = [[] for x in xrange(len(set(cluster_labels)))]
	for i in xrange(len(cluster_labels)):
		doc_clusters[cluster_labels[i]].append(i)

	# create list of cluster itemsets 
	cluster_transactions = [[] for x in xrange(len(set(cluster_labels)))]
	for i in doc_clusters:
		for j in i:
			cluster_transactions[doc_clusters.index(i)].append(list(all_transactions[j]))


	cluster_cfi = []
	min_sup = 3


	x = [[1, 5, 6, 8], [2, 4, 8], [4, 5, 7], [2, 3], [5, 6, 7], [2, 3, 4], [2, 6, 7, 9], [5], [8], [3, 5, 7], [3, 5, 7], [5, 6, 8], [2, 4, 6, 7], [1, 3, 5, 7], [2, 3, 9]]

	for x in cluster_transactions:
		cluster_rpctree = RPCTree(x, min_sup)
		cluster_rpctree.construct()
		# cluster_rpctree.traverse()

		cluster_cfi.append(list(cluster_rpctree.cfpm())) 

	print len(cluster_cfi)


	



            
