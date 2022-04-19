from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib.auth.models import User
from django.contrib import messages
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
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        
        #store data in db online judge
        c="insert into users values('{}','{}','{}','{}','{}','{}')".format(fname,lname,sex,email,pass1,username)
        cursor.execute(c)
        m.commit()
    
    return render(request,'signup_page.html')
