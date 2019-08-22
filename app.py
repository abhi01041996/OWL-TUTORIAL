import os
import itertools
import re
from flask import *
import ast
import subprocess
import logging


import MySQLdb
def check(u,p):  
    db = MySQLdb.connect(user='root', passwd='', port=3306, host='localhost', db='python_t')
    cursor = db.cursor()
    cursor.execute("select name from login where user='"+u+"' and pass='"+p+"'")
    lis = cursor.rowcount
	
    
    if lis==1:
    	lis = cursor.fetchone()
    	for row in lis:
    		d=row
    	
    	
    else:
    	d="null"
    db.close()
    return d
def check_insert(u,p,e):  
    db = MySQLdb.connect(user='root', passwd='', port=3306, host='localhost', db='python_t')
    cursor = db.cursor()
    cursor.execute("select user from login where email='"+e+"'")
    lis = cursor.rowcount
    cursor.execute("select user from login where user='"+u+"'")
    lis1 = cursor.rowcount

    
    if lis==0 and lis1==0:

    	lis = cursor.execute("INSERT INTO `login`(`user`,`pass`,`email`,`link`) VALUES ('"+u+"', '"+p+"', '"+e+"', 'u1111')")
    	d =str(lis)
    	db.commit()
    	print d
    else:
    	d="exist"
    db.close()
    return d












app=Flask(__name__)

@app.route("/")
def home_me():
	if 'username' in session:
	  	print 'have session'
	  	print session['username']
	  	return render_template('/index.html',methods=['POST'],user=session['username'])
	else:
		return render_template('index.html')

@app.route("/list")
def list_subject():
	if 'username' in session:
	  	print 'have session'
	  	print session['username']
	  	return render_template('/list1.html',methods=['POST'],user=session['username'])
	else:
		return render_template('index.html')
@app.route("/home")
def home():
	  if 'username' in session:
	  	print 'have session'
	  	return render_template('/home.html')
	  else:
	  	return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    # global host,port,uname,pwd,db
    
	    uname = request.form['uname'];
	    pwd = request.form['pwd'];
	    rr=str(check(uname,pwd))
	    if rr!="null":
		    session['username']=request.form['uname']
		    session['pwd']=request.form['pwd']
		    session['id']=rr
		    print uname,pwd,rr
		    return render_template('/home.html',methods=['POST'],user=rr)
	    else:
			return render_template('index.html',error='invaild') 
@app.route('/signup',methods=['POST'])
def signup():
     if 'username' not in session:
	  	uname = request.form['uname1'];
	  	pwd = request.form['pwd1'];
	  	email=request.form['email1'];
	  	rr=str(check_insert(uname,pwd,email))
	  	if rr!="exist":
	  		return render_template('index.html',methods=['POST'],error='id created please sign in')
	  	else:
	  		return render_template('index.html',error='id exist try something else')
     else:
		print 'have session'
		return render_template('home.html')

      	
@app.route("/python/id=<id>")

def python1(id):
	if 'username' in session:
		print 'have session'
		print "ffffffffffffffffffffffffffffffffffffffff"
		db = MySQLdb.connect(user='root', passwd='', port=3306, host='localhost', db='python_t')
		cursor = db.cursor()
		topic=""
		subtopic=""
		body=""
		ins=""
		hint=""
		print "adfasfsdds-------"
		print id
		id=str(id)
		print id


		cursor.execute("select * from data where id='"+id+"'")
		lis=cursor.rowcount
		print lis
		lis = cursor.fetchall()
		for row in lis:
			topic=row[1]
			subtopic=row[2]
			body=Markup(row[3])
			ins=Markup(row[4])
			hint=Markup(row[5])
			code1=str(open("main.py", "r").read())
				
            			
		return render_template('study1.html',methods=['POST'],topic=topic,subtopic=subtopic,body=body,ins=ins,hint=hint,code1=code1,id=id)
	else:
		return render_template('login.html')

    
      	
@app.route("/active",methods=['POST'])

def activeId():
	if 'id' in session:
		print 'have session'
		print "ffffffffffffffffffffffffffffffffffffffff"
		db = MySQLdb.connect(user='root', passwd='', port=3306, host='localhost', db='python_t')
		cursor = db.cursor()
		topic=""
		subtopic=""
		body=""
		ins=""
		hint=""
		print "adfasfsdds-------"
		name=session['id']
		user=session['username']
		print user
		
		print name


		cursor.execute("select link from login where name='"+name+"' and user='"+user+"'")
		lis=cursor.rowcount
		print lis
		
		lis = cursor.fetchone()
		
		for row in lis:
			print row
			topic=row
		if topic=='u1111':
			return render_template('list1.html',methods=['POST'])
		else:
			return redirect(url_for("/python/id="+topic+"'"))


            			
		
	else:
		return render_template('login.html')





@app.route("/next", methods=['POST'])

def pythonnext():
	id = request.form['c'];
	if 'username' in session:
		print 'have session'
		print "ffffffffffffffffffffffffffffffffffffffff"
		db = MySQLdb.connect(user='root', passwd='', port=3306, host='localhost', db='python_t')
		cursor = db.cursor()
		print id
		id=str(id)
		print id


		cursor.execute("select * from data where id>'"+id+"'")
		lis=cursor.rowcount
		
		lis = cursor.fetchone()
		
		for row in lis:
			print row
			topic=row
			return topic

				
            			
		
	
@app.route("/rundown", methods=['POST'])
def rundown():
		if 'username' in session:
				print 'have session'
				print "ffffffffffffffffffffffffffffffffffffffff"
				with open("myapp.txt", "w+") as output:
						
						

				


						try:
							
							
								subprocess.call(["python", "code.py"], stdout=output);
								



							
						
						except Exception as ex:
							print ex

				a=str(open("myapp.txt", "r").read())
				return a


				

@app.route('/calc', methods=['POST'])
def calc():
    txt = request.form['c'];
    print txt
    try:
    	a=open("code.py", "w").write(txt)

    	a= eval(txt)
    	print a
    	return str(a)
    except Exception as e:
    	s = str(e)
    	print s
    	return str(s)

@app.route('/logout')
def logout():
    if 'username'in session:
        session.pop('username')
        session.pop('pwd')
        session.pop('id')
       
        return render_template('index.html',methods=['POST'], error='Successfully Logged Out')

    else:
        print 'no session'
        return render_template ('index.html',methods=['POST'], error='Need to login first')	
if __name__=="__main__":
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(debug=False)




