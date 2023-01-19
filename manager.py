import json

import matplotlib.pyplot as plt
import requests
from flask import Flask, request, render_template, redirect
import paho.mqtt.client as mqtt

app = Flask(__name__)
configs = []
backup = []


@app.route('/add', methods=['POST'])
def add_http_reading():
    file = request.json
    # with open('dane.json', 'a') as f:
    #     s = ''
    #     for i in file:
    #         s += i
    # dane.append(s)
    return 'Record received'


@app.route('/config', methods=['GET'])
def gens():
    configs = backup
    return configs


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        data = request.form
        method = data['method'].upper()
        frequency = int(data['frequency'])
        id_gen = data['id']
        topic = data['topic']
        is_active = int(data['is_active'])
        with open(f'../config1.json', 'r+') as config:
            d = json.load(config)
            if len(method) != 0:
                d['method'] = method
            if len(topic) != 0:
                d['topic'] = topic
            if len(str(frequency)) != 0:
                d['frequency'] = frequency
            d['is_active'] = int(is_active)
            d['id'] = int(id_gen)
            config.seek(0)
            json.dump(d, config, indent=4)
            config.truncate()
            dictionary = {"id": d['id'], 'is_active': d['is_active'], 'method': d['method'], 'address': d['address'],
                          "frequency": d['frequency'], "broker": d['broker'], "topic": d['topic']}
            configs.append(dictionary)
            backup.append(dictionary)
            response = requests.post("http://127.0.0.1:3000/start", json=dictionary)

        return dictionary


@app.route("/stop")
def stop():
    for config in backup:
        config['is_active'] = 0

    return redirect("/config")


@app.route("/change", methods=["GET", 'POST'])
def change():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        global configs
        data = request.form
        method = data['method'].upper()
        frequency = int(data['frequency'])
        id_gen = int(data['id'])
        topic = data['topic']
        is_active = int(data['is_active'])
        for config in backup:
            if config['id'] == id_gen:
                if len(method) != 0:
                    config['method'] = method
                if len(topic) != 0:
                    config['topic'] = topic
                if len(str(frequency)) != 0:
                    config['frequency'] = frequency
                config['is_active'] = is_active
                dictionary = {"id": config['id'], 'is_active': config['is_active'], 'method': config['method'],
                              'address': config['address'],
                              "frequency": config['frequency'], "broker": config['broker'], "topic": config['topic']}
        response = requests.post("http://127.0.0.1:3000/start", json=dictionary)
        return redirect("/config")


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'GET':
        return render_template("filter.html")
    if request.method == 'POST':
        data = request.form
        from_where = data["from_where"]
        what = data['what']
        bigger = int(data['bigger'])
        to_where = data['to_where']
        gen_id = int(data['gen_id'])
        dictionary = {'from_where': from_where, 'what': what, "bigger": bigger, "to_where": to_where, 'gen_id': gen_id}
        response = requests.post("http://127.0.0.1:6000/insert", json=dictionary)
        return redirect("/filter")


@app.route('/dtv', methods=['GET', 'POST'])
def dtv():
    if request.method == 'GET':
        return render_template("dtv.html")
    if request.method == 'POST':
        data = request.form
        gen_id = int(data['gen_id'])
        agre = int(data['agre'])
        filt = int(data['filter'])
        if gen_id != 0:
            r = requests.get("http://127.0.0.1:4000/get_data")
            r.raise_for_status()
            if r.status_code != 204:
                x = r.json()
            lista = [gen for gen in x if gen[2][0] == gen_id]
            plt.bar(1, len(lista))
            plt.title(f'{len(lista)}')
            plt.ylabel('Count of data send by gen')
            plt.savefig('static/wykres.png')
        elif agre == 1:
            r = requests.get("http://127.0.0.1:4000/get_data")
            r.raise_for_status()
            if r.status_code != 204:
                x = r.json()
            plt.bar(1, len(x))
            plt.title(len(x))
            plt.ylabel('Count of data send by aggregator')
            plt.savefig('static/wykres.png')
        else:
            r = requests.get("http://127.0.0.1:6000/get_data")
            r.raise_for_status()
            if r.status_code != 204:
                x = r.json()
            plt.bar(1, len(x))
            plt.title(len(x))
            plt.ylabel('Count of data send by filter')
            plt.savefig('static/wykres.png')
        return redirect("/visualize")


@app.route('/visualize', methods=['GET'])
def visualize():
    return render_template('vis.html')


# def on_message(client, userdata, message):
#     print(message.payload.decode('utf-8'))


if __name__ == '__main__':
    # client = mqtt.Client()
    # client.connect('test.mosquitto.org', port=1883)
    # client.on_message = on_message
    # client.loop_start()
    # client.subscribe('weather')
    # client.subscribe('wearables')
    # client.subscribe('water_quality')
    # client.subscribe('parking')
    # client.subscribe('location')

    app.run(debug=True)
