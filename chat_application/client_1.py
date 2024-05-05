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
        self.window_size = window_size
        self.running = True

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message. 
        Use make_message() and make_util() functions from util.py to make your first join packet
        Waits for userinput and then process it
        '''
        join_message = util.make_packet("join", 0, self.name)
        self.sock.sendto(join_message.encode(), (self.server_addr, self.server_port))
        
        print("Type 'help' for a list of commands.")
        while self.running:
            try:
                msg = input()
                if msg.startswith("quit"):
                    self.send_quit()
                    break
                elif msg.startswith("list"):
                    self.request_users_list()
                elif msg.startswith("msg"):
                    if self.validate_message_command(msg):
                        self.send_message(msg)
                    else:
                        print("Incorrect message format. Usage: msg <number_of_users> <username1> ... <message>")
                elif msg.startswith("help"):
                    self.print_help()
                else:
                    print("Unknown command. Type 'help' for a list of valid commands.")
            except KeyboardInterrupt:
                self.send_quit()
            

    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''
        while self.running:
            try:
                data, _ = self.sock.recvfrom(1024)
                message = data.decode('utf-8')
                msg_type, seqno, content, checksum = util.parse_packet(message)
                if util.validate_checksum(message):
                    if "error" in msg_type:
                        print(f"Error from server: {content}")
                        self.running = False  # Stop the client if username is unavailable
                        self.sock.close()
                        break
                    else:
                        print(content)  # Display the received message with the sender info
                else:
                    print("Received corrupted message")
            except socket.error as e:
                if not self.running:
                    continue
                else:
                    print("Socket error:", e)
    
    def validate_message_command(self, msg):
        parts = msg.split()
        if len(parts) < 3:
            return False
        try:
            int(parts[1])  # This checks if the number of users is an integer
            return True
        except ValueError:
            return False

    def send_message(self, msg):
        _, num_users, *rest = msg.split()
        num_users = int(num_users)
        message = ' '.join(rest[num_users:])
        usernames = rest[:num_users]
        formatted_message = ' '.join([str(num_users)] + usernames + [message])
        packet = util.make_packet("msg", 0, formatted_message)
        self.sock.sendto(packet.encode(), (self.server_addr, self.server_port))

    def request_users_list(self):
        packet = util.make_packet("list", 0, "")
        self.sock.sendto(packet.encode(), (self.server_addr, self.server_port))

    def send_quit(self):
        disconnect_msg = util.make_packet("disconnect", 0, self.name)
        self.sock.sendto(disconnect_msg.encode(), (self.server_addr, self.server_port))
        self.running = False  # Set running flag to False to stop the receiver thread
        self.sock.close()
        print(f"{self.name} disconnected.")

    def print_help(self):
        print("Available commands:")
        print("  msg <number_of_users> <username1> <username2> ... <message> - Send a message.")
        print("  list - Request a list of connected users.")
        print("  quit - Quit the chat application.")
        print("  help - Print this help message.")



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
