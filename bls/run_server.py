import os
import subprocess


addr=open("addr.txt",'r').read().strip()
subprocess.run(f'./cli --addr {addr} mediator-server run',shell=True).stdout
