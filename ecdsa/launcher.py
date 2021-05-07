#Script to launch generation sign and verification on gcp
## The start index is give by  the second computer
###


import subprocess,sys,os,csv
import multiprocessing,threading

from os import path



import time
NB_CPUS=multiprocessing.cpu_count()
TASK_PER_CPU=8 ##TASK PER CPU



##Start is used to parallelized processing
START=0
if len (sys.argv)>1:
    START = int(sys.argv[1])

import json,codecs
def write_params(n,t):
    with open('params.json','w') as f :
        f.write(json.dumps({"parties":str(n), "threshold":str(t)}))
        f.close()
def generate_message(message_size):
    return "".join("a" for i in range(message_size))





def generate_keys(n,t):  
    os.system("rm keys/keys?.store")
    os.system("rm signature")
    write_params(n, t)
    beginning=time.process_time()
    def task(id):
        subprocess.call(["./gg18_keygen_client", "http://127.0.0.1:8001", f'keys/keys{id+1}.store'])
                     
    tasks=[]        
    for id in range(n):
        tasks.append(multiprocessing.Process(target=task,args=[id]))
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
    duration=time.process_time()-beginning                             
    return duration    



def sign(message_size,t):
    message=generate_message(message_size)
    beginning=time.process_time()
    def task(id):
            subprocess.call(["./gg18_sign_client", "http://127.0.0.1:8001", f'keys/keys{id+1}.store',message])
    tasks=[]        
    
    for id in range(t+1):
        tasks.append(threading.Thread(target=task,args=[id]))
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
        
    duration=time.process_time()-beginning

    signature=open("signature","r");
    sign_size=sum(map(lambda elt:len(elt),signature.read().split(" ")))
    signature.close()

    return sign_size,duration


##Print result in output csv
def report(row):
    print("Reporting",row)
    ## Report results
    exists=False
    if path.exists("output_dataset.csv"):
        exists=True
    
    
    ##The output dataset for generating curves
    csv_file=open("output_dataset.csv","a")
    writer=csv.writer(csv_file)
    "Check if we need to add the header or not"

    if not exists:
    	csv_header=["t","n","keygen duration","message_size","signature_size","sign_verify"]
    	writer.writerows([csv_header])
    writer.writerows([row])
    csv_file.close()





MESSAGE_SIZES=[64,128]
N_VALUES=[10,20]
THRESHOLD_VALUES=[0.3,0.4,0.5,0.7,0.8,0.9]

def main():
    #LAUCHING SERVER
    print("Launching server")
    threading.Thread(target=lambda: os.system("./sm_manager ")).start()
    for message_size in MESSAGE_SIZES:
        for n in N_VALUES:
            t_values= list(set( map(lambda ts:int(n*ts)+1,THRESHOLD_VALUES )) )## Unique corresponding t_values
            for t in t_values : 
                ##KEY GENERATION;
                keytime=generate_keys(n, t)
                ###SIGNATURE;
                ssize,stime=sign(message_size,t)
                
                 ###REPORT
                report([t,n,keytime,message_size,ssize,stime])
                
    
                 
                 
    
main()





