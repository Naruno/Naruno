---
title: APIs
parent: References
nav_order: 1
---

# Accessing to The API

In normal usage (api/main.py) the default host is 0.0.0.0 and port is 8000.

In auto_builders based instalation the host is 0.0.0.0 and port is
increase by node number. For example:

- 1st node port is 8000
- 2nd node port is 8101
- 3rd node port is 8102

# API Referance

| Method | Path                               | Description                                                         |
| ------ | ---------------------------------- | ------------------------------------------------------------------- |
| GET    | /wallet/print                      | Returns the wallets                                                 |
| GET    | /wallet/change/:number             | Changes the currently wallet                                        |
| GET    | /wallet/create/:password           | Creates a new wallet with the given password                        |
| GET    | /wallet/delete                     | Deletes the currenly wallet                                         |
| GET    | /wallet/balance                    | Returns the balance of the currently wallet                         |
| POST   | /send                              | Send coin, data with given addresss and password.                   |
| GET    | /node/start/:ip/:port              | Starts a node server with the given ip and port                     |
| GET    | /node/stop                         | Stops the node server                                               |
| GET    | /node/newunl/?:id                  | Creates a new UNL node with given id                                |
| GET    | /node/connect/:ip/:port            | Connects to a node with the given ip and port                       |
| GET    | /node/connectmixdb                 | Connects to a nodes in the mixdb                                    |
| GET    | /node/id                           | Returns the id of the node server                                   |
| GET    | /settings/test/on                  | Sets the test mode on                                               |
| GET    | /settings/test/off                 | Sets the test mode off                                              |
| GET    | /settings/debug/on                 | Sets the debug mode on                                              |
| GET    | /settings/debug/off                | Sets the debug mode off                                             |
| GET    | /block/get                         | Gets block from other nodes                                         |
| GET    | /transactions/sended/validated     | Returns sended validated transactions as json                       |
| GET    | /transactions/sended/not_validated | Returns sended not validated transactions as json                   |
| GET    | /transactions/received             | Returns received transactions as json                               |
| GET    | /transactions/all                  | Returns all transactions as json                                    |
| GET    | /export/transactions/csv           | Exports transactions to csv                                         |
| GET    | /status                            | Returns the status of network                                       |
| POST   | /proof/get/                        | Returns the given transaction proof from signature                  |
| POST   | /proof/check/                      | Returns the check result of given proof path                        |
| POST   | /block/get/                        | Returns the currently block as json                                 |
| POST   | /sign/                             | Signs and returns the signed data file from given data and password |
| POST   | /verify/                           | Return the verify result of given path of signed data               |

# Starting the API

For starting the API you should run the api/main.py file. If you use the [Automatic Building a Test Network](https://docs.naruno.net/building_a_test_network/automatic.html) you don't need to start API manually. The API will start automatically with the node.

Otherwise you can start the API with the following command:

```bash
python3 Decentra-Network/decentra_network/api/main.py
```

Also you can give the -p parameter for changing the port of the API. For example:

```bash
python3 Decentra-Network/decentra_network/api/main.py -p 8000
```

_If you use [Building a Test Network](https://docs.naruno.net/building_a_test_network/) you should change "Decentra-Network" to ex. "Decentra-Network-0"._
