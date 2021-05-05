import os,sys
import threading
import random 
import string
import time
import csv
from os import path
import subprocess



##PARSING ARGS
assert(len(sys.argv)>=5)
t=int(sys.argv[1])
n=int(sys.argv[2])
message_size=int(sys.argv[3])
id=int(sys.argv[4])


## READING ADDRES
addr=open("addr.txt",'r').read().strip()




##PREPARING OUTPUT

if not path.exists("target/keys"):
    os.makedirs("target/keys")

if not path.exists("target/signatures"):
    os.makedirs("target/signatures")


row_output=[t,n,message_size]
letters = string.ascii_lowercase
message = "".join("a" for i in range(message_size))



def generate_key(t,n):
    if id==1:
        subprocess.run(f'./cli --addr {addr} keygen -t {t} -n {n} --output target/keys/key{t}_{n}_{id}|tail -n1 > target/keys/public_key{t}_{n}',shell=True).stdout
    else:
        subprocess.run(f'./cli --addr {addr} keygen -t {t} -n {n} --output target/keys/key{t}_{n}_{id}',shell=True).stdout





def sign(t,n,message):
    # if id>t+1:
    #     return
    begining=time.process_time()
    #print(f"./cli --addr {addr} sign -n {t}  --key target/keys/key{t}_{n}_{id} --digits {message}|tail -n1  > target/signatures/signature{t}_{n}_{id}.txt")
    if id ==1 :
        subprocess.run(f"./cli --addr {addr} sign -n {n}  --key target/keys/key{t}_{n}_{id} --digits {message}|tail -n1  > target/signatures/signature{t}_{n}.txt",shell=True).stdout
    else :
        subprocess.run(f"./cli --addr {addr} sign -n {n}  --key target/keys/key{t}_{n}_{id} --digits {message}",shell=True)
        return


    duration=time.process_time()-begining
    f=open(f'target/signatures/signature{t}_{n}.txt',"r")
    signature=f.read().split("Signature:")[1].strip()
    sign_len=len(signature)
    row_output.append(sign_len)
    row_output.append(duration)
    f.close()
    f=open(f'target/signatures/signature{t}_{n}.txt',"w")
    f.write(f"\nMessage size: {len(message)}; t:{t}; n:{n}")
    f.write(f"\nSignature size: {sign_len}")
    f.write(f"\nSignature duration: {duration}")
    f.close()
    return signature



def verify(t,n,message,signature):
    if id != 1:
        return
    f=open(f"target/keys/public_key{t}_{n}","r")
    pk_raw=f.read()
    f.close()
    pk=pk_raw.split("Public key:")[1].strip()
    print("Public key ",pk)
    begining=time.process_time()
    subprocess.run(f'./cli --addr {addr} verify --digits {message} --signature {signature} --public-key {pk}',shell=True)
    duration=time.process_time()-begining

    f=open(f'target/signatures/signature{t}_{n}.txt',"a")
    f.write(f"\nVerification duration: {duration}")
    f.close()
    row_output.append(duration)



def report():
    if id!=1:
        return
    ## Report result
    exists=False
    if path.exists("target/signatures/output_dataset.csv"):
        exists=True
    
    ##The output dataset for generating curves
    csv_file=open(f"target/signatures/output_dataset.csv","a")
    writer=csv.writer(csv_file)
    "Check if we need to add the header or not"

    if not exists:
    	csv_header=["t","n","message_size","signature_size","signature_duration","verification_duration"]
    	writer.writerows([csv_header])
    writer.writerows([row_output])
    csv_file.close()

generate_key(t, n)

signature=sign(t,n,message) #Production de la signature

verify(t,n,message,signature) #Vérification de la signature

report()
