---
title: Stability
parent: Tests
grand_parent: Getting Started
nav_order: 3
---

# Stability Tests
Stability tests are check yoru system stability in different conditions with functional tests.

## Prerequisites
Before you begin, make sure you have the following:

```bash
mkdir test_enviroment
cd test_enviroment
git clone https://github.com/Decentra-Network/Decentra-Network.git
pip3 install pytest -y
```

## Running the Stability Tests
To run the stability tests, run the following command:

```bash
pytest Decentra-Network/tests/stability_tests
```