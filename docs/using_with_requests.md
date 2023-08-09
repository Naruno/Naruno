## Using the Naruno API with requests

Welcome to the documentation on using the Naruno API with the `requests` library.

### Introduction

The Naruno API allows you to interact with the Naruno blockchain and perform various operations. This guide will walk you through the process of using the Naruno API with the `requests` library.

### Installing the `requests` library

Before you can start making API requests, you need to install the `requests` library. You can do this by running the following command:

```bash
pip install requests
```

### Making GET requests

To retrieve data from the Naruno blockchain, you can use the `requests.get()` method. Here's an example of making a GET request to retrieve the latest block:

```python
import requests

response = requests.get('http://localhost:8000/block/get')
if response.status_code == 200:
    block_data = response.json()
    print(block_data)
else:
    print('Error:', response.status_code)
}

### Making POST requests

To send data to the Naruno blockchain, you can use the `requests.post()` method. Here's an example of making a POST request to send a transaction:

```python
import requests

data = {
    'from_user': 'sender_address',
    'to_user': 'recipient_address',
    'amount': 10.0,
    'data': 'Transaction data',
    'password': 'sender_password'
}

response = requests.post('http://localhost:8000/send/', data=data)
if response.status_code == 200:
    transaction_data = response.json()
    print(transaction_data)
else:
    print('Error:', response.status_code)
}

### Handling authentication

To authenticate your requests, you can include your credentials in the request headers. Here's an example of including basic authentication credentials:

```python
import requests

url = 'http://localhost:8000/wallet/delete'
auth = ('username', 'password')

response = requests.get(url, auth=auth)
if response.status_code == 200:
    print('Success')
else:
    print('Error:', response.status_code)
}

### Additional resources

For more information on using the Naruno API and the `requests` library, you can refer to the following resources:

- [Naruno API Documentation](https://naruno-api-docs.com)
- [Requests Library Documentation](https://requests.readthedocs.io)
import requests

response = requests.get('http://localhost:8000/block/get')
if response.status_code == 200:
    block_data = response.json()
    print(block_data)
else:
    print('Error:', response.status_code)
}

### Additional resources

For more information on using the Naruno API and the `requests` library, you can refer to the following resources:

- [Naruno API Documentation](https://naruno-api-docs.com)
- [Requests Library Documentation](https://requests.readthedocs.io)