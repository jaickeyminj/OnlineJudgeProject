import os,subprocess

subprocess.run('docker build -t python:0.1 C:/Users/jaick/Documents/OnlineJudgeProject/OnlineJudgeProject/OnlineJudge', shell=True)
output = subprocess.run('docker run python:0.1 > output1.txt', shell=True, capture_output=True)
print(output.stderr)
print(output.stdout)
with open('output1.txt', 'r') as file:
    content = file.read()
    print(content)