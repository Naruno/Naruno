---
layout: default
title: Embedded
parent: Apps
grand_parent: Concepts
nav_order: 1
---

# Create

- Decentra-Network
  - apps
    - App_Name
      - app_name_main.py

# Explanation

Some definitions are required for the Main Software to recognize app.

**Note: Starred ones must be.**

# In app_name_main.py

## \* A Receiver for Approved Transactions

When a transaction is confirmed, the function here is triggered.

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import sys


def app_name_main_tx(tx):
    print("Data of the TX: "+str(tx.data))
    sys.exit()

```

You must use sys.exit() to exit the app when you are done.


# On github

## Git Clone

### Go to Apps Directory (Decentra-Network/decentra_network/apps)

`git clone github_link`
