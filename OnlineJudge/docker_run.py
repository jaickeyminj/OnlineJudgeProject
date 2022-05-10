import os,subprocess

subprocess.run('docker build -t python:0.1 .', shell=True) 
file = open('data.txt','r').read()
output = subprocess.run('docker run -i python:0.1 > output1.txt', shell=True, capture_output=True,input=file.encode())
# output = subprocess.run('docker run -it -v /tmp/python/:/python/data python:0.1 data.txt data/output2.txt', shell=True, capture_output=True)
print(output.stderr.decode('UTF-8'))
print(output.stdout.decode(('UTF-8')))
print(output)
with open('output1.txt', 'r') as file:
    content = file.read()
    print(content)