import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_inpath = "../paymo_input/batch_payment.txt"
in_file_path = os.path.join(script_dir, rel_inpath)
rel_outpath = "../paymo_output/output1.txt"
out_file_path = os.path.join(script_dir, rel_outpath)

#TODO: Set directory to the location of choice
#Currently using directory from env
pay2me = dict()
i=0
#with open('batch_payment-2.txt') as fin:
with open(in_file_path) as fin:
    for line in fin:
        if i == 0:
            i=i+1
            continue
        
        d=line.split(',')
        id1=d[1].strip()
        id2=d[2].strip()
        inkey = id1+'::' +id2
        revkey=id2+'::'+id1
        #create hash key and set to 1
        if inkey in pay2me or revkey in pay2me:
            pass
        else:    
            pay2me[inkey]= 1
            
        #DEBUG ONLY: Print first 20             
        #if i < 20 :
            #print(pay2me)
        i=i+1
        
        
#Now start to read the other file
istrusted = dict()
i=0
rel_inpath = "../paymo_input/stream_payment.txt"
in_file_path = os.path.join(script_dir, rel_inpath)
#with open("../paymo_output/Output1.txt", "w") as text_file:
with open(out_file_path, "w") as text_file:
    #with open('stream_payment-2.txt') as strm:
    with open(in_file_path) as strm:
        for each in strm:
            #skip header
            if i == 0:
                i=i+1
                continue
            fr=each.split(',')
            liveid1=fr[1].strip()
            liveid2=fr[2].strip()
            liveinkey = liveid1+'::' +liveid2
            liverevkey=liveid2+'::'+liveid1
        
            if liveinkey in pay2me or liverevkey in pay2me:
                #write "trusted"
                text_file.write("trusted\n")
            else:
                #write "unverified"
                text_file.write("unverified\n")
            #DEBUG ONLY: Print first 20 
            #if( i < 20 ):
             #   print(liveinkey+ " and "+ liverevkey)
            i = i+1

