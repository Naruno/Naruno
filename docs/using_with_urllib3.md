## Using the Naruno API with urllib3

Welcome to the documentation on using the Naruno API with the `urllib3` library.

### Introduction

The Naruno API allows you to interact with the Naruno blockchain and perform various operations. This guide will walk you through the process of using the Naruno API with the `urllib3` library.

### Installing the `urllib3` library

Before you can start making API requests, you need to install the `urllib3` library. You can do this by running the following command:

```bash
pip install urllib3
```

### Making GET requests

To retrieve data from the Naruno blockchain, you can use the `urllib3` library's `GET` method. Here's an example of making a GET request to retrieve the latest block:

```python
import urllib3
import json

http = urllib3.PoolManager()

response = http.request('GET', 'http://localhost:8000/block/get')
if response.status == 200:
    block_data = json.loads(response.data.decode('utf-8'))
    print(block_data)
else:
    print('Error:', response.status)
```

### Making POST requests

To send data to the Naruno blockchain, you can use the `urllib3` library's `POST` method. Here's an example of making a POST request to send a transaction:

```python
import urllib3
import json

http = urllib3.PoolManager()

data = {
    'from_user': 'sender_address',
    'to_user': 'recipient_address',
    'amount': 10.0,
    'data': 'Transaction data',
    'password': 'sender_password'
}

response = http.request('POST', 'http://localhost:8000/send/', fields=data)
if response.status == 200:
    transaction_data = json.loads(response.data.decode('utf-8'))
    print(transaction_data)
else:
    print('Error:', response.status)
}

### Handling authentication

To authenticate your requests, you can include your credentials in the request headers. Here's an example of including basic authentication credentials:

```python
import urllib3
import base64
import json

http = urllib3.PoolManager()

url = 'http://localhost:8000/wallet/delete'
username = 'your_username'
password = 'your_password'
credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
headers = {'Authorization': f'Basic {credentials}'}

response = http.request('GET', url, headers=headers)
if response.status == 200:
    print('Success')
else:
    print('Error:', response.status)
}

### Additional resources

For more information on using the Naruno API and the `urllib3` library, you can refer to the following resources:

- [Naruno API Documentation](https://naruno-api-docs.com)
- [urllib3 Documentation](https://urllib3.readthedocs.io)