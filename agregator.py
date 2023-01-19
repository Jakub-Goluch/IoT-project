import requests
from flask import Flask, request, render_template
from datetime import datetime, timedelta

app = Flask(__name__)
files = []
method = 'HTTP'
frequency = 30
ids = 1

@app.route("/add", methods=['POST'])
def add_reading():
    global ids
    file = request.json['file']
    files.append([ids, datetime.now(), file])
    ids += 1
    print(files)
    return "Record recived"


@app.route("/insert", methods=['POST', 'GET'])
def insert():
    if request.method == 'GET':
        return render_template('agre.html')
    if request.method == 'POST':
        global method
        global frequency
        data = request.form
        if len(data['method']) != 0:
            method = data['method'].upper()
        frequency = int(data['frequency'])
        dt = datetime.now()
        temp = 0
        for element in files:
            if element[1] > dt - timedelta(minutes=frequency):
                temp += 1
        count = [{"Count of files": temp}]
        address = "http://127.0.0.1:5000/add"
        r = requests.post(address, json=count)
        return str(temp)

@app.route("/get_data", methods=['GET'])
def get_data():
    return files


if __name__ == "__main__":
    app.run(debug=True, port=4000)
