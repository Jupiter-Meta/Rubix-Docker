#!/usr/bin/python3
from flask import Flask, request, jsonify, Response
import requests,json, time, sys
from flask_cors import CORS
import json
import os, subprocess

current_directory = os.getcwd()
# print("Current Directory:", current_directory)

os.chdir(current_directory+"")

app = Flask(__name__)
# CORS(app)

def get_mnemonic_content(did):
            path = "/app/rubix"
            mnemonic_path = os.path.join(path, 'node1', 'Rubix', 'TestNetDID', did, 'mnemonic.txt')
            if os.path.exists(mnemonic_path):
                with open(mnemonic_path, 'r') as file:
                    content = file.read()
                return content
            else:
                return None

# Home
@app.route('/', methods=['GET'])
def home():
	return "Hello"

@app.route('/api/getalldid', methods=['GET'])
def getalldid():
    alldidurl = f'http://localhost:20000/api/getalldid'
    alldid = requests.get(alldidurl).text
    return (json.loads(alldid))

@app.route('/api/createparentdid', methods=['GET'])
def createParentDID():
    print("create ParentDID API")
    start_time = time.time()


    # Get the port based on user input; use the default if not found in the dictionary
    port = 20000

    # Define the API endpoint URL
    url = f'http://localhost:{port}/api/createdid'
    
    # Create a dictionary for form data
    form_data = {'did_config': (None, '{"type":0,"dir":"","config":"","master_did":"","secret":"My DID Secret","priv_pwd":"mypassword","quorum_pwd":"mypassword"}'),}

    # Specify the file to upload
    files = {'img_file': ('/app/middleware/image.png', open(r'/app/middleware/image.png', 'rb'), 'image/png')}

# Send a POST request with multipart/form-data
    try:
        response = requests.post(url, data=form_data, files=files)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)
    # Check the response status code
        if response.status_code == 200:
             message = json.loads(response.text)
             if message['status'] == True:
                did = message['result']['did']
                peerid = message['result']['peer_id']
                didpeerid={'status':True,
                           'createTime':end_time,
                           'port':port,
                           'did':did,
                           'peerid':peerid,
                           'timeTaken':elapsed_time,
                           }
                print(didpeerid)
                return jsonify(didpeerid)
             else:
                print(message)
                return message
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        return (str(e))
    
#CreateDID Child API
@app.route('/api/createchilddid', methods=['GET'])
def createchildDID():
    print("create childDID API")

    # Get the port based on user input; use the default if not found in the dictionary
    port = 20000

    # Check if the user input is not recognized
    start_time = time.time()
    # Define the API endpoint URL
    url = f'http://localhost:{port}/api/createdid'

    # Create a dictionary for form data
    formstring = '{"type":3,"dir":"","config":"","master_did":"","secret":"My DID Secret","priv_pwd":"mypassword","quorum_pwd":"mypassword"}'
    formstring = json.loads(formstring)
    formstring['master_did'] = "bafybmihbqvwytabrio4pswssjxteugbbgip32tnagtbuqgrzthsjpvwuza"
    formstring = json.dumps(formstring)
    form_data = {'did_config': (None, formstring)}

    # Specify the file to upload
    files = {'img_file': ('/app/middleware/image.png', open(r'/app/middleware/image.png', 'rb'), 'image/png')}

# Send a POST request with multipart/form-data
    try:
        response = requests.post(url, data=form_data, files=files)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)
    # Check the response status code
        if response.status_code == 200:
        # Request was successful
            message = json.loads(response.text)
            if message['status'] == True:
                print(message['result']['did'])
                print(message['result']['peer_id'])
                didpeerid={'status':True,
                           'did':message['result']['did'],
                           'peerid':message['result']['peer_id'],
                           'timeTaken':elapsed_time}
                # Remove the _id field if it exists
                return jsonify(didpeerid)
            else:
                print(message)
                return message
        else:
            print(f"POST request failed with status code {response.status_code}")
            print("Response content:", response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        return (str(e))

#CreateDID Child API - Doesnt work
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
            print(response.text)
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

@app.route('/api/createUserDID2', methods=['GET'])
def MakeType4DID():
    # try:
    for i in range(1):
        path = current_directory
        print(path)
        os.chdir("/app/rubix")

        command = "./rubixgoplatform createdid -testNet -didType 4"
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(process)
        stderr_lines = process.stderr.decode('utf-8').splitlines()

        DIDs = set()
        for line in stderr_lines:
            if 'DID' in line:
                words = line.split()
                for i, word in enumerate(words):
                    if word == 'DID':
                        did = words[i + 1] 
                        DIDs.add(did)
                        break

        mnemonic_contents = {
            "DID":"",
            'Mnemonic':""
        }
        for did in DIDs:
            content = get_mnemonic_content(did)
            if content:
                mnemonic_contents["DID"] = did
                mnemonic_contents['Mnemonic'] = content
            else:
                mnemonic_contents[did] = "mnemonic.txt not found"

        return jsonify(mnemonic_contents), 200

    # except Exception as e:
        # return jsonify({'error': str(e)}), 500

@app.route('/api/testallnodes', methods=['GET'])
def testAllNodes():
#Ping to nodes and test
    node_statuses = {"node1":1}
    return jsonify(node_statuses)   		

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
