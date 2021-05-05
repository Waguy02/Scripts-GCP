import subprocess,sys
import multiprocessing
NB_CPUS=8




def task(t,n,message_size,id):
    subprocess.call(["python3","gen_sign_verif_gcp.py",str(t),str(n), str(message_size),str(id + 1)])

MESSAGE_SIZES=[64,128]
N_VALUES=[8]
THRESHOLD_VALUES=[0.5,0.7,0.8,0.9]


for message_size in MESSAGE_SIZES:
    for n in N_VALUES:

        t_values= list(set( map(lambda ts:int(n*ts)+1,THRESHOLD_VALUES )) )## Unique corresponding t_values

        for t in t_values :
            if t >n:
                break

            tasks=[]
            for id in range(n):
                tasks.append(multiprocessing.Process(target=task,args=[t,n,message_size,id]))

            for t in tasks:
                t.start()
            for t in tasks:
                t.join()









