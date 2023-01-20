---
layout: default
title: Apps
nav_order: 10
parent: Concepts
---

# Apps

Decentra Network supports the development of apps. Apps are the main way to interact with the Decentra Network blockchain for development decentralized applications.

For this Decentra Network support two integration methods. The first one is embedded apps. This apps are included in Decentra Network concept system. The second one is remote apps. This apps are unning outside of Decentra Network and uses Decentra Network API for communication.

For integrating apps with Decentra Network you need to change send and get functions with Decentra Network.

## Send Function

Example you have a messaging application and you want to send a message to another user. And already you have a function for sending messages. Example with socket, for integrations with Decentra Network just your need changing the socket with our send function. We can handle the sending message to other users.

## Get Function

In above example the user that receiving the message is have a function with socket for getting the messages. For integration with Decentra Network user should changing the get function with our get function. We give the messages to the user.

```mermaid
flowchart LR
    subgraph Applications Functions
    subgraph user_1[User 1]
        subgraph APP_1
            send_1[Send Functions]
            get_1[Get Functions]
        end
    end

    subgraph Decentra Network
        send_d[Send Functions]
        get_d[Get Functions]
    end



    subgraph user_2[User 2]
        subgraph APP_2
            send_2[Send Functions]
            get_2[Get Functions]
        end
    end

    send_1 -- data_1 --> send_d
    get_d -- data_2 --> get_1

    send_2 -- data_1 --> send_d
    get_d -- data_2 --> get_2

end

```

## Embedded Apps

Embedded apps organized by our Apps engine. Apps engine is give basic and fast integration infrastructure for decentralized apps.

When a transaction is approved by the network, if this transaction's recipient is the user of Decentra Network installation the engine is start.

If the engine finds an app send the transaction to the app. The app can process the transaction for its own purpose. For example, the app can send a notification to the user.

Also apps can uses send transactions functions for sending datas.

## Remote Apps

Remote apps are running outside of Decentra Network. Remote apps can uses API for sending and getting data.

```mermaid
flowchart LR

subgraph Applications Environment
    direction LR

    subgraph Node_1 [Node 1]
        API_1[API]

        subgraph Embedded_Apps_1 [Embedded Apps]
            direction TB
            E1_1[App 1]
            E2_1[App 2]
            E3_1[App 3]
        end
        subgraph Remote_Apps_1 [Remote Apps]
            direction TB
            R1_1[App 4]
            R2_1[App 5]
            R3_1[App 6]
        end
        subgraph Decentra_Network_1 [Decentra Network]
            Embedded_Apps_1
        end

        Remote_Apps_1 --> API_1
        API_1 <--> Decentra_Network_1

    end

    subgraph Node_2 [Node 2]
        API_2[API]

        subgraph Embedded_Apps_2 [Embedded Apps]
            direction TB
            E1_2[App 1]
            E2_2[App 2]
            E3_2[App 3]
        end
        subgraph Remote_Apps_2 [Remote Apps]
            direction TB
            R1_2[App 4]
            R2_2[App 5]
            R3_2[App 6]
        end
        subgraph Decentra_Network_2 [Decentra Network]
            Embedded_Apps_2
        end

        Remote_Apps_2 --> API_2
        API_2 <--> Decentra_Network_2

    end


Node_1 <--data--> Node_2


end
```
