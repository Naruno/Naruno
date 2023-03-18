---
layout: default
title: Apps
nav_order: 10
parent: Concepts
---

# Apps

Naruno supports the development of apps. Apps are the main way to interact with the Naruno blockchain for development decentralized applications.

For this Naruno support two integration methods. The first one is embedded apps. This apps are included in Naruno concept system. The second one is remote apps. This apps are unning outside of Naruno and uses Naruno API for communication.

For integrating apps with Naruno you need to change send and get functions with Naruno.

## Send Function

Example you have a messaging application and you want to send a message to another user. And already you have a function for sending messages. Example with socket, for integrations with Naruno just your need changing the socket with our send function. We can handle the sending message to other users.

## Get Function

In above example the user that receiving the message is have a function with socket for getting the messages. For integration with Naruno user should changing the get function with our get function. We give the messages to the user.

```mermaid
flowchart TB
    subgraph Applications Functions
        subgraph user_1[User 1]
            subgraph APP_1
                send_1[Send Functions]
                get_1[Get Functions]
            end


            subgraph dn1[Naruno 1]
                send_d1[Send Functions]
                get_d1[Get Functions]

            end
        end




        subgraph user_2[User 2]
            subgraph dn2[Naruno 2]
                send_d2[Send Functions]
                get_d2[Get Functions]
            end
            subgraph APP_2
                send_2[Send Functions]
                get_2[Get Functions]
            end

        end

        send_1 -- data_1 --> send_d1
        get_d1 -- data_2 --> get_1

        send_2 -- data_2 --> send_d2
        get_d2 -- data_1 --> get_2


        user_1 --- Naruno[Naruno] --- user_2


    end


```

## Remote Apps

Remote apps are running outside of Naruno. Remote apps can uses API for sending and getting data.

```mermaid
flowchart LR

subgraph Applications Environment
    direction LR

    subgraph Node_1 [Node 1]
        API_1[NARUNO API]


        subgraph Remote_Apps_1 [Remote Apps]
            direction TB
            R1_1[App 4]
            R2_1[App 5]
            R3_1[App 6]
        end


        Remote_Apps_1 <--> API_1


    end

    subgraph Node_2 [Node 2]
        API_2[NARUNO API]


        subgraph Remote_Apps_2 [Remote Apps]
            direction TB
            R1_2[App 4]
            R2_2[App 5]
            R3_2[App 6]
        end


        Remote_Apps_2 <--> API_2


    end


Node_1 <--data--> Node_2


end
```
