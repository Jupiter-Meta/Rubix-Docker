import requests

url = 'http://34.47.140.50:5050/api/createUserDIDwithDB'
num_requests = 500
print("start")
for i in range(num_requests):
    try:
        # Make a POST request to the API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # print(f'Request {i+1}: Success')
            pass
        else:
            print(f'Request {i+1}: Failed with status code {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'Request {i+1}: Failed due to error - {e}')

print('All requests completed.')
