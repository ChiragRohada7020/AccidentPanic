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







def closest(lst, K):
      
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]
      
# Driver code




app = Flask(__name__)
CORS(app)
app.secret_key=os.urandom(24)
app.config['UPLOAD_FOLDER']='./static/img'
bcrypt = Bcrypt(app)


if __name__ == '__main__':
    app.run(host='192.168.0.1', port=5000)



myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["IOT"]



mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kjseit.q@gmail.com'
app.config['MAIL_PASSWORD'] = 'ghkwfpxqlicxlfch'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
global n,otpp
n = random.randint(1000,9999)




admin_user = {
  "name":"user",
  "email":"user@gmail.com",
  "password":"hello"
}
  
initial_user = {
  "name":"user",
  "email":"user@gmail.com",
  "password":"hello"
}

@app.route("/")
def hello_world():
    
  try:
        if 'user_id' in session:
        
          

          return render_template('index.html',type="Logout",type1="logout") 
        return render_template('index.html',type="Login",type1="login") 
  except:
    return render_template('error.html')




@app.route("/login",methods = ['POST', 'GET'])
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

        
      
      
    




@app.route("/logout")
def user_logout():
    session.pop('user_id')
    
    return redirect(url_for('hello_world'))


@app.route("/admin_index")
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

@app.route("/admin_logout")
def admin_logout():
    session.pop('admin_id')
    session.pop('admin_loc')
    return redirect(url_for('admin_login'))


@app.route("/next")
def next():
    
    
    
    return render_template('next.html')


@app.route("/admin_login",methods = ['POST', 'GET'])
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
            

            

            return redirect(url_for('admin_index'))
        except:
          error="Invalid Email"
        else:
          error="Invalid Email"

      else:
        error="Allow Location!"
        



    
      
    return render_template('admin_login.html',error=error)




@app.route("/sign_up",methods = ['POST', 'GET'])
def sign_up():
    global n
    
    
    try:

        if request.method == 'POST':
            user_name=request.form['name']
            user_password=request.form['password']
            user_email=request.form['email']
            user_password = bcrypt.generate_password_hash(user_password)
      

        
   
            mycol = mydb['Users']
            x=mycol.find_one({"email":user_email})
            if x:
              return render_template('sign-up.html',error="email aleardy registered")
            else:
          

          
              n = random.randint(1000,9999)
    
      

    

      
           

      
      

      
      
           
        
      
              msg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [user_email]
               )
              msg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. Use the following OTP to complete your Sign Up procedures. Its a one time otp</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">"""+str(n)+"""</h2>
      <p style="font-size:0.9em;">Regards,<br />Pbl Project</p>
      <hr style="border:none;border-top:1px solid #eee" />
      <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>Pbl Project</p>
        <p>Flat 302</p>
        <p>Mumbai , MH.</p>
      </div>
    </div>
  </div>
        """
      
            mail.send(msg)
   
   
            return redirect(url_for('check',email=user_email,password=user_password,name=user_name))
    
        return render_template("sign-up.html",error="")
    except Exception as e:
        print(e)

    
  
    


#------------------------------------------------------------OTP_CHECK--------------------------------------------------------



@app.route("/check/<email>/<password>/<name>",methods = ['POST', 'GET'])
def check(email,password,name):

    global n,otpp
  
  
  

  
    if request.method == 'POST':
        otp=request.form['otp']
     
      
        if (str(n) == str(otp)):
            
            msgg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [email]
               )
            msgg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. We will contact you soon</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;"></h2>
      <p style="font-size:0.9em;">Regards,<br />Pbl Project</p>
      <hr style="border:none;border-top:1px solid #eee" />
      <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>Pbl Project</p>
        <p>Flat 302</p>
        <p>Mumbai , MH.</p>
      </div>
    </div>
  </div>
        """
       
        
            mail.send(msgg)
   
            mycol = mydb["Users"]
            mycol.insert_one({"email":email,"name":name,"password":password})
            n = random.randint(1000,9999)
       
        
            return redirect(url_for('login'))
        else:
            n = random.randint(1000,9999)
        
        
            text="invalid email"
            return redirect(url_for('sign_up'))







    return render_template('check.html',email=email,name=name,password=password)

@app.route("/iot/<id>/<lat>/<log>")
def iot(id,lat,log):
    try:   
            # mycol = mydb["vehicle"]
            # mycol.find({'iot_id':id})
            # iot_id=request.form['iot_id']
            # location=request.form['location']
            # location=location.split(',')
            mycol = mydb["accident"]

            mycol.insert_one({"iot_id":int(id),"location":[float(lat),float(log)]})

            print(id)
            # print(location[1])
            return "accident detected"
    except:
        print("Not valid")

        
    return "Not Valid"

@app.route("/vehicle",methods = ['POST', 'GET'])
def add_vehicle():
    if 'user_id' in session:
        try:
            if request.method == 'POST':
                vehicle_no=request.form['vehicle_no']
                first_name=request.form['first_name']
                mobile_no=request.form['mobile_no']
                vehicle_name=request.form['vehicle_name']
                address=request.form['address']
                
                f = request.files['file']
                print(f)
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], vehicle_no+'.png' ))

                mycol = mydb["vehicle"]
                mycol.insert_one({"vehicle_no":vehicle_no,"email":session['user_id'],"iot_id":None,"mobile_no":mobile_no,"vehicle_name":vehicle_name,"first_name":first_name,"address":address})
            return redirect(url_for('user_index'))
        except:
            return render_template('vehicle.html')
    else:
        return render_template('error.html')

@app.route("/give_no/<id>")
def give_no(id):
    print(id)
    
    
    mycol = mydb["vehicle"]
    x=mycol.find({"vehicle_no":id})
    for i in x:
       print(i)
      #  mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':i['_id']}})
       mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':1}})
       msgg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [i['email']]
               )
       msgg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. Your vehicle no :-"""+i['vehicle_no'] +""" is ready to go</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;"></h2>
      <p style="font-size:0.9em;">Regards,<br />Pbl Project</p>
      <hr style="border:none;border-top:1px solid #eee" />
      <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>Pbl Project</p>
        <p>Flat 302</p>
        <p>Mumbai , MH.</p>
      </div>
    </div>
  </div>
        """
       
        
       mail.send(msgg)
    
    # mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':"kjhk"}})
       return redirect(url_for('admin_index'))
