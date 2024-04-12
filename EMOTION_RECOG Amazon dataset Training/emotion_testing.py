import re
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from keras.layers import *
from keras.models import load_model
from autocorrect import Speller
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the saved model
mo = load_model("(balanced)20epochs_Own_Amazon.h5")

glove = 'glove.6B.50d.txt'

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

Sentiments = ['Angry', 'Sad', 'Happy', 'Disgusted']

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
Y = enc.fit_transform(np.array(Sentiments).reshape(-1, 1)).toarray()

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

    # Split the sentences into words
    sentences = tf.strings.split(corrected_sentences)

    # Convert to lowercase
    sentences = tf.strings.lower(sentences)

    # Convert the result to a tensor with padding
    sentences = sentences.to_tensor(default_value=b"<pad>")

    return sentences

def pad_or_truncate(sentences, max_length, glove_embedding):
    # Preprocess and encode sentences
    processed_sentences = preprocess(sentences)
    encoded_sentences = encoding(processed_sentences, glove_embedding)

    # Pad or truncate to the specified max_length
    padded_or_truncated = pad_sequences(encoded_sentences, maxlen=max_length, padding='post', truncating='post', dtype='float32')

    return padded_or_truncated

def get_emotion(i):
    # Input sentences
    twt = [i]

    # Specify max_length based on your model's requirements
    max_length = 72

    # Preprocess and pad/truncate
    Twt = pad_or_truncate(twt, max_length, Glove)

    # Predict the sentiment by passing the sentence to the model
    sentiment = mo.predict(Twt)[0]
    label = np.argmax(sentiment)
    emotion = enc.categories_[0][label]

    return emotion

# Example usage
while True:
    inp = input("Enter: ")
    if inp=="Q":
        break
    predicted_emotion = get_emotion(inp)
    print("Predicted Emotion:", predicted_emotion)