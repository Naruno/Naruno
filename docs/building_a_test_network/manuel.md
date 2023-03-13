---
title: Manuel
parent: Building a Test Network
nav_order: 2
---

# Building a Test Network [![Open in Cloud Shell](https://img.shields.io/badge/Open%20in%20Cloud%20Shell-Tutorial-5ec205)](https://ssh.cloud.google.com/cloudshell/open?shellonly=true&cloudshell_git_repo=https://github.com/Naruno/Naruno&cloudshell_tutorial=docs/building_test_network/manuel.md)
A test network can do all the things a production network can do, but it is not connected to the main Naruno. This means that you can test your code without worrying about affecting the main network. You can also use a test network to test your code in a controlled environment. And all is free and yours to use. So let's get started.

## Prerequisites
- Free 6 ports
- Phisical or virtual network connection for each node
- Safe place for node 0
- [Python >=3.8](https://www.python.org/downloads/)
- [git](https://git-scm.com/downloads)

## Step 1: Download the Naruno Source Code
In this steep we will download the Naruno source code. You can download the source code from master branch with the following command:
```bash
git clone https://github.com/Naruno/Naruno.git
```
## Step 2: Generating the Nodes
In this steep we will generate 3 node and we will put them in the "test_network" folder. You can generate the nodes with the following command:
```bash
mkdir test_network
cp -r -f Naruno test_network/Naruno-0
cp -r -f Naruno test_network/Naruno-1
cp -r -f Naruno test_network/Naruno-2
cd test_network
```

## Step 3: Configuring the Nodes
Now we have unconfigured nodes. We need to configure them.

### Step 3.1: Configuring test mode of Node 0
We need to set `test` mode on for node 0
```bash
python3 Naruno-0/naruno/cli/main.py --testmodeon
```
### Step 3.2: Configuring debug mode of each node
And we should setting the `debug` mode off for each node because otherwise the node prints a lot of unnecessary information.
```bash
python3 Naruno-0/naruno/cli/main.py --debugmodeoff
python3 Naruno-1/naruno/cli/main.py --debugmodeoff
python3 Naruno-2/naruno/cli/main.py --debugmodeoff
```

### Step 3.3: Creating the wallets of each node
In Naruno we use password protected wallets. But for the first wallet we dont use password because first wallet is used for the node communication. So you must be in safe place for node 0. You can create the wallets with the following command:
```bash
python3 Naruno-0/naruno/cli/main.py --createwallet password
```
```bash
python3 Naruno-1/naruno/cli/main.py --createwallet password
```
```bash
python3 Naruno-2/naruno/cli/main.py --createwallet password
```

Now you can check your wallet with
```bash
python3 Naruno-0/naruno/cli/main.py --printwallet
``` 
command.


### Step 3.4: Configuring the UNL nodes for each node
Naruno nodes dont connect any stranger node. So we need to introduce our nodes to each other. 

First you need to get the ids of node 0, node 1 and node 2. You can get the ids with the following command:
```bash
python3 Naruno-0/naruno/cli/main.py --ndid
```
```bash
python3 Naruno-1/naruno/cli/main.py --ndid
```
```bash
python3 Naruno-2/naruno/cli/main.py --ndid
```

#### Step 3.4.1: Configuring the UNL nodes for Node 0
Now you can configure the UNL nodes for node 0 with the following command:
```bash
python3 Naruno-0/naruno/cli/main.py --ndnewunl node_1_id
python3 Naruno-0/naruno/cli/main.py --ndnewunl node_2_id
```

#### Step 3.4.2: Configuring the UNL nodes for Node 1
Now you can configure the UNL nodes for node 0 with the following command:
```bash
python3 Naruno-1/naruno/cli/main.py --ndnewunl node_0_id
python3 Naruno-1/naruno/cli/main.py --ndnewunl node_2_id
```

#### Step 3.4.3: Configuring the UNL nodes for Node 2
Now you can configure the UNL nodes for node 0 with the following command:
```bash
python3 Naruno-2/naruno/cli/main.py --ndnewunl node_0_id
python3 Naruno-2/naruno/cli/main.py --ndnewunl node_1_id
```

### Step 3.5: Starting the node protocol
Nodes are communicate over a tcp socket. So we need to start the node protocol for each node. But now we must switch to menu menu of each node. Because the node protocol and its connections are a thread. we need to be in same thread for some communication operations.

You can switch to menu for node 0, node 1 and node 2 with the following command:
```bash
python3 Naruno-0/naruno/cli/main.py --menu
```
switch another terminal and run:
```bash
python3 Naruno-1/naruno/cli/main.py --menu
```
switch another terminal and run:
```bash
python3 Naruno-2/naruno/cli/main.py --menu
```


Okey, let's start nodes via menu of each node. You can start the node protocol with the followings:

- Menu Of Node 0:
Type `ndstart` and enter 0.0.0.0 as ip and 7999 as port.

- Menu Of Node 1:
Type `ndstart` and enter 0.0.0.0 as ip and 8011 as port.

- Menu Of Node 2:
Type `ndstart` and enter 0.0.0.0 as ip and 8012 as port.



## Step 4: Connecting the nodes
Now we have configured and started the nodes. before the last step we need to connect the nodes. Use the followings:

- Menu Of Node 0:
Type `ndconnect` and enter 0.0.0.0 as ip and 8011 as port.
- Menu Of Node 0:
Type `ndconnect` and enter 0.0.0.0 as ip and 8012 as port.
- Menu Of Node 1:
Type `ndconnect` and enter 0.0.0.0 as ip and 8012 as port.

## Step 5: Starting the Circulation
Now we are ready for the launch. As you can remember the node 0 have a test mode. So we need to start the circulation by node 0 following command:

- Menu Of Node 0:
Type `getblock` and enter

## Step 6: Testing the Circulation
If everything is ok, you can see and check the test network with the following command:

- Menu Of Node 0:
Type `status` and enter

If status is equal to "Working" there is no problem.
