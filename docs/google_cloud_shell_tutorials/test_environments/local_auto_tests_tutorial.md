# Local Test Environments Tutorial

## Duplicating The Decentra Network Core
First we will replicate the already installed Decentra Network Core.

```bash
cd ..
```

```bash
cp -r Decentra-Network Decentra-Network-2
```
```bash
cp -r Decentra-Network Decentra-Network-3
```

## Running The Core 1

```bash
python3 Decentra-Network/src/api.py
```
<walkthrough-footnote>Local Test Environments Tutorial</walkthrough-footnote>

## Running The Core 2
Open new terminal.
```bash
python3 cloudshell_open/Decentra-Network-2/src/api.py -p 8010
```
<walkthrough-footnote>Local Test Environments Tutorial</walkthrough-footnote>

## Running The Core 3
Open new terminal.
```bash
python3 cloudshell_open/Decentra-Network-3/src/api.py -p 8020
```
<walkthrough-footnote>Local Test Environments Tutorial</walkthrough-footnote>

## Running The Auto Tests
Finaly open new terminal and we run our automated test tool, it sets up and tests the network for us.

```bash
python3 cloudshell_open/Decentra-Network/test_environments/local/test_decentra_network_local.py
```
<walkthrough-footnote>Local Test Environments Tutorial</walkthrough-footnote>
## Conclusion
<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>



<walkthrough-footnote>Local Test Environments Tutorial</walkthrough-footnote>
