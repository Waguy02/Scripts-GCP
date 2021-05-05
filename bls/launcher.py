import subprocess,sys
import threading
NB_CPUS=8




def task(t,n,message_size,id):
    subprocess.call(["python3","gen_sign_verif_gcp.py",str(t + 1),str(n), str(message_size),str(id + 1)])

MESSAGE_SIZES=[64,128]
N_VALUES=[10,20]
THRESHOLD_VALUES=[0.6,0.7,0.8,0.9]
for message_size in MESSAGE_SIZES:
    for n in N_VALUES:
        for threshold in THRESHOLD_VALUES:
            t=int(n*threshold)
            tasks=[]
            for id in range(n):
                tasks.append(threading.Thread(target=task,args=[t,n,message_size,id]))

            for t in tasks:
                t.start()
            for t in tasks:
                t.join()









