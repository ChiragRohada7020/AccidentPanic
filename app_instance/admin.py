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

admin =Blueprint('admin',__name__)


def closest(lst, K):
      
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]
#---------------------------------------ADMIN LOGIN ------------------------------------------------------

@admin.route("/admin_login",methods = ['POST', 'GET'])
def admin_login():
    
    
    error=""
    if 'admin_login' in session:
        return render_template('admin_index.html')

    if request.method == 'POST':
      email=request.form['email']
      password=request.form['password']
      lat=request.form['lat']
      log=request.form['log']
      print(log,lat )
      

      if(float(log)):
        try:
          mycol = mydb['Admin']
          x=mycol.find_one({"email":email,"password":password})
          if(x):
            
            session['admin_id']=x["email"]
            session['admin_loc']=[lat,log]
            accident_count=0
            mycol = mydb["accident"]
            accident=mycol.find({})
            for i in accident:
              accident_count=accident_count+1

            session['accident']=accident_count
            

            

            return redirect(url_for('admin.admin_index'))
        except:
          error="Invalid Email"
        else:
          error="Invalid Email"

      else:
        error="Allow Location!"
        



    
      
    return render_template('admin_login.html',error=error)


#------------------------------------------------------------ADMIN INDEX---------------------------------------------------

@admin.route("/admin_index")
def admin_index():
    error=" "
    if 'admin_id' and 'admin_loc' in session:
      try:
        lat=session['admin_loc'][0]
        log=session['admin_loc'][1]
        print(lat)
        loc="hello"
        lst = [3.64, 5.2, 19.0499205, 19.0471737, 8.5, 8]
        K = float(lat)
        location=closest(lst, K)
        print(location)
        if(location==19.0499205):
          loc='Control Room 1'

        if(location==19.0471737):
          loc='Control Room 2'
           
        print("hello"+session['admin_loc'][0])
        mycol = mydb['vehicle']
        x=mycol.find({"iot_id":None})
        y=mycol.find({"iot_id":1})
        print(x)
        return render_template('admin_index.html',user1=x,user2=y,loc=loc)
      except:
        error="allow location"
        


        
    return render_template('admin_login.html',error=error)


#--------------------------------------------------------ADMIN LOGOUT-----------------------------------


@admin.route("/admin_logout")
def admin_logout():
    session.pop('admin_id')
    session.pop('admin_loc')
    return redirect(url_for('admin.admin_login'))




#-----------------------------------------ADMIN ACCIDENT -----------------------------------

@admin.route("/admin_accident")
def accident():
  try:

    if 'admin_id' in session:
    
      mycol = mydb["accident"]
      x=mycol.find({})
      return render_template('accident.html',accident=x)
    else:
      return redirect(url_for('admin.admin_login'))

  except:
    return 'error occur n'