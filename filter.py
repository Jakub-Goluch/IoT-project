from flask import Flask, request
import requests

import json

app = Flask(__name__)
lista = []


@app.route("/insert", methods=['POST'])
def insert():
    file = request.json
    filter(file)
    return "OK"


def filter(config):
    r = requests.get(config['from_where'])
    x = r.json()
    if int(config['gen_id']) != 0:
        for item in x:
            if item[0] > config["bigger"] and item[2][0] == int(config['gen_id']):
                lista.append(item)
    else:
        for item in x:
            if item[0] > config["bigger"]:
                lista.append(item)
    filtered = [{"filtered_data": lista}]
    p = requests.post(config["to_where"], json=filtered)

@app.route('/get_data', methods=['GET'])
def get_data():
    return lista


if __name__ == "__main__":
    app.run(debug=True, port=6000)
