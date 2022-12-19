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

data1 =Blueprint('data1',__name__)


@data1.route("/data")
def data():
  mycol = mydb['numbers']
  y=mycol.find()
  print(y)
  # df = pd.DataFrame(y)
  # print(df)
  # x=df.plot.barh(x="city", y="accident",linewidth = 8.0, figsize=(8,5))
  # x.figure.savefig('static/file.svg')  
  bar_chart = pygal.Bar()
  pie_chart= pygal.Pie()
  # bar_chart.title = 'Browser usage in February 2012 (in %)'
  # bar_chart.add('IE', 19.5)
  # bar_chart.add('Firefox', 36.6)
  # bar_chart.add('Chrome', 36.3)
  # bar_chart.add('Safari', 4.5)
  # bar_chart.add('Opera', 2.3)
  # bar_chart.render()
  thislist = []
  for i in y:
    thislist.append(i['accident'])
    bar_chart.add(i['city'], i['accident'])
    pie_chart.add(i['city'], i['accident'])
    

  # bar_chart.add('Fibonacci','hello', thislist)  # Add some values
  bar_chart.render_to_file('static/bar_chart.svg')
  pie_chart.render_to_file('static/pie_chart.svg')
  return render_template('data.html')