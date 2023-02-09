# load dependencies
import re
import pickle
import nltk
import corpora
import numpy as np
import pandas as pd
import streamlit as st
nltk.download('stopwords')

import subprocess
cmd = ['python3', '-m', 'textblob.download_corpora']
subprocess.run(cmd)
print("corpora downloaded successfully")

from textblob import Word
from keras import backend as K
from nltk.corpus import stopwords
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# path of the model
MODEL_PATH = r"model_LSTM.h5"
# maximize number of the allowed word in an input
max_words = 500
# shape of input data passed for prediction
max_len = 1000
# path of tokenizer file
tokenizer_file = r"tokenizer_LSTM.pkl"

# load tokenizer
with open(tokenizer_file,'rb') as handle:
    tokenizer = pickle.load(handle)
    
# apply text cleaning to input data
def text_cleaning(line_from_column):
    text = line_from_column.lower()
    # Replacing the digits/numbers
    text = text.replace('d', '')
    # remove stopwords
    words = [w for w in text if w not in stopwords.words("english")]
    # apply stemming
    words = [Word(w).lemmatize() for w in words]
    # merge words
    words = ' '.join(words)
    return text

# load the sentiment analysis model
@st.cache(allow_output_mutation=True)
def Load_model():
    model = load_model(MODEL_PATH)
    model.summary() # included making it visible when the model is reloaded
    session = K.get_session()
    return model, session

if __name__ == '__main__':
    st.title('Political Threads Sentiment Classification App')
    st.write('A simple sentiment analysis classification app')
    st.subheader('Input the Thread below')
    sentence = st.text_area('Enter your thread here',height=200)
    predict_btt = st.button('predict')
    model, session = Load_model()
    if predict_btt:
        clean_text = []
        K.set_session(session)
        i = text_cleaning(sentence)
        clean_text.append(i)
        sequences = tokenizer.texts_to_sequences(clean_text)
        data = pad_sequences(sequences, maxlen =  max_len)
        # st.info(data)
        prediction = model.predict(data)
        prediction_prob_negative = prediction[0][0]
        prediction_prob_neutral = prediction[0][1]
        prediction_prob_positive= prediction[0][2]
        prediction_class = prediction.argmax(axis=-1)[0]
        print(prediction.argmax())
        st.header('Prediction using LSTM model')
        if prediction_class == 0:
          st.warning('Thread has negative sentiment')
        if prediction_class == 1:
          st.success('Thread has neutral sentiment')
        if prediction_class==2:
          st.success('Thread has positive sentiment')
