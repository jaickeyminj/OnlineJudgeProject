import subprocess
import os
from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Problem, Language, TestCase
import sys
import filecmp
from subprocess import Popen,PIPE
from django.views.generic import TemplateView
# from .models import Post
# fn=''
# ln=''
# s=''
# email=''
# pwd=''
# un=''
# Create your views here.
def signaction(request):
    # global fn,ln,s,email,pwd,un
    if request.method=="POST":
        #open connection to db
        m=sql.connect(host="localhost",user="root",password="root",database='onlinejudge')
        cursor=m.cursor()
        data=request.POST
        username = request.POST['user_name']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        sex = request.POST['sex']
        #fetch the values
        # for key,value in data.items():
        #     if key=="first_name":
        #         fn=value
        #     if key=="last_name":
        #         ln=value
        #     if key=="sex":
        #         s=value
        #     if key=="email":
        #         email=value
        #     if key=="password":
        #         pwd=value
        #     if key=="user_name":
        #         un=value
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return render(request,'signup_page.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return render(request,'signup_page.html')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return render(request,'signup_page.html')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return render(request,'signup_page.html')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        
        #store data in db online judge
        c="insert into users values('{}','{}','{}','{}','{}','{}')".format(fname,lname,sex,email,pass1,username)
        cursor.execute(c)
        m.commit()
    
    return render(request,'signup_page.html')

def loginaction(request):
    # global email,pwd
    if request.method=="POST":
        #open connection to db
        m=sql.connect(host="localhost",user="root",password="root",database='onlinejudge')
        cursor=m.cursor()
        data=request.POST
        #fetch the values
        # for key,value in data.items():
        #     if key=="email":
        #         email=value
        #     if key=="password":
        #         pwd=value
        username = request.POST['username']
        pass1 = request.POST['password']
        
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "welcome.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return render(request,'login_page.html')
        #store data in db online judge
        # c="select * from users where email='{}' and password='{}'".format(username,pass1)
        # cursor.execute(c)
        # t=tuple(cursor.fetchall())
        # if t==():
        #     return render(request,'error.html')
        # else:
        #     return render(request,'welcome.html')
    return render(request,'login_page.html')

def displayproblem(request):
    print("displayprpbelm")
    problem = Problem.objects.all()
    return render(request,'DisplayProblem.html',{'problem':problem})

def displayproblemdetail(request,problem_id):
    # print("detail")
    # print(problem_id+"fsfs")
    problem = Problem.objects.filter(problem_id=problem_id).first()
    language = Language.objects.all()
    testcase = TestCase.objects.filter(problem_id=problem_id).first()
    
    if request.method == 'POST':
        language1 = request.POST['language']
        code_part = request.POST['code_area']
        input_part = request.POST['input_area']
        
        if 'run' in request.POST:
            y = input_part
            output = ''
            if(language1 == "Python"):
                # file = open('data.txt','w')
                # file.write(input_part)
                # file.close()
                print('aaaaaaa1')
                input_part = input_part.replace("\n"," ").split(" ")
                # print(input_part)
                file = open('data.txt','w')
                for i in input_part:
                    # print(i)
                    # i+='\n'
                    file.write(str(i))
                # # file = open('data2.txt','w')
                # # file.write(str(input_part))
                print('aaaaaaa2')
                file.close()
                # print(str(input_part))
                # input_part = input_part.replace("\n"," ").split(" ")
                def input(self):
                    a = input_part[0]
                    del input_part[0]
                    return a
                try:
                    file = open('HelloWorld.py','w')
                    # print(code_part)
                    file.write(code_part)
                    file.close()
                    print('aaaaaaa3')
                    orig_stdout = sys.stdout
                    sys.stdout = open('file.txt', 'w')
                    # exec(code_part)
                    
                    subprocess.run('docker build -t python:0.1 .', shell=True) 
                    # output = subprocess.run('docker run -t -i python:0.1 > output1.txt', shell=True, capture_output=True)
                    
                    file = open('data.txt','r').read()
                    file1 = file
                    file.close()
                    output = subprocess.run('docker run -i python:0.1 > output1.txt', shell=True, capture_output=True,input=file1.encode())
                    # file.close()
                    # output1.close()
                    sys.stdout.close()
                    sys.stdout=orig_stdout
                    # output = open('file.txt', 'r').read()
                    output = open('output1.txt', 'r').read()
                    # output.close()
                except Exception as e:
                    sys.stdout.close()
                    sys.stdout=orig_stdout
                    output = e
                    print(e)
            if(language1 == "Java"):
                print(language1)
                input_part = request.POST['input_area']
                y = input_part
                try:
                    file = open('HelloWorld.java','w')
                    print(code_part)
                    file.write(code_part)
                    file.close()
                    s = subprocess.run('javac -sourcepath C:\\Users\\jaick\\Documents\\OnlineJudgeProject\\OnlineJudgeProject\\OnlineJudge -d C:\\Users\\jaick\\Documents\\OnlineJudgeProject\\OnlineJudgeProject\\OnlineJudge HelloWorld.java',shell=True, capture_output=True, text=True)
                    if s.returncode ==0:
                        s = subprocess.run('java -classpath . HelloWorld',shell=True, capture_output=True, text=True,input=input_part)
                    output = s.stdout + '\n' +s.stderr
                except Exception as e:
                    output = e
            res = render(request,'displayProblemDetail.html',{"code":code_part,"input":y,"output":output,'problem':problem,'language':language})
            return res
        if 'submit' in request.POST:
            y = input_part
            output = ''
            if(language1 == "Python"):
                file = open('pythonTestCaseInput.txt','w')
                file.write(testcase.input)
                file.close()
                file = open('HelloWorld.py','w')
                    # print(code_part)
                file.write(code_part)
                file.close()
                input_part = open('pythonTestCaseInput.txt', 'r').read()
                input_part = input_part.replace("\n"," ").split(" ")
                def input(self):
                    a = input_part[0]
                    del input_part[0]
                    return a
                try:
                    orig_stdout = sys.stdout
                    sys.stdout = open('file.txt', 'w')
                    exec(code_part)
                    sys.stdout.close()
                    with open('file.txt', 'r') as file:
                        content = file.read()

                    with open('file.txt', 'w', newline='\n') as file:
                        file.write(content.replace('\n',''))
                    file = open('pythonTestCaseOutput.txt','w')
                    file.write(testcase.output)
                    file.close()
                    sys.stdout=orig_stdout
                    output = open('file.txt', 'r').read()
                    f1 = "file.txt"
                    f2 = "pythonTestCaseOutput.txt"
                    result = filecmp.cmp(f2, f1)
                    print(result)
                    result = filecmp.cmp(f2, f1, shallow=False)
                    print(result)
                    if result == True:
                        output = output + '\n' +'Result : '+ 'Pass'
                    else :
                        output =  'Result : '+ 'Fail \n'
                except Exception as e:
                    sys.stdout.close()
                    sys.stdout=orig_stdout
                    output = e
            if(language1 == "Java"):
                print(language1)
                input_part = request.POST['input_area']
                y = input_part
                file = open('javaTestCaseInput.txt','w')
                file.write(testcase.input)
                file.close()
                input_part = open('javaTestCaseInput.txt', 'r').read()
                try:
                    file = open('HelloWorld.java','w')
                    print(code_part)
                    file.write(code_part)
                    file.close()
                    s = subprocess.run('javac -sourcepath C:\\Users\\jaick\\Documents\\OnlineJudgeProject\\OnlineJudgeProject\\OnlineJudge -d C:\\Users\\jaick\\Documents\\OnlineJudgeProject\\OnlineJudgeProject\\OnlineJudge HelloWorld.java',shell=True, capture_output=True, text=True)
                    if s.returncode ==0:
                        s = subprocess.run('java -classpath . HelloWorld',shell=True, capture_output=True, text=True,input=input_part)
                    file = open('javaTestCaseOutput.txt','w')
                    file.write(testcase.output)
                    file.close()
                    file = open('javaOutput.txt','w')
                    file.write(s.stdout)
                    file.close()
                    with open('javaOutput.txt', 'r') as file:
                        content = file.read()

                    with open('javaOutput.txt', 'w', newline='\n') as file:
                        file.write(content.replace('\n',''))
                    print(s.stderr)
                    print(s.stdout)
                    f1 = "javaOutput.txt"
                    f2 = "javaTestCaseOutput.txt"
                    result = filecmp.cmp(f2, f1)
                    print(result)
                    result = filecmp.cmp(f2, f1, shallow=False)
                    print(result)
                    output = open('javaOutput.txt', 'r').read()
                    if result == True:
                        print('omg')
                        print(output)
                        output = output + '\n' +'Result : '+ 'Pass'
                        print(output)
                    else :
                        output =  'Result : '+ 'Fail \n'
                        output = output + '\n' +s.stderr
                except Exception as e:
                    output = e
            res = render(request,'displayProblemDetail.html',{"code":code_part,"input":y,"output":output,'problem':problem,'language':language})
            return res
    return render(request,'displayProblemDetail.html',{'problem':problem,'language':language})


def same(name1, name2): 
    print("same")    
    with open(name1, "rb") as one: 
        with open(name2, "rb") as two: 
            chunk = other = True 
            while chunk or other: 
                chunk = one.read(1000) 
                other = two.read(1000) 
                print(chunk)
                print(other)
                if chunk != other: 
                    return False 
            return True

class HomePageView(TemplateView):
    template_name = 'home.html' 