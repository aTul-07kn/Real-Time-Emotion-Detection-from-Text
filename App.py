from flask import Flask,render_template,request,redirect,url_for
# Importing the required libraries
import re
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from keras.layers import *
from keras.models import load_model
from autocorrect import Speller

# for sending mail
# we are importing the send_email() function from the emailTesting.py file which is in Emailmodule folder
# Emailmodule folder --> emailTesting.py --> send_email() function is called
from Emailmodule.emailTesting import send_email

#----------- MySQL-----------------
from flask_mysqldb import MySQL
app=Flask(__name__,template_folder="Template")
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="customer"
mysql=MySQL(app)
# ----------MySQL inports-----------

@app.route('/')
def home():
    return render_template("index.html")

# info dictionary to store customer information
info={"name":"","email":"","age":"","gender":"","location":"","orderId":"","product":"","feedback":"","emotion":""}

@app.route('/response')
def response():
    return render_template("response.html")

@app.route("/failure")
def failure():
    return render_template("failure.html")

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        age=request.form['age']
        gender=request.form['gender']
        location=request.form['location']
        orderId=request.form['orderId']
        product_name=request.form['product']
        feedback=request.form['feedback']
    
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Check if the orderId exists in the orders_table
        cur.execute("SELECT * FROM `orders_table` WHERE order_id = %s", (orderId,))
        existing_orderid = cur.fetchone()
        
        if existing_orderid==None:
            print(f"Order ID {orderId} does not exist in the orders_table.")
            cur.close()
            return redirect(url_for('failure'))

        spell = Speller(lang="en") #autocorrect library
        correct_feedback=spell(feedback)

        emotion=EmoDet(name,email,age,gender,location,orderId,product_name,correct_feedback)
        try:
            cur.execute("INSERT INTO customer_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,email,age,gender,location,orderId,product_name,correct_feedback,emotion))
            mysql.connection.commit()
            cur.close()

            # sending mail to customer
            send_email(name, email, emotion)
            
            #thankyou page--load after submitting the form
            return redirect(url_for('response'))
        except Exception as e:
            print("duplicate order EXCEPTION")
            return render_template("duplicate.html")  #if the user again tries to give feedback, then render the duplicate feedback template
    
#saved model is for 50 epochs
mo=load_model("trained_model_3.h5")

glove ='glove.6B.50d.txt'

def load_glove_embeddings(path):
    embeddings_index = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
    return embeddings_index

Glove = load_glove_embeddings(glove)

Sentiments=['anger', 'fear', 'joy', 'sadness']

# Perform one-hot encoding on df[0] i.e emotion
def encoding(sentences, Glove):
    Encoded_vec = []
    for sentence in sentences:
        sent_vec = []
        for token in sentence:
            token = token.numpy().decode('utf-8')
            if token in Glove:
                sent_vec.append(Glove[token])
            else:
                sent_vec.append(np.zeros(50))
        Encoded_vec.append(sent_vec)
    return Encoded_vec

enc = OneHotEncoder(handle_unknown='ignore')
Y = enc.fit_transform(np.array(Sentiments).reshape(-1,1)).toarray()
print(Y.shape)

def preprocess(Sentences):
    # Extract a substring of up to 300 characters
    sentences = tf.strings.substr(Sentences, 0, 300)

    # Replace HTML line breaks with spaces
    sentences = tf.strings.regex_replace(sentences, b"<br\\s*/?>", b" ")

    # Replace characters that are not letters or apostrophes with spaces
    sentences = tf.strings.regex_replace(sentences, b"[^a-zA-Z']", b" ")

    # Initialize the Speller class
    spell = Speller(lang="en")

    # Convert the TensorFlow tensor to a Python list of strings
    python_strings = [sentence.decode('utf-8') for sentence in sentences.numpy()]

    # Apply spelling correction on each string
    corrected_sentences = [spell(sentence) for sentence in python_strings]
    # print(corrected_sentences)

    # Split the sentences into words
    sentences = tf.strings.split(corrected_sentences)

    # Convert to lowercase
    sentences = tf.strings.lower(sentences)

    # Convert the result to a tensor with padding
    sentences = sentences.to_tensor(default_value=b"<pad>")

    return sentences

# function to predict emotion
def get_emotion(i):  
  twt = [i]
  #Next, tokenize it
  Twt = preprocess(twt)

  # Encoding
  Twt = encoding(Twt, Glove)
  Twt = np.array(Twt)
  print(Twt.shape)
  #Predict the sentiment by passing the sentence to the model we built.
  sentiment = mo.predict(Twt)[0]
  label = np.argmax(sentiment)
  return(enc.categories_[0][label])

# function to detect emotion and printing..
def EmoDet(name,email,age,gender,location,orderid,product,feedback):
    emotion=get_emotion(feedback)
    print(emotion)
    info["name"]=name
    info["email"]=email
    info["age"]=age
    info["gender"]=gender
    info["location"]=location
    info["orderId"]=orderid
    info["product"]=product
    info["feedback"]=feedback
    info["emotion"]=emotion
    print(info)
    return emotion

if __name__=="__main__":
    app.run(debug=True, port=5000)

# use this to use git lfs, to store all the large files in some in a separate storage server like GitHuB LFS server
# git lfs migrate import --include="*.txt" 