class Node(object):

    def __init__(self, data=None, count=0):
        self.child = None
        self.sibling = None
        self.data = data
        self.count = count
transactions = [[1, 5, 6, 8], [2, 4, 8], [4, 5, 7], [2, 3], [5, 6, 7], [2, 3, 4], [
   2, 6, 7, 9], [5], [8], [3, 5, 7], [3, 5, 7], [5, 6, 8], [2, 4, 6, 7], [1, 3, 5, 7], [2, 3, 9]]

# import json
# load_transactions = open('../apriori/itemsets','r')
# transactions = json.load(load_transactions)
#print transactions_2[0:2]
# pct construction
r2=len(transactions)

# get number of distinct items and max item val
items = []
max_val = 0
distinct_items = 0
for i in transactions:
    for j in i:
        if j not in items:
            distinct_items += 1
            items.append(j)
        if j > max_val:
            max_val = j

#distinct_items = len(list(set(transactions_2)))
r=10
count = [0 for i in range(max_val+1) ]
print len(count)
root = Node()


print 'Transactions'
for i in transactions:
    print i
print 'PC-Tree Construction'

main_root = root

def construct():
	
	for i in range(0, len(transactions)):
	    for j in range(0, len(transactions[i])):
	        #print transactions[i][j]
	        #print len(count)
	        count[transactions[i][j]] += 1
	        if root.child == None:
	            root.child = Node(transactions[i][j], count=1)
	            root = root.child
	        elif root.child.data == transactions[i][j]:
	            root.child.count += 1
	            #print 'data {} count {}'.format(root.child.data, root.child.count) 
	            root = root.child
	        else:
	            root = root.child
	            flag = 0
	            while(root.sibling is not None):
	                if root.sibling.data != transactions[i][j]:
	                    root = root.sibling
	                else:
	                    root.sibling.count += 1
	                    #print 'data {} count {}'.format(root.sibling.data,root.sibling.count) 
	                    root = root.sibling
	                    flag = 1
	                    break
	            if flag == 0:
	                root.sibling = Node(transactions[i][j], count=1)
	                root = root.sibling
	    root = main_root


# pct traversal
def traverse():
    nodes = []
    root = main_root.child
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


traverse()

# deleting infrequent items
def delete_infrequent_nodes(min_sup):
    print 'Min Support {}'.format(min_sup)    
    nodes = []
    root = main_root

    parent = main_root
    #flag_switch = 0
    while True:
        #if flag_switch == 0:
        while root.child is not None:
            #print 'root.child at the beginning of the while loop {}'.format(root.child.data)
            #print 'count(root child data) {} min sup {}'.format(count[root.child.data],min_sup) 
            if count[root.child.data] < min_sup:
                # delete
                temp = root.child
                root.child = temp.child

                if temp.child is None:
                    root.child = temp.sibling
                    #print '{} temp.sibling {} root.child'.format(temp.sibling.data,root.child.data)
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
                #print '({}, {})'.format(x.data, x.count)
                
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

                del(temp)

            #print '({}, {})'.format(x.data, x.count)
            else:
                flag = 1
                root = root.sibling
            
        nodes.append(root)
    return True
status = False
status = delete_infrequent_nodes(2)
print 'Deleted infrequent nodes: {}'.format(status)
traverse()
#print count


# merging repeating heads
def merge_repeating_heads():
    root = main_root.child
    head = root.sibling
    head_parent = root
    while root.sibling is not None:
        while head is not None:
            print 'root {}, head {}'.format(root.data,head.data)
            if head.data != root.data:
                head = head.sibling
                head_parent = head_parent.sibling
                continue
            else:
                # merge
                root_ptr = root
                head_ptr = head
                #while head_ptr is not None or root_ptr is not None:
                while head_ptr.data == root_ptr.data :
                    if head_ptr.child is not None and root_ptr.child is not None:
                        root_ptr.count = root_ptr.count + head_ptr.count
                        if head_ptr.sibling is not None and head_ptr.sibling != head.sibling:
                            last_sibling = root_ptr.sibling
                            while last_sibling.sibling is not None:
                                last_sibling = last_sibling.sibling
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
        root = root.sibling
        head = root.sibling
        head_parent = root
    return True

# merging repeating heads
def merge_repeating_siblings():
    root = main_root.child
    head = root.sibling
    head_parent = root
    sibling_check = []
    sibling_check.append(root)
    while len(sibling_check) != 0:

        while root.sibling is not None:
            while head is not None:
                #print 'root {}, head {}'.format(root.data,head.data)
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
                                while last_sibling.sibling is not None:
                                    last_sibling = last_sibling.sibling
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


