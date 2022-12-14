import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template
from main import *

app=Flask(__name__)
## load the model
model=pickle.load(open('HousePrice.pkl','rb'))
scaler=pickle.load(open('scaling.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    data1=list(data.values())
    print(data1)
    data_in=DataProcess()
    pre_data=data_in.process_input(data1)
    print(pre_data)
    res = scaler.transform(np.array(pre_data).reshape(1, -1))
    print(res)
    output=model.predict(res)
    print(output[0])
    return jsonify((str(output[0])))
@app.route('/predict',methods=['POST'])
def predict():
    out_data = [x for x in request.form.values()]
    print(out_data)
    data_in=DataProcess()
    pre_data=data_in.process_input(out_data)
    print(pre_data)
    final_input = scaler.transform(np.array(pre_data).reshape(1, -1))
    print(final_input)
    output = model.predict(final_input)[0]
    return render_template("home.html",prediction_text="The House price prediction is {}".format(output))

if __name__=="__main__":
    app.run(debug=True)

