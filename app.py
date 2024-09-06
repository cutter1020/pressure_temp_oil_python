from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
import os
import requests

secret = os.environ.get("LINE_CHANNEL_SECRET")
bear = os.environ.get("LINE_CHANNEL_TOKEN")

app = Flask(__name__)

#mqtt
app.config['MQTT_BROKER_URL'] = "mqtt.eclipseprojects.io"
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 10  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
#topic = '3ZeDnU$/'

mqtt_client = Mqtt(app)
LINE_API = 'https://api.line.me/v2/bot/message/push'

@app.route("/callback", methods=['POST'])
def callback_function():
    i=0
    request_data = request.get_json()
    print(request_data)
    if 'events' in request_data:
        try:
            msg = request_data['events'][0]['message']['text']
        except:
            msg = "none"
        while True:
            print("msg : ", msg)
            publish_result = mqtt_client.publish('fr3oiltemp', msg)
            print(publish_result)
            if publish_result[0]==0:
                break
            i+=1
        
    elif 'ESP' in request_data:
        Authorization = 'Bearer {}'.format(bear)
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization':Authorization
        }
        data = {
            "to":"C9c7c2c3dbf0d0b116c86bc6af8e6c73e",
            "messages":[{
                "type":"text",
                "text":request_data['ESP']
            }]
        }
        data = json.dumps(data)
        r = requests.post(LINE_API, headers=headers, data=data)
        print(r)
        i=-1
    #return str(publish_result[0])
    return str(i)
    

if __name__ == "__main__":
    app.run()
