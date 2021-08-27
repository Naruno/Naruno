---
title: Definition For App
parent: Embedded
grand_parent: Apps
nav_order: 3
---

# Explanation
Some definitions are required for the Main Software to recognize app.

**Note: Starred ones must be.**
# In app_name_main.py
## * A Receiver for Approved Transactions
When a transaction is confirmed, the function here is triggered.
```python
def app_name_main_tx(tx):
    print("Data of the TX: "+str(tx.data))
```
