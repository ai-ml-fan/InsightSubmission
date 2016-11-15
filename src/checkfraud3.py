import os
import sys
sys.setrecursionlimit(5000)
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_inpath = "../paymo_input/batch_payment.txt"
in_file_path = os.path.join(script_dir, rel_inpath)
rel_outpath = "../paymo_output/output3.txt"
out_file_path = os.path.join(script_dir, rel_outpath)
 



def found( k,l):
    id1=k.strip()
    id2=l.strip()
    fwd = id1+':' +id2
    rev=id2+':'+id1
    if fwd in pay2me or rev in pay2me:
            return 1
    return 0

def search(myDictOfColl, k,l,proximity=4,isRoot=False):
    curr = 'str'
    match = 'str'
    klist =[]
    llist=[]
    global completed
    if isRoot:
        completed= []
    
    if proximity <= 0:
        return 0
        
    if not k in myDictOfColl:
        return 0;    
    klist = myDictOfColl[k]
    
    
    for key in klist:
        #Check if the key is k:l(first degree relation)
        if key in completed:
            continue
        x,y = key.split(':')
        curr = x if k == x else y
        match = x if curr == y else y
        if match== l:
            return curr
        #Look if we have an indirect link
        elif proximity >= 1: 
            if found(match,l) ==1:
                return match
        llist.append(match)        
        completed.append(key)
        continue
    
    #print "Completed for proximity ", proximity, " LEN of links: " ,len(llist) , " Len of completed: " , len(completed)
    #','.join(completed) + ':::'+ key + "-----" + ','.join(llist))
    
    proximity = proximity -1
    if proximity <= 0:
        return 0;
    for link in llist:
        match = search(isTrusted_dict,link,l,proximity,False)
        if match != 0: 
            return match
    return 0                
    #Key not found in k's 
                    

#TODO: Set directory to the location of choice
#Currently using directory from env
pay2me = dict()
completed =[]

i=0
from collections import defaultdict
isTrusted_dict = defaultdict(list)


with open(in_file_path) as fin:
    for line in fin:
        if i == 0:
            i=i+1
            continue
        
        d=line.split(',')
        id1=d[1].strip()
        id2=d[2].strip()
        inkey = id1+':' +id2
        revkey=id2+':'+id1
        #Now changed to set as no value from dict(create  hash key and set to 1)
        if inkey in pay2me or revkey in pay2me:
        #if revkey in pay2Set:
            pass
        else:    
            pay2me[inkey]= 1
            isTrusted_dict[id1].append(inkey)
            isTrusted_dict[id2].append(inkey)
            
            #pay2Set.add(inkey)
            
        #DEBUG ONLY: Print first 20             
        #if i < 20 :
            #print(pay2me)
        i=i+1
        
        
#Now start to read the other file
#NEXT CHANGE: TO DEFINE AN_INMEMORY WRITE THAT CAN BE WRITTEN TO FILE AT THE END MORE EFFICIENTLY
i=0
match=0
rel_inpath = "../paymo_input/stream_payment.txt"
in_file_path = os.path.join(script_dir, rel_inpath)
with open(out_file_path, "w") as text_file:
    with open(in_file_path) as strm:
        #print sum(1 for _ in strm)
        for each in strm:
            #skip header
            if i == 0:
                i=i+1
                continue
            fr=each.split(',')
            liveid1=fr[1].strip()
            liveid2=fr[2].strip()
            liveinkey = liveid1+':' +liveid2
            liverevkey=liveid2+':'+liveid1
                    
            #if liveinkey in pay2me or liverevkey in pay2me:
            isFound = found(liveid1,liveid2)
            if isFound==1:
                #write "trusted"
                text_file.write("trusted\n")
            else:
                #Check for Friend of Friend
                #Iterate over the hash containing keys key1
                #For each iter check if the other key is available in a combo with key2
                #if yes trusted
                match = search(isTrusted_dict,liveid1,liveid2,4,True)
                #if( i < 20 ):
                   # print(str(match) + " and " +liveid1+ " and "+ liveid2)

                #write "unverified"
                text_file.write("unverified\n" if match == 0 else "trusted\n")
            
            #DEBUG ONLY: Print first 20 
            #if( i < 20 ):
               # print(str(isFound) + " and " +liveid1+ " and "+ liveid2)
            i = i+1

