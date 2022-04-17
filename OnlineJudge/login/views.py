from django.shortcuts import render
import mysql.connector as sql
email=''
pwd=''

# Create your views here.
def loginaction(request):
    global email,pwd
    if request.method=="POST":
        #open connection to db
        m=sql.connect(host="localhost",user="root",password="root",database='onlinejudge')
        cursor=m.cursor()
        data=request.POST
        #fetch the values
        for key,value in data.items():
            if key=="email":
                email=value
            if key=="password":
                pwd=value
        #store data in db online judge
        c="select * from users where email='{}' and password='{}'".format(email,pwd)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t==():
            return render(request,'error.html')
        else:
            return render(request,'welcome.html')
    return render(request,'login_page.html')
