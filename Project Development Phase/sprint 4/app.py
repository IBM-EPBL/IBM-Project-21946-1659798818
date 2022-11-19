
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail,Message
from linkedin_api import Linkedin
import requests
import pandas as pd
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as mls
import pandas as pd 
import csv
import os
import json
import ibm_db
dsn_hostname = "54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "mzw99208"
dsn_pwd = "X5OCas8TwAsNxiZ9"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "32733"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

dsn = (
     "DRIVER={0};"
     "DATABASE={1};"
     "HOSTNAME={2};"
     "PORT={3};"
     "PROTOCOL={4};"
     "UID={5};"
     "PWD={6};"
     "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

print(dsn)
db=ibm_db
conn = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)
var_list = []
PROXYCURL_API_KEY = '877e8019097a754907f2eb658b2a44e17374afb4'  # todo - fill this field up
app = Flask(__name__)
app.secret_key='a'
@app.route('/')
def home():
  return render_template('login.html')

@app.route('/linkpass')
def linkpass():
  return render_template('linked.html')


@app.route('/skillreg',methods=["POST", "GET"])
def dashhome():
  insert_sql = "INSERT INTO SKILLUSER (EMAILID, PASSWORD, NAME,PHONENUMBER)  VALUES (?,?,?,?)"
  prep_stmt = ibm_db.prepare(conn, insert_sql)
  email = request.form['username']
  password= request.form['password']
  name = request.form['name']
  ph = request.form['phonenum']
  var_list.append(email)
  var_list.append(password)
  var_list.append(name)
  var_list.append(ph)
  ibm_db.bind_param(prep_stmt, 1, email)
  ibm_db.bind_param(prep_stmt, 2, password)
  ibm_db.bind_param(prep_stmt, 3, name)
  ibm_db.bind_param(prep_stmt, 4, ph)
  print("giun")
  ibm_db.execute(prep_stmt)
  return render_template('email.html')

@app.route('/gojob',methods=["POST", "GET"])
def gojob():
    print("job")
    url = "https://indeed11.p.rapidapi.com/"
    p=1
    payload = {
        "search_terms": "Marketing",
        "location": "United States",
        "page": "1"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "9381357d88msha354337c2eb1e98p1348a7jsn192d84997537",
        "X-RapidAPI-Host": "indeed11.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    html=response.text
    dict=json.loads(html)
    print(dict)
    return render_template('upgrade.html',data=dict)
@app.route('/register',methods=["POST", "GET"])
def register():
  return render_template('register.html')


@app.route('/linkedlogin',methods=["POST", "GET"])
def linkedlogin():
  username = request.form['username']
  api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
  header_dic = {'Authorization': 'Bearer ' + PROXYCURL_API_KEY}
  params = {
      'url': f'https://www.linkedin.com/in/{username}',
  }
  response = requests.get(api_endpoint,
                          params=params,
                          headers=header_dic)
  print(response.json())
  return render_template('skill.html')


@app.route('/confirm',methods=["POST", "GET"])
def confirm():
  print("hi")
  msg = Message('Registration successfully completed', sender = 'pradeepnarayaniyappan@gmail.com', recipients = [var_list[0]])
  msg.body = "Thank You for registering in Skill And Job recommender and Submit your resume in your profile section and Can apply for your desired jobs"
  return render_template('Application form.html')

@app.route('/submitapp',methods=["POST", "GET"])
def subapp():
  insert_sql = "INSERT INTO DETAILS (NAME,FNAME,GENDER,EID,ADDRESS,TENTHMARK,TWELTHMARK,DEG_CGPA,AADHAR,DOMAIN)  VALUES (?,?,?,?,?,?,?,?,?,?)"
  prep_stmt = ibm_db.prepare(conn, insert_sql)
  name = request.form['yourname']
  fname = request.form['fname']
  GD = request.form['GD']
  EID = request.form['EID']
  add = request.form['AL1']
  mark1 = request.form['s5']
  mark2 = request.form['h5']
  cgpa = request.form['b5']
  AADHAR = request.form['Aadhar']
  DOMAIN = request.form['domain']

  ibm_db.bind_param(prep_stmt, 1,str( name),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_VARCHAR)
  ibm_db.bind_param(prep_stmt, 2,str (fname),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_VARCHAR)
  ibm_db.bind_param(prep_stmt, 3,str (GD),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_VARCHAR)
  ibm_db.bind_param(prep_stmt, 4,str (EID),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_VARCHAR)
  ibm_db.bind_param(prep_stmt, 5,str (add),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_VARCHAR)
  ibm_db.bind_param(prep_stmt,6,str (mark1),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_INTEGER)
  ibm_db.bind_param(prep_stmt,7,str (mark2),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_INTEGER)
  ibm_db.bind_param(prep_stmt, 8,str (cgpa),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_INTEGER)
  ibm_db.bind_param(prep_stmt, 9, str(AADHAR),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_INTEGER)
  ibm_db.bind_param(prep_stmt, 10,str (DOMAIN),ibm_db.SQL_PARAM_INPUT,ibm_db.SQL_VARCHAR)

  print("giun")
  ibm_db.execute(prep_stmt)
  msg = Message('Your Application has been Saved', sender = 'pradeepnarayaniyappan@gmail.com', recipients = [EID])
  msg.body = "Further you can edit the application form in your profile section and continue your job searching and apply to it"
  return render_template('skill.html')
  

@app.route('/skilllogin',methods=["POST", "GET"])
def login():
  msg = ''
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      email = request.form['username']
      password = request.form['password']
      sql = "SELECT * FROM SKILLUSER WHERE EMAILID =? AND PASSWORD =?"
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.bind_param(stmt,2,password)
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)

      if account:
          msg = 'Logged in successfully !'
          return render_template('skill.html', msg = msg)
      else:
          msg = 'Incorrect email / password !'
  return render_template('login.html', msg = msg)
  
if __name__ == '__main__':
    app.run(debug=True)



