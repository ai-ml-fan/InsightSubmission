import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_inpath = "../paymo_input/batch_payment.txt"
in_file_path = os.path.join(script_dir, rel_inpath)
rel_outpath = "../paymo_output/output2.txt"
out_file_path = os.path.join(script_dir, rel_outpath)
 


def found( k,l):
#def found(mySet, k,l):
    id1=k.strip()
    id2=l.strip()
    fwd = id1+':' +id2
    rev=id2+':'+id1
    if fwd in pay2me or rev in pay2me:
            return 1
    return 0

def search(myDictOfColl, k,l):
    curr = 'str'
    match = 'str'
    klist =[]
    llist=[]
        
    klist = myDictOfColl[k]
    llist = myDictOfColl[l]
    #print("List of values for key1 " + k + "-----" + ','.join(klist))
    
    for key in klist:
        #Extract the substring
        x,y = key.split(':')
        if x == k or y == k:
            curr = x if k == x else y
            match = x if curr == y else y
            if match== l:
                return curr
            #Look if we have an indirect link
            elif found(match,l) ==1:
                return match
            else: 
                continue
        else:
            continue
    return 0                
    #Key not found in k's 
                    





#TODO: Set directory to the location of choice
#Currently using directory from env
pay2me = dict()


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
                text_file.write(" trusted\n")
            else:
                #Check for Friend of Friend
                #Iterate over the hash containing keys key1
                #For each iter check if the other key is available in a combo with key2
                #if yes trusted
                match = search(isTrusted_dict,liveid1,liveid2)
                #if( i < 20 ):
                   # print(str(match) + " and " +liveid1+ " and "+ liveid2)

                #write "unverified"
                text_file.write("unverified\n" if match == 0 else "trusted \n")
            
            #DEBUG ONLY: Print first 20 
            #if( i < 20 ):
               # print(str(isFound) + " and " +liveid1+ " and "+ liveid2)
            i = i+1

