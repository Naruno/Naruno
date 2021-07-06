# Opening


## CLI Mode
If you want to use the CLI, you should open the "src/cli.py".

`python3 src/cli.py`

## GUI Mode
If you want to use the CLI, you should open the "src/gui.py".

`python3 src/gui.py`


# Creating the Wallet
Wallets are background of your address. Wallets consist of two parts: **pubkey** and **privatekey**.
You can share your pubkey, but privatekey is private. Wallets are stored in a file named "wallet_list.decentra_network". Wallets are encrypted and saved with your password.
## CLI Mode
Write `cw` and press enter.
## GUI Mode
Click "Create Wallet" button.

# Starting the P2P Server
Before connecting to other nodes, you need to start the local P2P server.
## CLI Mode
Write `ndstart` and press enter.
## GUI Mode
Click "Start Node Server" button in node page.

# Getting The id Of Your Node
## CLI Mode
Write `ndid` and press enter.
## GUI Mode
Click "Copy node id" button in node page.

# Adding the UNL Node
## CLI Mode
Write `ndnewunl` and write id of unl and press enter.
## GUI Mode
Click "Add New UNL" button and write id of unl and press OK.

# Connect to Other Nodes
Connection request of non-unl nodes is not accepted
## CLI Mode
Write `ndconnect` and press enter.
## GUI Mode
Click "Connect Node" button.