import time

import paho.mqtt.client as mqtt
import requests
import csv
import threading
from flask import Flask, request

thread_ids = []

app = Flask(__name__)


@app.route("/start", methods=["POST"])
def start():
    file = request.json
    print("start")
    print(file)
    working(file)

    return "OK"


# def get():
#     response = requests.get("http://127.0.0.1:5000/config")
#     response.raise_for_status()
#     if response.status_code != 204:
#         x = response.json()
#         return x


def appka(data):
    method = data['method']
    frequency = data['frequency']
    id = int(data['id'])

    if method == 'MQTT':
        broker = data['broker']
        topic = data['topic']
        client = mqtt.Client("application1")
        client.connect(broker, port=1883)

        while True:
            with open("weather.csv", newline='') as csvfile:
                read = csv.reader(csvfile, delimiter=',')
                for row in read:
                    client.publish(topic, ' '.join(row))
                    print("Send to mqtt, topic: " + topic)
                    time.sleep(frequency)
                    if not thread_dict[id].is_alive():
                        break
            break

    else:
        while True:
            with open("weather.csv", newline='') as csvfile:
                read = csv.reader(csvfile, delimiter=',')
                for row in read:
                    row.insert(0, id)
                    response = requests.post("http://127.0.0.1:4000/add", json={'file': row})
                    f = open("config1.json")
                    print("Send to http")
                    print(thread_dict[id])
                    time.sleep(frequency)
                    if not flags_dict[id]:
                        break
                break


thread_dict = {}
flags_dict = {}


def working(config):
    print("working")
    data = config
    if data['is_active'] == 1:
        t = threading.Thread(target=appka, args=(data,))
        thread_dict[int(data['id'])] = t
        flags_dict[data['id']] = True
        t.start()
    else:
        flags_dict[data['id']] = False
        thread_dict[int(data["id"])].join(timeout=1)
        time.sleep(1)
        print(thread_dict[data['id']])
        print(data['id'])
        print("Thread killed")
        print(thread_dict)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
