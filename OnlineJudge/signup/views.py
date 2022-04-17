from django.shortcuts import render
import mysql.connector as sql
# from .models import Post
fn=''
ln=''
s=''
email=''
pwd=''
un=''
# Create your views here.
def signaction(request):
    global fn,ln,s,email,pwd,un
    if request.method=="POST":
        #open connection to db
        m=sql.connect(host="localhost",user="root",password="root",database='onlinejudge')
        cursor=m.cursor
        data=request.POST
        #fetch the values
        for key,value in data.items():
            if key=="first_name":
                fn=value
            if key=="last_name":
                ln=value
            if key=="sex":
                s=value
            if key=="email":
                email=value
            if key=="password":
                pwd=value
            if key=="user_name":
                un=value
        #store data in db online judge
        c="insert into users('{}','{}','{}','{}','{}','{}')".format(fn,ln,s,email,pwd,un)
        cursor.execute(c)
        m.commit()
    
    return render(request,'signup_page.html')
