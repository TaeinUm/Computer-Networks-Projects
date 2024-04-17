# CSE 310 Programming Assignment 1

#### Taein Um
#### 1112348159

## External Libraries Used

- `socket`: For TCP connection handling.
- `os`: To interact with the file system.
- `mimetypes`: To determine the MIME type of served files.
- `threading`: For handling multiple connections concurrently in the proxy server.
- `hashlib`: For generating cache filenames based on request URLs.
- `logging`: For logging server operations.

## Instructions on Running the Programs

### Part A

1. Place `webserver.py` and an HTML file (e.g., `HelloWorld.html`) in the same directory.
2. Run the server using `python webserver.py`.
3. Access the web server from a browser using the server's IP address and port. I used port 8080, e.g., `http://localhost:8080/HelloWorld.html`.

### Part B

1. Run the proxy server using `python proxyserver.py`.
2. Configure your web browser to use the proxy with the server's IP address and port, e.g., `localhost` and `8888`.
3. Access web pages through the proxy, e.g., `http://localhost:8888/http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html`.

## Tested Webpages

Below are the webpages I tested with:
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file5.html