@app.route("/assign/<id>")
def assign(id):
    print(id)
    
    
    mycol = mydb["vehicle"]
    x=mycol.find({"vehicle_no":id})
    for i in x:
       print(i)
       mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':str(i['_id'])}})
       
       msgg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [i['email']]
               )
       msgg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. Your vehicle no :-"""+i['vehicle_no'] +""" is ready to go</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;"></h2>
      <p style="font-size:0.9em;">Regards,<br />Pbl Project</p>
      <hr style="border:none;border-top:1px solid #eee" />
      <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>Pbl Project</p>
        <p>Flat 302</p>
        <p>Mumbai , MH.</p>
      </div>
    </div>
  </div>
        """
       
        
       mail.send(msgg)
    
    # mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':"kjhk"}})
       return redirect(url_for('admin_index'))




@app.route("/user_index")
def user_index():
    if 'user_id' in session:

        mycol = mydb["vehicle"]
        data=mycol.find({"email":session['user_id']})
        return render_template('user_index.html',type="logout",type1="logout",data=data)
    else:
        return redirect(url_for('login'))
                
@app.route("/iot1",methods = ['POST', 'GET'])
def iot1():
  try:

    if 'admin_id' in session:
      y=0
      mycol = mydb["accident"]
      x=mycol.find({})
      for i in x:
        y=y+1

      if(y>session['accident']):
        count=y-session['accident']
        return {"hello":count}

      return {"hello":0}

  except:  
    return "error occur"
     
 
@app.route("/iot2")
def iot2():
  return render_template('user1.html')

@app.route("/admin_accident")
def accident():
  try:

    if 'admin_id' in session:
    
      mycol = mydb["accident"]
      x=mycol.find({})
      return render_template('accident.html',accident=x)
    else:
      return redirect(url_for('admin_login'))

  except:
    return 'error occur n'

    

@app.route("/data")
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


@app.route("/user_data/<id>")
def user_data(id):
  mycol = mydb['vehicle']
  y=mycol.find({'vehicle_no':id},{'_id':0})
  
  return y[0];

@app.route("/user_data2/<id>")
def user_data2(id):
  print(id)
  mycol = mydb['vehicle']
  y=mycol.find({'iot_id':id},{'_id':0})
  
  return y[0];

# @app.route('/download/<path:filename>', methods=['GET'])
# def download(filename):
#     """Download a file."""
#     logging.info('Downloading file= [%s]', filename)
#     logging.info(app.root_path)
#     full_path = os.path.join(app.root_path, UPLOAD_FOLDER)
#     logging.info(full_path)
#     return send_from_directory(full_path, filename, as_attachment=True)

global mus
@app.route("/mus/<id>/")
def mus(id):
    try:   
            # mycol = mydb["vehicle"]
            # mycol.find({'iot_id':id})
            # iot_id=request.form['iot_id']
            # location=request.form['location']
            # location=location.split(',')
            
            mus=id
            # print(location[1])
            return mus
    except:
        print("Not valid")

        
    return "Not Valid"

@app.route("/mus_send", methods=['GET'])
def mus_send():
    try:   
            # response = flask.jsonify({'some': 'data'})
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # return response
            
            return mus
    except:
        print("Not valid")

        
    return "Not Valid"