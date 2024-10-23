#!/usr/bin/python3
from flask import Flask, request, jsonify, Response
import requests,json, time, sys
from flask_cors import CORS
import json
import os, subprocess

current_directory = os.getcwd()
print("Current Directory:", current_directory)

# os.chdir(current_directory+"/..")
home_directory = "/app"
# print(home_directory)

app = Flask(__name__)
CORS(app)


def get_mnemonic_content(did):
            path = home_directory
            path = "/app"
            #Testnet
            mnemonic_path = os.path.join(path, 'node1', 'Rubix', did, 'mnemonic.txt')
            #Mainnet
            # mnemonic_path = os.path.join(path, 'node1', 'Rubix', did, 'mnemonic.txt')
            if os.path.exists(mnemonic_path):
                with open(mnemonic_path, 'r') as file:
                    content = file.read().split()
                return content
            else:
                return None

# Home
@app.route('/', methods=['GET'])
def home():
	return "Hello"

#CreateDID Child API
@app.route('/api/createUserDID', methods=['GET'])
def createbibdid():
    print("create child BIB DID API")
    port=20002
    didpeerid = {}
    # for i in range (1):
    try:
        # Define the API endpoint URL
        url = "http://localhost:20000/api/createdid"
        files = {'did_config': (None, '{"type": 4, "priv_pwd": "mypassword"}'),}
        headers = {}

        # for i in range(1):
        try:
            # response = requests.post(url, data=form_data, files=files)
            response = requests.post(url, headers=headers, files=files)
            # print(response.text)
    # Check the response status code
            if response.status_code == 200:
                message = json.loads(response.text)
                
                if message['status'] == True:
                    did = message['result']['did']
                    peerid = message['result']['peer_id']

                    didpeerid={'status':True,
                           'did':did,
                           'peerid':peerid,
                           }
                    content = get_mnemonic_content(did)
                    if content:
                        didpeerid['Mnemonic'] = content

                    else:
                        didpeerid["Mnemonic"] = "mnemonic.txt not found"

                    return jsonify(didpeerid)
                else:
                    return "Failed to create DID"
        except Exception as e:
             return f"Failed to create DID - error in rubix node, {e}"
    except Exception as e:
        return f"Failed to create DID - error connecting to rubix node, {e}"
        
		
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
