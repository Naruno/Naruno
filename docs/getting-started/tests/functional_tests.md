---
title: Functional Tests
parent: Tests
grand_parent: Getting Started
nav_order: 2
---

# Functional Tests
Functional tests are check your system circulation. To run the functional tests, run the following command:

## Prerequisites
Before you begin, make sure you have the following:

```bash
mkdir test_enviroment
cd test_enviroment
git clone https://github.com/Decentra-Network/Decentra-Network.git
pip3 install pytest -y
```

## Running the Functional Tests
To run the functional tests, run the following command:

```bash
pytest Decentra-Network/tests/functional_tests
```