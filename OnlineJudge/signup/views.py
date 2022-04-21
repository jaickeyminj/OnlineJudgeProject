from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Problem
import sys
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
    problem = Problem.objects.all()
    return render(request,'DisplayProblem.html',{'problem':problem})

def displayproblemdetail(request,problem_id):
    problem = Problem.objects.filter(problem_id=problem_id).first()
    return render(request,'displayProblemDetail.html',{'problem':problem})

def runcode(request,problem_id):
    if request.method == 'POST':
        code_part = request.POST['code_area']
        input_part = request.POST['input_area']
        problem = Problem.objects.filter(problem_id=problem_id).first()
        y = input_part
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
            sys.stdout=orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = e
        print(output)
    res = render(request,'displayProblemDetail.html',{"code":code_part,"input":y,"output":output,'problem':problem})
    return res