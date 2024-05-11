'''
This module defines the behaviour of a client in your Chat Application
'''
import sys
import getopt
import socket
import random
from threading import Thread
import os
import util


'''
Write your code inside this class. 
In the start() function, you will read user-input and act accordingly.
receive_handler() function is running another thread and you have to listen 
for incoming messages in this function.
'''

class Client:
    '''
    This is the main Client Class. 
    '''
    def __init__(self, username, dest, port, window_size):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None)
        self.sock.bind(('', random.randint(10000, 40000)))
        self.name = username

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message. 
        Use make_message() and make_util() functions from util.py to make your first join packet
        Waits for userinput and then process it
        '''

        # Initial connection setup by sending a JOIN message.
        self.send_to_server("join", 1, self.name)

        while True:
            user_input = input().strip().split(' ')
            cmd = user_input[0]
            param = user_input[1:]

            # Command processing
            if cmd == "msg":
                self.handle_message_command(param)
            elif cmd == "list":
                self.send_to_server("request_users_list", 2)
            elif cmd == "help":
                self.print_help()
            elif cmd == "quit":
                self.handle_quit()
            else:
                print("incorrect userinput format")

    def send_to_server(self, message_type, message_format, data=""):
        #Constructs and sends a packet to the server based on the message type and data.
        msg = util.make_message(message_type, message_format, data)
        packet = util.make_packet(msg=msg)
        self.sock.sendto(packet.encode(), (self.server_addr, self.server_port))

    def handle_message_command(self, param):
        # Processes the 'msg' command to send messages to other clients through the server.
        user_num = int(param[0])
        user_list = param[1:user_num+1]
        message = " ".join(param[user_num+1:])
        data = f"{user_num} {' '.join(user_list)} {message}"
        self.send_to_server("send_message", 4, data)

    def print_help(self):
        # Displays help information about client commands.
        print("Client")
        print("-u username | --user=username The username of Client")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-w WINDOW_SIZE | --window=WINDOW_SIZE The window_size, defaults to 3")
        print("-h | --help Print this help")

    def handle_quit(self):
        # Processes the 'quit' command to disconnect from the server and exit the application.
        self.send_to_server("disconnect", 1, self.name)
        print("quitting")
        sys.exit(0)

    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''
         
        while True:
            message, addr = self.sock.recvfrom(2048)
            message = message.decode()
            pck_type, seqno, data, checksum = util.parse_packet(message)
            msg_type, data = data.split(' ', maxsplit=1)

            # Message handling based on type from server.
            if msg_type == "response_users_list":
                self.handle_user_list(data)
            elif msg_type == "forward_message":
                self.handle_forward_message(data)
            else:
                self.handle_error_message(msg_type)

    def handle_user_list(self, data):
        # Processes and prints a list of users sent by the server.
        data = data.split(' ')
        user_num = int(data[1])
        user_list = " ".join(data[2:user_num+2])
        print(f"list: {user_list}")

    def handle_forward_message(self, data):
        # Processes and displays messages forwarded by the server from other clients.
        data = data.split(' ')
        sender = data[2]
        message = " ".join(data[3:])
        print(f"msg: {sender}: {message}")

    def handle_error_message(self, msg_type):
        # Handles error messages from the server and closes the connection.
        error_messages = {
            "err_unknown_message": "server received an unknown command",
            "err_server_full": "server full",
            "err_username_unavailable": "username not available"
        }

        if msg_type in error_messages:
            self.sock.close()
            print(f"disconnected: {error_messages[msg_type]}")
            sys.exit(1)

            

# Do not change below part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our Client module completion
        '''
        print("Client")
        print("-u username | --user=username The username of Client")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-w WINDOW_SIZE | --window=WINDOW_SIZE The window_size, defaults to 3")
        print("-h | --help Print this help")
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "u:p:a:w", ["user=", "port=", "address=","window="])
    except getopt.error:
        helper()
        exit(1)

    PORT = 15000
    DEST = "localhost"
    USER_NAME = None
    WINDOW_SIZE = 3
    for o, a in OPTS:
        if o in ("-u", "--user="):
            USER_NAME = a
        elif o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a
        elif o in ("-w", "--window="):
            WINDOW_SIZE = a

    if USER_NAME is None:
        print("Missing Username.")
        helper()
        exit(1)

    S = Client(USER_NAME, DEST, PORT, WINDOW_SIZE)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
