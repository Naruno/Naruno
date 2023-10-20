## Naruno

Naruno is a lightning-fast, secure, and scalable blockchain that is able to create transaction proofs and verification via raw data and timestamp. We remove the archive nodes and lazy web3 integrations.

### Documentation

- [Getting Started](getting-started/index.md)
- [Concepts](docs/concepts/index.md)
- [Creating an App](docs/creating_a_app/index.md)
- [API Reference](docs/referances/apis.md)
- [CLI Reference](docs/referances/clis.md)
- [Release Notes](release-notes/index.md)
- [FAQ](faq.md)
- [Videos](docs/videos/baklavatestnet.py)

## Using the Naruno API

- [Using the Naruno API with requests](using_with_requests.md)
- [Using the Naruno API with requests](using_with_requests.md)
- [Using the Naruno API with urllib3](using_with_urllib3.md)

## Sending Requests to Authorization-Needed Endpoints

To send a request to authorization-needed endpoints using the Python requests library, you can follow these steps:

1. Import the `requests` library.
2. Prepare the necessary data for the request.
3. Send the request using the `requests` library.

Here's an example code snippet demonstrating how to send a GET request to an authorization-needed endpoint:

```python
import requests

response = requests.get('http://localhost:8000/authorization-needed-endpoint', auth=('username', 'password'))

if response.status_code == 200:
    # Request was successful
    data = response.json()
    print(data)
else:
    # Request failed
    print('Error:', response.status_code)
```

Replace `'http://localhost:8000/authorization-needed-endpoint'` with the actual URL of the authorization-needed endpoint you want to send a request to. Replace `'username'` and `'password'` with the actual credentials required for authentication.

Remember to handle any errors or exceptions that may occur during the request.