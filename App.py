from flask import Flask,render_template,request

#----------- MySQL-----------------
# from flask_mysqldb import MySQL
app=Flask(__name__,template_folder="Template")
# app.config['MYSQL_HOST']="localhost"
# app.config['MYSQL_USER']="root"
# app.config['MYSQL_PASSWORD']=""
# app.config['MYSQL_DB']="rohan"
# mysql=MySQL(app)
# ----------MySQL inports-----------
@app.route('/')
def home():
    return render_template("index.html")

info={"name":"","age":"","gender":"","location":"","orderId":"","feedback":""}
@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        gender=request.form['gender']
        location=request.form['location']
        orderId=request.form['orderId']
        feedback=request.form['feedback']
        EmoDet(name,age,gender,location,orderId,feedback)
        return render_template("response.html")
        # cur=mysql.connection.cursor()
        # cur.execute("INSERT INTO walt(Firstname,Lastname) VALUES(%s,%s)",(fname,lname))
        # mysql.connection.commit()
        # cur.close()
    
def EmoDet(n,a,g,l,o,f):
    info["name"]=n
    info["age"]=a
    info["gender"]=g
    info["location"]=l
    info["orderId"]=o
    info["feedback"]=f
    print(info)

    # return render_template("index.html")
if __name__=="__main__":
    app.run(debug=True)