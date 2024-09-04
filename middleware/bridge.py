#!/usr/bin/python3
from flask import Flask, request, jsonify, Response
import requests,json, time, sys
from flask_cors import CORS
import json
import os, subprocess
from dbConnect import fetchUserTransactions, fetchUserAttributes, fetchUserTransactionswithID, fetchUserAttributeswithID



current_directory = os.getcwd()
print("Current Directory:", current_directory)

# os.chdir(current_directory+"/..")
home_directory = "/Rubix-Docker"
print(home_directory)

app = Flask(__name__)
CORS(app)


def get_mnemonic_content(did):
            path = home_directory
            path = "/Rubix-Docker/rubix"
            #Testnet
            mnemonic_path = os.path.join(path, 'node1', 'Rubix', 'TestNetDID', did, 'mnemonic.txt')
            #Mainnet
            # mnemonic_path = os.path.join(path, 'node1', 'Rubix', did, 'mnemonic.txt')
            if os.path.exists(mnemonic_path):
                with open(mnemonic_path, 'r') as file:
                    content = file.read().split()
                return content
            else:
                return None

def ping_peer(peer_id):
    os.chdir(home_directory+"/rubix")
    # os.chdir("/Users/saishibunb/Downloads/rubixgoplatform-v0.0.17-darwin-amd64/")
    command = './rubixgoplatform ping -peerID ' + peer_id
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output1 = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
        print(output1)
        if '[ERROR]' in output1:
            return 0
        else:
	        return 1
    
    except subprocess.CalledProcessError as e:
        return f"Ping failed: {e.stderr}"


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
    for i in range (1):
    # try:
        # Define the API endpoint URL
        url = "http://localhost:20000/api/createdid"
        files = {'did_config': (None, '{"type": 4, "priv_pwd": "mypassword"}'),}
        headers = {}

        for i in range(1):
        # try:
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
                

@app.route('/api/healthcheck', methods=['POST'])
def testAllNodes():
#Ping to nodes and test
    # peer_id = ["12D3KooWQeswhUUofgvrKufuKRqT65y1WCojMaHcx5b9UzyNSW9V","12D3KooWCw9ZoG5q1fahS6NoEpj1BXea7yzR6f5NepbmJjtfSJca"]
    data = request.get_json()
    peer_id = data.get('peer_id', [])
    statuses=[]
    for peerid in peer_id:
        output = ping_peer(peerid)
        statuses.append(output)
    return jsonify(statuses)   	

@app.route('/status', methods=['GET'])
def testAllNodes2():
    return jsonify({"status":"ok"})  	

##DBHANDLER
@app.route('/fetchtxn', methods=['POST'])
def fetchtxn():
    size = int(request.json.get('size'))
    response = fetchUserTransactions(size)
    return response

@app.route('/fetchattr', methods=['POST'])
def fetchattr():
    size = int(request.json.get('size'))
    response = fetchUserAttributes(size)
    return response

@app.route('/fetchtxnwithuserid', methods=['POST'])
def fetchtxnwithuserid():
    userId = (request.json.get('userId'))
    response = fetchUserTransactionswithID(userId)
    return response

@app.route('/fetchattrwithuserid', methods=['POST'])
def fetchattrwithuserid():
    userId = (request.json.get('userId'))
    response = fetchUserAttributeswithID(userId)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
