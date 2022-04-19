from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import mysql.connector as sql
# email=''
# pwd=''

# Create your views here.
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
