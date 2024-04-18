# Web Server and Proxy

#### Taein Um



## Overview
This project contains the source code for a basic Web Server and a Web Proxy Server, developed for the Computer Networks course at Stony Brook University. These applications illustrate the practical application of networking theories including TCP socket programming, handling HTTP requests, and implementing a caching mechanism for web contents.



## Features

### Web Server

- **HTTP Request Handling**: Processes one HTTP request at a time, ensuring simplicity and clarity in handling connections.
- **File Serving**: Serves requested files from the server's local filesystem, including HTML, JPEG, and PNG files.
- **Response Generation**: Generates proper HTTP headers and content in responses, including handling for 404 Not Found errors when a file is not available.

### Proxy Server

- **Caching**: Implements basic caching to store and serve frequently requested web resources, reducing load times and bandwidth.
- **Request Forwarding**: Forwards client requests to the appropriate web server and delivers the server’s response back to the client, acting as an intermediary.



## Technologies Used
- **Language**: `Python`
- **Libraries**: 
    - `socket`: For TCP connection handling.
    - `os`: To interact with the file system.
    - `mimetypes`: To determine the MIME type of served files.
    - `threading`: For handling multiple connections concurrently in the proxy server.
    - `hashlib`: For generating cache filenames based on request URLs.
    - `logging`: For logging server operations.



## Instructions on Running the Programs

### Web Server

1. Place `webserver.py` and an HTML file (the sample file, `HelloWorld.html`, is attached) in the same directory.
2. Run the server using `python webserver.py`.
3. Access the web server from a browser using the server's IP address and port. I used port 8080, e.g., `http://localhost:8080/HelloWorld.html`.

### Proxy Server

1. Run the proxy server using `python proxyserver.py`.
2. Configure your web browser to use the proxy with the server's IP address and port, e.g., `localhost` and `8888`.
3. Access web pages through the proxy, e.g., `http://localhost:8888/http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html`.

## Tested Webpages

Below are the webpages I tested with:
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file5.html



## Contact Information
- Name: Taein Um
- Email: taeindev@gmail.com
- LinkedIn: https://www.linkedin.com/in/taein-um-00b14916b/
