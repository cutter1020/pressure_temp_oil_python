from flask import Flask, request, jsonify
import os
import requests

secret = os.environ.get("LINE_CHANNEL_SECRET")
bear = os.environ.get("LINE_CHANNEL_TOKEN")

app = Flask(__name__)
LINE_API = 'https://api.line.me/v2/bot/message/push'
state = 0
command = ""

@app.route("/checkstate", methods=['GET'])
def checkState():
    global state
    return str(state)

@app.route("/getcommand", methods=['GET'])
def GetCommand():
    global command
    return str(command)

@app.route("/callback", methods=['POST'])
def callback_function():
    global state, command
    request_data = request.get_json()
    print(request_data)
    if 'events' in request_data:
        try:
            command = request_data['events'][0]['message']['text']
        except:
            command = "none"
        state+=1
        return command
        
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
        return str(1)

if __name__ == "__main__":
    app.run()
