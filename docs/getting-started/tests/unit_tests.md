---
title: Unit Tests
parent: Test
grand_parent: Getting Started
nav_order: 1
---

# Unit Tests
Tests are a great way to verify that your installation is working as expected. In this section, we will run the Unit Tests.

## Prerequisites
Before you begin, make sure you have the following:

```bash
mkdir test_enviroment
cd test_enviroment
git clone https://github.com/Decentra-Network/Decentra-Network.git
pip3 install pytest -y
```

## Running the Unit Tests
To run the unit tests, run the following command:

```bash
pytest Decentra-Network/tests/unit_tests
```