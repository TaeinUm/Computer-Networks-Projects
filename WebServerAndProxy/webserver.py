"""
CSE 310
Taein Um
112348159
"""

import socket
import os
import mimetypes


# Function to generate an HTTP response
def http_response(header, content_type, content):
    # Constructs an HTTP response with appropriate headers and content
    return f"{header}\r\nContent-Length: {len(content)}\r\nContent-Type: {content_type}\r\n\r\n".encode() + content


# Function to generate a 404 Not Found response
def file_not_found_response():
    # Returns a 404 error page as part of the HTTP response
    content = "<html><body><h1>404 Not Found</h1></body></html>".encode()
    return http_response("HTTP/1.0 404 Not Found", "text/html", content)


# Function to handle incoming client requests
def handle_request(client_connection):
    # Receives and decodes the client's request
    request = client_connection.recv(1024).decode()
    print(f"Received request:\n{request}")

    # Parses the request to extract the filename
    lines = request.splitlines()
    top_line = lines[0]
    filename = top_line.split()[1]

    # Prepares the file path
    filepath = filename[1:]
    if filepath == "":
        filepath = "HelloWorld.html"  # Default file to serve if no specific file is requested

    # Checks if the file exists and determines its MIME type
    if os.path.isfile(filepath):
        mime_type, _ = mimetypes.guess_type(filepath)  # Dynamically sets the Content-Type based on the file
        mime_type = mime_type or 'application/octet-stream'  # Default MIME type for binary files
        with open(filepath, 'rb') as f:
            response_content = f.read()
        response = http_response("HTTP/1.0 200 OK", mime_type, response_content)
    else:
        response = file_not_found_response()  # Handles the case where the file is not found

    # Sends the constructed HTTP response to the client
    client_connection.sendall(response)


# Function to start the web server
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)  # Listens for incoming connections
    print(f"Listening on port {port}...")

    while True:
        # Accepts a connection and handles the request
        client_connection, client_address = server_socket.accept()
        handle_request(client_connection)
        client_connection.close()  # Closes the connection after handling the request


if __name__ == "__main__":
    start_server(8080)  # Start the server listening on port 8080
