#!/usr/bin/python3
from flask import Flask, request, jsonify, Response
import requests,json, time, sys
from flask_cors import CORS
import json
import os, subprocess
from redirectToken import generate_token
from pymongo import MongoClient

client = MongoClient('mongodb+srv://jmRubix:JupiterMeta%40jmRubix@jm-rubix.qmlx6.mongodb.net/')
db = client['jmdidtable']
collection = db['irctcusers']


current_directory = os.getcwd()
print("Current Directory:", current_directory)

# os.chdir(current_directory+"/..")
home_directory = "/Rubix-Docker"
print(home_directory)

app = Flask(__name__)
CORS(app)


def dbWrite(data):
      try:
        collection.insert_one(data)
        return 1
      except:
           return 0

def get_mnemonic_content(did):
            path = home_directory
            path = "/home/saishibu/Rubix-Docker/rubix"
            #Testnet
            # mnemonic_path = os.path.join(path, 'node1', 'Rubix', 'TestNetDID', did, 'mnemonic.txt')
            #Mainnet
            mnemonic_path = os.path.join(path, 'node1', 'Rubix', did, 'mnemonic.txt')
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
        # print(elapsed_time)
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
                # print(didpeerid)
                return jsonify(didpeerid)
             else:
                # print(message)
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
        # print(elapsed_time)
    # Check the response status code
        if response.status_code == 200:
        # Request was successful
            message = json.loads(response.text)
            if message['status'] == True:
                # print(message['result']['did'])
                # print(message['result']['peer_id'])
                didpeerid={'status':True,
                           'did':message['result']['did'],
                           'peerid':message['result']['peer_id'],
                           'timeTaken':elapsed_time}
                # Remove the _id field if it exists
                return jsonify(didpeerid)
            else:
                # print(message)
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
                
@app.route('/api/createUserDIDwithDB', methods=['GET'])
def createbibdidDB():
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
                    dbWrite(didpeerid)
                    if '_id' in didpeerid:
                        didpeerid.pop('_id')    
                    return jsonify(didpeerid)
                else:
                    return "Failed to create DID"

@app.route('/api/createUserDID2', methods=['GET'])
def MakeType4DID():
    # try:
    for i in range(1):
        path = current_directory
        # print(path)
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
    url = 'http://172.28.57.14:5050/fetchtxn'
    payload = {
    'size': size 
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return jsonify({"error":{"status":response.status_code, "response":response.text}})

@app.route('/fetchattr', methods=['POST'])
def fetchattr():
    size = int(request.json.get('size'))
    url = 'http://172.28.57.14:5050/fetchattr'
    payload = {
    'size': size 
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return jsonify({"error":{"status":response.status_code, "response":response.text}})

@app.route('/writeattr', methods=['POST'])
def writeattr():
    data = request.get_json()
    url = 'http://172.28.57.14:5050/writeattr'
    
    # Extract data from JSON payload
    payload = {
        "UserID": data.get('UserID'),
        "DID": data.get('DID'),
        "Attributes": data.get('Attributes'),
        "Keywords": data.get('Keywords'),
        "isOnboarded": data.get('isOnboarded')
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return jsonify({"error":{"status":response.status_code, "response":response.text}})


##INSIGHTINTELLIGENCE-WEBURLHANDLER

@app.route('/getUserID', methods=['POST'])
def home1():

	userID = request.json["userId"]
	
	table = ["IRCTC1"]
	userData = {}

	auth_url = "https://devapi.insightengine.in/v2/web/web_auth"
	if userID in table:
		userData["did"] ="bafy"
		redirect_token = generate_token(userID,userData["did"])
		userData["redirect_token"] = redirect_token
	else:
		api_url = "http://34.47.131.10:5050//api/createUserDID"
		response = requests.get(api_url)
		if response.status_code == 200:
			response_data = response.json()  # Assuming response is a dictionary
			userData={
				"did":response_data["did"],
				"peerID":response_data["peerid"],
				"Mnemonic":response_data["Mnemonic"],	
            }
			redirect_token = generate_token(userID,userData["did"])
			userData["redirect_token"] = redirect_token 
		else:
			userData["did"] = None
	userData["userId"] = userID
	userData["platform"] = "iOS"
	userData["bussiness-id"] = "660a7e6725e206f03c2c9dd0"
	userData["merchant-id"] = "irctc"
	auth_response = requests.post(auth_url, json=userData)
	print(userData)
	if auth_response.status_code == 200:
		return jsonify({"status":"true", "message":"auth success","url":f"https://irctc.insightengine.in?redirect_token={redirect_token}"})
	else:
		return jsonify({"status":"false", "message":"auth failed"})
     

@app.route('/getUserIDFWD', methods=['POST'])
def getUserIDFWD():
    userData = {
         "userID" : request.json["userId"]
    }
    
    auth_url = "http://103.116.163.61/getUserDB"
    auth_response = requests.post(auth_url, json=userData)
    if auth_response == 200:
         return jsonify({"status":"true", "message":"auth success","url":f"https://irctc.insightengine.in?redirect_token="})
    else:
         return jsonify({"status":"false", "message":"auth failed"})


@app.route('/db/fetchtxn', methods=['POST'])
def fetchtxn2():
     userData = {
          "sizes":int(request.json['sizes'])
     }
     
     url = "http://172.30.72.15:5050/fetchtxn"
     auth_response = requests.post(url, json=userData)
     if auth_response == 200:
        return jsonify({"status": True, "response": auth_response})
     else:
        return jsonify({"status": False, "response": auth_response})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
