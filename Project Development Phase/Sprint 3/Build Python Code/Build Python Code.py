import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from gevent.pywsgi import WSGIServer
import os
import requests
#from joblib import load
app = Flask(__name__)
model = pickle.load(open('RandomForestRegressor.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')
