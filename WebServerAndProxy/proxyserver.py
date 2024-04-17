"""
CSE 310
Taein Um
112348159
"""

import socket
import threading
import signal
import os
import hashlib
import logging

# Set up logging for debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Proxy server configuration
config = {
    'HOST_NAME': '0.0.0.0',  # Listen on all network interfaces
    'PORT': 8888,  # Port for proxy server to bind
    'MAX_REQUEST_LEN': 4096,  # Maximum request length to handle
    'CONNECTION_TIMEOUT': 5,  # Connection timeout for sockets
    'CACHE_DIR': 'cache'  # Directory to store cached content
}

# Ensure cache directory exists
if not os.path.isdir(config['CACHE_DIR']):
    os.makedirs(config['CACHE_DIR'])


class ProxyServer:
    def __init__(self, config):
        # Graceful shutdown handling
        signal.signal(signal.SIGINT, self.shutdown)
        # Socket setup
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((config['HOST_NAME'], config['PORT']))
        self.serverSocket.listen(10)  # Start listening for connections
        logging.info("Proxy Server started on port {0}".format(config['PORT']))

    def proxy_thread(self, conn, client_address):
        # Thread to handle each client request
        try:
            request_line = conn.recv(config['MAX_REQUEST_LEN']).decode('utf-8')
            if not request_line:  # Ignore empty requests
                return
            # Extract and process URL from client request
            first_line = request_line.split('\n')[0]
            url = first_line.split(' ')[1]
            actual_url = url[1:]  # Remove leading slash

            # Ignore favicon.ico requests
            if "favicon.ico" in actual_url:
                conn.close()
                return

            # Parse URL to find hostname, port, and path
            http_pos = actual_url.find("://")
            temp = actual_url[(http_pos + 3):] if http_pos != -1 else actual_url
            port_pos = temp.find(":")
            webserver_pos = temp.find("/") if temp.find("/") != -1 else len(temp)
            webserver = temp[:port_pos] if port_pos != -1 else temp[:webserver_pos]
            port = int(temp[port_pos + 1:webserver_pos]) if port_pos != -1 else 80
            path = actual_url[actual_url.find(webserver) + len(webserver):]

            # Check cache before fetching from web
            cache_filename = hashlib.sha256(actual_url.encode('utf-8')).hexdigest()
            cache_filepath = os.path.join(config['CACHE_DIR'], cache_filename)

            # Serve content from cache or fetch from web
            if os.path.isfile(cache_filepath):
                logging.info("Cache hit for {0}".format(actual_url))
                with open(cache_filepath, 'rb') as f:
                    conn.sendall(f.read())
            else:
                logging.info("Cache miss for {0}. Fetching from web.".format(actual_url))
                self.fetch_from_web(conn, webserver, port, path, cache_filepath)
        except Exception as e:
            logging.error("An error occurred: {0}".format(e))
        finally:
            conn.close()

    def fetch_from_web(self, conn, webserver, port, path, cache_filepath):
        # Fetch content from the web and cache it
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(config['CONNECTION_TIMEOUT'])
            s.connect((webserver, port))
            server_request = f"GET {path} HTTP/1.0\r\nHost: {webserver}\r\n\r\n"
            s.sendall(server_request.encode())
            with open(cache_filepath, 'wb') as cache_file:
                while True:
                    data = s.recv(config['MAX_REQUEST_LEN'])
                    if len(data) > 0:
                        conn.send(data)
                        cache_file.write(data)
                    else:
                        break

    def shutdown(self, signum, frame):
        # Shutdown the proxy server
        logging.info('Shutting down the server...')
        self.serverSocket.close()

    def start(self):
        # Start the proxy server and handle incoming connections
        while True:
            client_socket, client_address = self.serverSocket.accept()
            threading.Thread(target=self.proxy_thread, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    server = ProxyServer(config)
    server.start()
