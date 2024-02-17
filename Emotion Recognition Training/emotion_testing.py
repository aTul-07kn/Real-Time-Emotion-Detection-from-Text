# Importing the required libraries
import re
import numpy as np
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from keras.layers import *
from keras.models import load_model
from autocorrect import Speller

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

# preprocess
# tokenization [
# encoding- Glove
# prediction [0,1,2,3]

def get_emotion(i):
  twt = [i]
  #Next, tokenize it
  Twt = preprocess(twt) #this preprocesses the data and tokenizes the data
  # Twt=["i","feeling", "very", "low"]
  
  # Encoding
  Twt = encoding(Twt, Glove) 
  Twt = np.array(Twt) #[0.545,0.056,0.045], [0.455,0.042,0.025], [0.005,0.055,0.075], [0.505,0.046,0.655]

  print(Twt.shape)
  #Predict the sentiment by passing the sentence to the model we built.
  sentiment = mo.predict(Twt)[0]
  print(sentiment)
  #[0.08207992 0.12517232 0.00428951 0.7884583 ]

  label = np.argmax(sentiment)
  print(enc.categories_[0][label])

inp=input("Enter : ")
get_emotion(inp)