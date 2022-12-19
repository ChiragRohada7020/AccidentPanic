from flask import Blueprint
from distutils.log import error
import email
from logging import exception
from pickletools import float8
from flask import Flask
from flask import render_template
import pymongo
from flask_mail import Mail, Message
import random
from flask import request
from flask import abort, redirect, url_for,session
import os
import numpy as np
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.figure import Figure
import pygal      
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_bcrypt import Bcrypt
from pymongo import mongo_client
from flask_cors import CORS

myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["IOT"]

index =Blueprint('index',__name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)


#--------------------------------------------  USER LOGOUT ------------------------------------------



@index.route("/logout")
def user_logout():
    session.pop('user_id')
    
    return redirect(url_for('index.hello_world'))




#---------------------------------------------  USER INDEX----------------------------------------------


@index.route("/")
def hello_world():
    
  try:
        if 'user_id' in session:
        
          

          return render_template('index.html',type="Logout",type1="logout") 
        return render_template('index.html',type="Login",type1="login") 
  except:
    return render_template('error.html')



#--------------------------------------------- USER LOGIN --------------------------------------------------

@index.route("/login",methods = ['POST', 'GET'])
def login():
    
    
    error=""

    if request.method == 'POST':
      email=request.form['email']
      password=request.form['password']
      


      try:
          mycol = mydb['Users']
          x= mycol.find_one({"email":email})
          
          if(bcrypt.check_password_hash(x['password'], password)):
            
            session['user_id']=x["email"]
            return redirect(url_for('user_index'))
          else:
            error="invalid credential"
            return render_template('login.html',error=error)
      except:
          return render_template('error.html')
    else:
       return render_template('login.html',error=error)
