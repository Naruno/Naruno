---
title: CLIs
parent: References
nav_order: 2
---

# CLI Arguments

| Short Usage  | Long Usage             | Parameters        | Description                                    |
| ------------ | ---------------------- | ----------------- | ---------------------------------------------- |
| -pw          | --printwallet          | NO                | Print wallets                                  |
| -w           | --wallet               | int:number        | Changeg the currently wallet with given number |
| -cw          | --createwallet         | NO                | Creates wallet                                 |
| -dw          | --deletewallet         | NO                | Deletes wallet                                 |
| -gb          | --getbalance           | NO                | Prints the balance of currently wallet         |
| -ndnunl      | --ndnewunl             | str:id            | Adds new unl node with given id                |
| -ndid        | --ndid                 | NO                | Prints the id of node server                   |
| -tmon        | --testmodeon           | NO                | Sets the test mode on                          |
| -tmoff       | --testmodeoff          | NO                | Sets the test mode off                         |
| -dmon        | --debugmodeon          | NO                | Sets the debug mode on                         |
| -dmoff       | --debugmodeoff         | NO                | Sets the test mode off                         |
| -exptrcsv    | --exporttransactioncsv | NO                | Exports transactions to csv                    |
| -returntrans | --returntransactions   | NO                | Prints transactions                            |
| -st          | --status               | NO                | Prints the status of network                   |
| -m           | --menu                 | NO                | Opens the cli menu                             |
| -gp          | --getproof             | str:signature     | Get proof of given transaction signature       |
| -cp          | --checkproof           | str:path_of_proof | Checks the given proof                         |

| -dnexport          | --dnexport           | NO | Backup and export the DB                         |
| -dnimport          | --dnimport           | str:path_of_backup_file | Imports the DB from given backup file                         |