#Script to launch generation sign and verification on gcp
## The start index is give by  the second computer
###


import subprocess,sys
import multiprocessing as mp


MESSAGE_SIZES=[64,128]
N_VALUES=[5,10,20,50,100]
THRESHOLD_VALUES=[0.3,0.6,0.75]

##Start is used to parallelized processing
START=0
if len (sys.argv)>1:
    START = int(sys.argv[1])

def task(t,n,message_size,id):
    assert(t<=n)
    subprocess.call(["python3","gen_sign_verif_gcp.py",str(t),str(n), str(message_size),str(id + 1)])

for message_size in MESSAGE_SIZES:
    for n in N_VALUES:
        t_values= list(set( map(lambda ts:int(n*ts)+1,THRESHOLD_VALUES )) )## Unique corresponding t_values
        for t in t_values:
            if t>=n:
                break
            def f(id):
                task(t,n,message_size,id)

            pool = mp.Pool(n)
            pool.map(f,range(n))
            pool.close()
            pool.join()








