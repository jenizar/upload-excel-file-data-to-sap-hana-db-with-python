from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import platform
from hdbcli import dbapi

from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route("/upload",methods=['POST','GET'])
def upload():
    if request.method=='POST':
      # upload file flask
        file1 = request.files['upload-file']
        data1 = pd.read_excel(file1)
      # loop through the rows using iterrows()
        for index, row in data1.iterrows():
            symbol1 = row['symbol']
            elements1 = row['elements']
            class1 = row['class']
            #class1 = f"{class1:,d}"
            #print(row['symbol'], row['elements'], row['class'])
            con = dbapi.connect(
            address="4b25c31e-9856-4586-a8d0-b1caa0f89c02.hana.trial-us10.hanacloud.ondemand.com",
            port=443,
            user="DBADMIN",
            password="MyHanadb911_")
            cur=con.cursor()
            sql = "INSERT INTO EXCEL.ELEMENTS(symbol, elements, class) VALUES (?,?,?)"
            val = (symbol1,elements1,class1)
            cur.execute(sql, val)
            con.commit()
            flash('Upload data','success')
        return redirect(url_for("index"))
    #return render_template('data.html', data=data.to_dict())

if __name__=='__main__':
    app.secret_key='admin911'
    app.run(debug=True)        
