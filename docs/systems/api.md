---
title: API
parent: Systems
nav_order: 5
---

# API

| Method | Path | Description |
|---|---|---|
| GET | /wallet/print | Returns the wallets |
| GET | /wallet/change/<int:number> | Changes the currently wallet | 
| GET | /wallet/create/<password> | Creates a new wallet with the given password |
| GET | /wallet/delete | Deletes the currenly wallet |
| GET | /wallet/balance | Returns the balance of the currently wallet |
| GET | /send/coin/<address>/<amount>/<password> | Deletes the currenly wallet |
| GET | /node/start/<ip>/<port> | Starts a node server with the given ip and port |
| GET | /node/stop | Stops the node server |
| GET | /node/newunl/?<id> | Creates a new UNL node with given id |
| GET | /node/connect/<ip>/<port> | Connects to a node with the given ip and port |
| GET | /node/connectmixdb | Connects to a nodes in the mixdb |
| GET | /node/id | Returns the id of the node server |
| GET | /settings/test/on | Sets the test mode on |
| GET | /settings/test/off | Sets the test mode off |
| GET | /settings/debug/on | Sets the debug mode on |
| GET | /settings/debug/off | Sets the debug mode off |
| GET | /block/get | Gets block from other nodes |
