'''
This module defines the behaviour of server in your Chat Application
'''
import sys
import getopt
import socket
import util


class Server:
    '''
    This is the main Server Class. You will  write Server code inside this class.
    '''
    def __init__(self, dest, port, window):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))
        self.clients = {}
        self.window = window
        self.MAX_NUM_CLIENTS = 10

    def start(self):
        '''
        Main loop.
        continue receiving messages from Clients and processing it.

        '''
        print("Server is starting on {} at port {}".format(self.server_addr, self.server_port))
        try:
            while True:
                data, addr = self.sock.recvfrom(1024)  # Buffer size is 1024 bytes
                self.handle_client(data, addr)
        except KeyboardInterrupt:
            self.shutdown_server()

    def handle_client(self, data, addr):
        try:
            msg_type, seqno, message, checksum = util.parse_packet(data.decode('utf-8'))
            if not util.validate_checksum(data.decode('utf-8')):
                raise ValueError("Invalid checksum")
            
            if msg_type == "join":
                self.handle_join(message, addr)
            elif msg_type == "msg":
                self.route_message(message, addr)
            elif msg_type == "list":
                self.send_user_list(addr)
            elif msg_type == "disconnect":
                self.handle_disconnect(message, addr)
            else:
                raise ValueError("Unknown command")
        except ValueError as e:
            error_msg = f"Error: {str(e)}"
            self.send_error_message(error_msg, addr)
            print(f"Error handling message from {addr}: {str(e)}")

    def send_error_message(self, error_msg, addr):
        packet = util.make_packet("error", 0, error_msg)
        self.sock.sendto(packet.encode(), addr)

    def route_message(self, message, addr):
        parts = message.split()
        num_users = int(parts[0])
        usernames = parts[1:num_users + 1]
        actual_message = ' '.join(parts[num_users + 1:])
        sender = None
        # Identify the sender based on the address
        for name, address in self.clients.items():
            if address == addr:
                sender = name
                break
        if not sender:
            print("Sender not recognized.")
            return

        print(f"Routing message from {sender} to {usernames}: {actual_message}")  # Debugging output
        for username in usernames:
            if username in self.clients:
                client_addr = self.clients[username]
                # Include the sender's name in the message
                forward_message = f"From {sender}: {actual_message}"
                packet = util.make_packet("msg", 0, forward_message)
                self.sock.sendto(packet.encode(), client_addr)
            else:
                print(f"User {username} not found")  # Debugging output

    def send_user_list(self, addr):
        user_list = ' '.join(self.clients.keys())
        packet = util.make_packet("list", 0, user_list)
        self.sock.sendto(packet.encode(), addr)

    def handle_join(self, username, addr):
        if username in self.clients:
            # Reject the new connection attempt if the username is already in use
            msg = util.make_packet("error", 0, "Username unavailable. Please choose a different username.")
            self.sock.sendto(msg.encode(), addr)
            print(f"Rejected join attempt with username '{username}' from {addr} - Username already in use.")
        elif len(self.clients) >= self.MAX_NUM_CLIENTS:
            msg = util.make_packet("error", 0, "Server full")
            self.sock.sendto(msg.encode(), addr)
        else:
            # Accept the new client if the username is not in use
            self.clients[username] = addr
            print(f"Client {username} joined from {addr}")

    def handle_message(self, params, addr):
        num_users = int(params[0])
        users = params[1:num_users+1]
        message = ' '.join(params[num_users+1:])
        for user in users:
            if user in self.clients:
                self.sock.sendto(message.encode(), self.clients[user])

    def handle_quit(self, addr):
        for username, address in self.clients.items():
            if address == addr:
                del self.clients[username]
                break
        print(f"{username} disconnected.")
    
    def handle_disconnect(self, username, addr):
        if username in self.clients:
            print(f"Client {username} disconnected.")
            del self.clients[username]  # Remove the client from active clients

    def shutdown_server(self):
        self.sock.close()
        print("Server has been shut down.")

# Do not change below part of code

if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our module completion
        '''
        print("Server")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-w WINDOW | --window=WINDOW The window size, default is 3")
        print("-h | --help Print this help")

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "p:a:w", ["port=", "address=","window="])
    except getopt.GetoptError:
        helper()
        exit()

    PORT = 15000
    DEST = "localhost"
    WINDOW = 3

    for o, a in OPTS:
        if o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a
        elif o in ("-w", "--window="):
            WINDOW = a

    SERVER = Server(DEST, PORT,WINDOW)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
