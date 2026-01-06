from flask import Flask, render_template,request
import requests 
import mysql.connector
from dotenv import load_dotenv
load_dotenv() 
import os
apikey= os.getenv("APIKEY")
con = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_DATABASE")
    )
cursor = con.cursor()

url="https://api.api-ninjas.com/v1/quotes"
headers={'X-Api-Key': apikey}
def get_quote():
    response=requests.get(url,headers=headers)
    data=response.json()
    if isinstance(data,list) and len(data)>0:
        quote_value = data[0]['quote']
        author_value = data[0]['author']
        category_value = data[0]['category']
        return quote_value, author_value, category_value
    else:
        return "No quote found"
        
app=Flask(__name__)
app.config["secretkey"]=os.getenv("secretkey")
@app.route('/')
def home():
    quote,author,category=get_quote()
    return render_template('ai_quote.html',
                           quote1 =quote,
                           author1=author,
                           category1=category)

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method=="POST":
        user=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        cursor.execute("insert into users(name,email,password) values (%s,%s,%s)",[user,email,password])
        con.commit()
        return "values stored"
    return render_template('reg.html')

app.run(use_reloader=True)
#data base connection
