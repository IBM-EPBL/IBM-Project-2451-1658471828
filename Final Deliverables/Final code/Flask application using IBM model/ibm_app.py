import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from gevent.pywsgi import WSGIServer
import os
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "DJ-qq-RyTIQ1elVLq32920_ooU33DUuoK3JXCpvU0ZIN"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

#from joblib import load
app = Flask(__name__)
model = pickle.load(open('RandomForestRegressor.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    print(x_test)
    #sc = load('scalar.save') 
    payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5']], "values": [[8,160,380,3504,82,1]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/02acdcd8-101c-43ce-9c9b-862ef5b9247f/predictions?version=2022-11-17', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print("Scoring response")
    print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    print(output)
    if(output<=9):
        pred="Worst performance with mileage " + str(prediction[0]) +". Carry extra fuel"
    if(output>9 and output<=17.5):
        pred="Low performance with mileage " +str(prediction[0]) +". Don't go to long distance"
    if(output>17.5 and output<=29):
        pred="Medium performance with mileage " +str(prediction[0]) +". Go for a ride nearby."
    if(output>29 and output<=46):
        pred="High performance with mileage " +str(prediction[0]) +". Go for a healthy ride"
    if(output>46):
        pred="Very high performance with mileage " +str(prediction[0])+". You can plan for a Tour"
        
    
    return render_template('index.html', prediction_text='{}'.format(pred))

if __name__ == "_main_":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0',port=port)