#status_2 = False
#status_2 = merge_repeating_heads()
#print 'Merged repeating heads : {}'.format(status_2)
#traverse()

#status_3 = False
#status_3 = merge_repeating_siblings()
#print 'Merged repeating heads and siblings : {}'.format(status_3)
#traverse()

#print [ i for i in range(len(count)) if count[i]>=2] 

def cfpm(min_sup):
    # reverse array of frequent 1-itemsets
    freq_one_itemsets = [i for i in xrange(len(count)) if count[i]>=min_sup]
    freq_one_itemsets.sort()
    freq_one_itemsets.reverse()
    print 'frequent one itemsets = {}'.format(freq_one_itemsets)
    for i in freq_one_itemsets:
        
        # delete head with data equal to the considered itemset
        head = main_root.child
        deleted_head = 0
        if head.data == i:
            main_root.child = head.sibling
            deleted_head = 1
            # print 'if1'
            del(head)
        if deleted_head == 0:
            # print 'if2'
            head_parent = head
            head = head.sibling
            
            while head is not None and head.data != i:
                head = head.sibling
                head_parent = head_parent.sibling

            if head is not None and head.data == i:
                # print 'if3'
                # print i
                # traverse()
                # print 't1 end'

                head_parent.sibling = head.sibling
                del(head)
                # traverse()
                # print 't2 end'
        # test 1 - working 
        #if i == 8:
        #    break
        #print 'deleted head'
        #traverse()

        paths = []
        root = main_root.child
        while root is not None:
            # print 'root child {}'.format(root.data), root.child is None
            if root.child is None:
                root = root.sibling
                #print 'continue loop head {}'.format(root.data) , root.sibling is None
                continue
            #print  root.child.sibling is None
            if root.child.sibling is None:
                #print 'child data = {}'.format(root.child.data)
                #print 'i {}'.format(i)
                if root.child.data == i:
                    paths.append([root.child.count, root.data, root.child.data])
            else:
                child = root.child
                while child.sibling is not None:
                    if child.data == i:
                        paths.append([child.count, root.data, child.data])
                    child = child.sibling
            root = root.sibling        
            #print 'end of while loop root child {}'.format(root.data), root.child is None
            #print 'head {}'.format(root.data) , root.sibling is None

        
        #print paths

        #if i == freq_one_itemsets[0]:
            #break
        
        # get paths ending with I
        # example - paths = [[count , e1, e2, e3, ...]]
        # paths = [[1,2,4,6,7],[1,2,6,7], [1,4,5,7], [1,5,6,7],[3,3,5,7]]
        
        #paths = getpath(I)
        # paths = [[1,4088,9278],[1,6151,9278]]
        # list containing all other elements
        l1 = [j for j in freq_one_itemsets if j<=i]
        minsupport_dict={}
        for j in l1:
            minsupport_dict[j]=0
        for j in range(0,len(paths)):
            for k in range(1,len(paths[j])):
                minsupport_dict[paths[j][k]] += paths[j][0]
        T = []
        for key,value in minsupport_dict.iteritems():
            if key!=i:
                if value >= min_sup:
                    T.append(key)

        # removing elements from paths that are not in T
        # reduced paths
        reduced_paths=[]
        for j in range(0,len(paths)):
            reduced_paths.append([])

        for j in range(0,len(paths)):
            reduced_paths[j].append(paths[j][0])
            for k in range(1,len(paths[j])):
                if (paths[j][k] in T or paths[j][k]==i):
                    reduced_paths[j].append(paths[j][k])

        #print "Reduced paths = {}".format(reduced_paths)


        closed_freq=[]
        # determining closed frequent itemsets from reduced paths
       
        j,k = 0,0
        while j < len(reduced_paths):
            k = j+1
            while k < len(reduced_paths):
                if(reduced_paths[j][1:] == reduced_paths[k][1:]):
                    reduced_paths[j][0] += reduced_paths[k][0]
                    del reduced_paths[k]
                    k -= 1
                elif set(reduced_paths[j]).issubset(reduced_paths[k]):
                    reduced_paths[j][0] += reduced_paths[k][0]
                k += 1
            j += 1


        # paths starting with elements in T and ending with I
        start = T
        end = i

        for j in reduced_paths:
            start_el = j[1]
            end_el = j[-1]
            if start_el not in T or end_el != i:
                del j

        cf_itemsets = [j[1:] for j in reduced_paths]
        print 'cfp for i = {} is {}'.format(i, cf_itemsets)

        



        

cfpm(2)
#traverse()


            
