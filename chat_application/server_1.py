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
        self.clients = {}  # Maps usernames to address
        self.reverse_clients = {}  # Maps addresses to usernames

    def start(self):
        '''
        Main loop.
        Continuously receive and process messages from clients.

        '''
        while True:
            msg, addr = self.sock.recvfrom(2048)  # Receives data up to 2048 bytes.
            msg = msg.decode()  # Converts bytes to string.

            pck_type, seqno, data, checksum = util.parse_packet(msg)
            msg_type, data = data.split(' ', maxsplit=1)

            # Dispatch message based on its type.
            if msg_type == "join":
                self.handle_join(msg_type, data, addr)
            elif msg_type == "request_users_list":
                self.handle_list_request(addr)
            elif msg_type == "send_message":
                self.handle_send_message(data, addr)
            elif msg_type == "disconnect":
                self.handle_disconnect(data, addr)
            else:
                self.handle_unknown_message(msg_type, addr)

    def send_response(self, message_type, message_format, data, addr):
        # Prepares and sends a response to the client.
        msg = util.make_message(message_type, message_format, data)
        packet = util.make_packet(msg=msg)
        self.sock.sendto(packet.encode(), addr)

    def handle_join(self, msg_type, data, addr):
        # Handles client join requests.
        username = data.split(' ')[1]

        if len(self.clients) >= util.MAX_NUM_CLIENTS:
            # Server full scenario
            self.send_response("err_server_full", 2, None, addr)
            print(f"Client {username} from {addr} cannot join as server is full")
            print("disconnected: server full")
        elif username in self.clients:
            # Username already taken scenario
            self.send_response("err_username_unavailable", 2, None, addr)
            print(f"Client {username} from {addr} already exists")
            print("disconnected: username not available")
        else:
            # Successful join
            self.clients[username] = addr
            self.reverse_clients[addr] = username
            print(f"join: {username}")

    def handle_list_request(self, addr):
        # Handles request to list all users.
        username = self.reverse_clients[addr]
        sorted_clients = sorted(self.clients.keys())
        user_list = f"{len(sorted_clients)} {' '.join(sorted_clients)}"
        self.send_response("response_users_list", 3, user_list, addr)
        print(f"request_users_list: {username}")

    def handle_send_message(self, data, addr):
        # Processes a message sending request to other clients.
        username = self.reverse_clients[addr]
        parts = data.split(' ')
        num_users = int(parts[1])
        user_list = parts[2:num_users+2]
        message = " ".join(parts[num_users+2:])

        for recv_user in user_list:
            if recv_user in self.clients:
                recv_addr = self.clients[recv_user]
                self.send_response("forward_message", 4, f"1 {username} {message}", recv_addr)
            else:
                print(f"msg: {username} to non-existent user {recv_user}")

        print(f"msg: {username}")

    def handle_disconnect(self, data, addr):
        # Handles a client's disconnection request.
        username = data.split(' ')[1]
        del self.clients[username]
        del self.reverse_clients[addr]
        print(f"disconnected: {username}")

    def handle_unknown_message(self, msg_type, addr):
        # Deals with unknown message types.
        self.send_response("err_unknown_message", 2, None, addr)
        print(f"Unknown message type: {msg_type}")
        print(f"disconnected: {addr} sent unknown command")



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
