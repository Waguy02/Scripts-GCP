#Script to launch generation sign and verification on gcp
## The start index is give by  the second computer
###


import subprocess,sys
import multiprocessing
import multiprocessing as mp
import threading
NB_CPUS=mp.cpu_count()
TASK_PER_CPU=8 ##TASK PER CPU



##Start is used to parallelized processing
START=0
if len (sys.argv)>1:
    START = int(sys.argv[1])




def task(t0,n,message_size,id):

    def f(t):
        subprocess.call(["python3", "gen_sign_verif_gcp.py", str(t), str(n), str(message_size), str(id + 1)])

    subtasks=[]
    for t in range(t0,t0+TASK_PER_CPU):
        if t>n:
            break
        st=threading.Thread(target=f,args=[t])
        subtasks.append(st)
    
    for st in subtasks:
        st.start()
        subprocess.call(["python3", "gen_sign_verif_gcp.py", str(t), str(n), str(message_size), str(id + 1)])
        
    
MESSAGE_SIZES=[64,128]
N_VALUES=[20,30,40,]
THRESHOLD_VALUES=[0.5,0.7,0.8,0.9]


for message_size in MESSAGE_SIZES:
    for n in N_VALUES:
        t_values= list(set( map(lambda ts:int(n*ts)+1,THRESHOLD_VALUES )) )## Unique corresponding t_values
        for t in t_values :
            if t >n:
                break
            tasks=[]
            if(START>=n):
                continue
            for id in range(START,min(START+NB_CPUS,n),TASK_PER_CPU):
                tasks.append(multiprocessing.Process(target=task,args=[t,n,message_size,id]))
            for t in tasks:
                t.start()
            for t in tasks:
                t.join()









