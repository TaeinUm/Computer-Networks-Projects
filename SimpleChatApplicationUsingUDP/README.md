# Simple Chat Application Using UDP
#### Taein Um




## Overview
This project implements a basic chat application using UDP, a transport protocol that does not ensure reliable communication. The application consists of a server and multiple clients that can send and receive messages through the server.


## Components
- **Application-Server**: A single-threaded server that listens for new client connections, handles messages from clients, and manages up to a specified maximum number of clients.
- **Application-Client**: A client interface for the chat application that connects to the server with a unique username, sends messages to other clients, and receives messages from the server.


## Features
- **Join the chat**: Clients can join the chat by connecting to the server with a unique username.
- **Send messages**: Clients can send messages to one or more other clients.
- **List users**: Clients can list all active users in the chat.
- **Help**: Clients can view the available commands.
- **Quit**: Clients can gracefully disconnect from the server.


## Technologies Used
- **Language**: `Python`
- **Libraries**:
    - `getopt`: Parses command-line options and arguments.
    - `socket`: Provides access to the BSD socket interface.
    - `random`: Implements pseudo-random number generators for various distributions.
    - `threading`: Constructs higher-level threading interfaces.
    - `Thread`: Provides a way to create and manage new threads.




## Usage

### Running the server
Start the server using the following command:<br>
```sh
python3 server_1.py -p <port_number>
```

### Running the Client
Start a client with a unique username:<br>
```sh
python3 client_1.py -p <server_port_number> -u <username>
```

### Commands
- **Send Message**: msg <number_of_users> <username1> <username2> ... <message>
- **List Users**: list
- **Help**: help
- **Quit**: quit




## Testing
To test your implementation of Part 1, use the provided test script.<br>
```sh
python3 tests/TestPart1.py
```




## Contact Information
- Name: Taein Um
- Email: taeindev@gmail.com
- LinkedIn: https://www.linkedin.com/in/taein-um-00b14916b/
