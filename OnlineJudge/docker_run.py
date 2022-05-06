import os,subprocess

subprocess.run('docker build -t python:0.1 D:/DataSet', shell=True)
output = subprocess.run('docker run python:0.1 › output.txt', shell=True, capture_output=True)
print(output.stderr)
print(output.stdout)