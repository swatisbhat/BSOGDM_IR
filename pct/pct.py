class Node(object):

    def __init__(self, data=None, count=0):
        self.child = None
        self.sibling = None
        self.data = data
        self.count = count
#transactions = [[1, 5, 6, 8], [2, 4, 8], [4, 5, 7], [2, 3], [5, 6, 7], [2, 3, 4], [
#    2, 6, 7, 9], [5], [8], [3, 5, 7], [3, 5, 7], [5, 6, 8], [2, 4, 6, 7], [1, 3, 5, 7], [2, 3, 9]]

import json
load_transactions = open('../apriori/itemsets','r')
transactions = json.load(load_transactions)
#print transactions_2[0:2]
# pct construction
r2=len(transactions)
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
            print 'data {} count {}'.format(root.child.data, root.child.count) 
            root = root.child
        else:
            root = root.child
            flag = 0
            while(root.sibling is not None):
                if root.sibling.data != transactions[i][j]:
                    root = root.sibling
                else:
                    root.sibling.count += 1
                    print 'data {} count {}'.format(root.sibling.data,
                            root.sibling.count) 
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
            print 'root.child at the beginning of the while loop {}'.format(root.child.data)
            print 'count(root child data) {} min sup {}'.format(count[root.child.data],min_sup) 
            if count[root.child.data] < min_sup:
                # delete
                temp = root.child
                root.child = temp.child
                print 'Hey1'
                if temp.child is None:
                    root.child = temp.sibling
                    print '{} temp.sibling {} root.child'.format(temp.sibling.data,root.child.data)
                elif temp.sibling is not None:
                    print 'Hey2'
                    last_sibling = temp.child
                    while last_sibling.sibling is not None:
                        last_sibling = last_sibling.sibling
                    last_sibling.sibling = temp.sibling
                    # free memory
                print 'Hey3'
                del(temp)
            else:
                print 'hey_else'
                nodes.append(root.child)
                root = root.child
            print 'hey4'
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

print [ i for i in range(len(count)) if count[i]>=2] 

def cfpm(min_sup):
    # reverse array of frequent 1-itemsets
    freq_one_itemsets = [i for i in xrange(len(count)) if count[i]>=min_sup]
    freq_one_itemsets.sort()
    freq_one_itemsets.reverse()
    print freq_one_itemsets
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
        print 'deleted head'
        traverse()

        paths = []
        root = main_root.child
        while root is not None:
            print 'root child {}'.format(root.data), root.child is None
            if root.child is None:
                root = root.sibling
                #print 'continue loop head {}'.format(root.data) , root.sibling is None
                continue
            #print  root.child.sibling is None
            if root.child.sibling is None:
                print 'child data = {}'.format(root.child.data)
                print 'i {}'.format(i)
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

        
        print paths

        #if i == freq_one_itemsets[0]:
            #break
        
        # get paths ending with I
        # example - paths = [[count , e1, e2, e3, ...]]
        # paths = [[1,2,4,6,7],[1,2,6,7], [1,4,5,7], [1,5,6,7],[3,3,5,7]]
        
        #paths = getpath(I)
        # paths = [[1,4088,9278],[1,6151,9278]]
        # list containing all other elements
        l1 = [i for i in f if i<=I]
        minsupport_dict={}
        for i in l1:
            minsupport_dict[i]=0
        for i in range(0,len(paths)):
            for j in range(1,len(paths[i])):
                minsupport_dict[paths[i][j]] += paths[i][0]
        T = []
        for key,value in minsupport_dict.iteritems():
            if key!=I:
                if value >= minsup:
                    T.append(key)

        # removing elements from paths that are not in T
        # reduced paths
        reduced_paths=[]
        for i in range(0,len(paths)):
            reduced_paths.append([])

        for i in range(0,len(paths)):
            reduced_paths[i].append(paths[i][0])
            for j in range(1,len(paths[i])):
                if (paths[i][j] in T or paths[i][j]==I):
                    reduced_paths[i].append(paths[i][j])

        print "Reduced paths = {}".format(reduced_paths)


        closed_freq=[]
        # determining closed frequent itemsets from reduced paths
        '''for i in range(0,len(paths)-1):
            for j in range(i+1,len(paths)):
                # add case where path array already considered for
                # previous i
                if len(paths[i])>=len(paths[j]):
                    if set(paths[j])<=set(paths[i]):
                        paths[i][0]+=paths[j][0]
                elif len(paths[i])<len(paths[j]):
                    if set(paths[i])<=set(paths[j]):
                        paths[i][0]+=paths[j][0]
        print "paths: ={}".format(paths)        
        '''
        i,j= 0,0
        while i < len(reduced_paths):
            j = i+1
            while j < len(reduced_paths):
                if(reduced_paths[i][1:] == reduced_paths[j][1:]):
                    reduced_paths[i][0] += reduced_paths[j][0]
                    del reduced_paths[j]
                    j -= 1
                elif set(reduced_paths[i]).issubset(reduced_paths[j]):
                    reduced_paths[i][0] += reduced_paths[j][0]
                j += 1
            i += 1
        print reduced_paths
        ''''
        rp=[]
        l=[]
        # to merge counts of same reduced_paths
        for i in range(0,len(reduced_paths)-1):
            a = reduced_paths[i]
            count = a[0]
            #del a[0]
            for j in range(i+1,len(reduced_paths)):
                b = reduced_paths[j]
                #del b[0]
                if set(a)==set(b):
                    count += reduced_paths[j][0]
            
            # reduced paths containing distinct lists with count
            rp.append([])
            rp.append(count)
            for j in range(1,len(reduced_paths[i])):
                rp.append(reduced_paths[i][j])
            print rp
        '''

        # paths starting with elements in T and ending with I
        start = T
        end = I

        for i in reduced_paths:
            start_el = i[1]
            end_el = i[-1]
            if start_el not in T or end_el != I:
                del i
        print reduced_paths

        


'''       
# pct traversal for getting paths ending with i
    #def traverse():
        nodes = []
        paths = []
        root = main_root.child
        nodes.append(root)
        i = 0
        break_flag = 0
        temp_paths = []
        while len(nodes)!=0:
            
            while root.child is not None:
                root = root.child
                nodes.append(root)
                
            x = nodes.pop()
            temp_paths.append([x.count, []])
            
            while x.sibling is None:
                #print '({}, {})'.format(x.data, x.count)
                for j in range(len(temp_paths)):
                    if j == i:
                        temp_paths[i][1].append(x.data)
                    else:
                        if temp_paths[j][1][-1] > x.data:
                            temp_paths[j][1].append(x.data)
                if len(nodes) == 0:
                    break_flag = 1
                    break
                x = nodes.pop()

            if break_flag == 1:
                break
            # print '({}, {})'.format(x.data, x.count)
            # temp_paths[i][1].append(x.data)
            for j in range(len(temp_paths)):
                if j == i:
                    temp_paths[i][1].append(x.data)
                else:
                    if temp_paths[j][1][-1] > x.data:
                        temp_paths[j][1].append(x.data)
            i+=1
            root = x.sibling
            nodes.append(root)
            # 
'''
        

cfpm(2)
#traverse()


            
