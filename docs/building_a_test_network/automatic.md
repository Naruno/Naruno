---
title: Automatic
parent: Building a Test Network
nav_order: 1
---

# Building a Test Network [![Open in Cloud Shell](https://img.shields.io/badge/Open%20in%20Cloud%20Shell-Tutorial-5ec205)](https://ssh.cloud.google.com/cloudshell/open?shellonly=true&cloudshell_git_repo=https://github.com/Naruno/Naruno&cloudshell_tutorial=docs/building_test_network/automatic.md)
A test network can do all the things a production network can do, but it is not connected to the main Naruno. This means that you can test your code without worrying about affecting the main network. You can also use a test network to test your code in a controlled environment. And all is free and yours to use. So let's get started.

## Prerequisites
- Free 6 ports
- Phisical or virtual network connection for each node
- Safe place
- [Python >=3.8](https://www.python.org/downloads/)
- [git](https://git-scm.com/downloads)
- [pip](https://pip.pypa.io/en/stable/installing/)

## Step 1: Download the Naruno Source Code
In this steep we will download the Naruno source code. You can download the source code from master branch with the following command:
```bash
git clone https://github.com/Naruno/Naruno.git
mkdir test_network 
cp -r -f Naruno test_network/Naruno
```

## Step 2: Generating the Test network
In this steep we will generate 3 node and we will put them in the "test_network" folder. You can generate the nodes with the following command:
```bash
cd test_network
python3 Naruno/auto_builders/local.py -nn 3 -scn 1 -d -i -s -r
```

## Step 3: Testing the Circulation
If everything is ok, you can see and check the test network with the following command:

```bash
python3 Naruno-0/decentra_network/cli/main.py -s
```

If status is equal to "Working" there is no problem.