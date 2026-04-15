# Mini HTTP Server Design and Implementation

## Design Overview
This project implements a simple client-server application using Python's `socket` library. The server simulates basic HTTP-style communication, handling GET requests and returning formatted HTTP responses.

### Server Architecture
The server follows a sequential processing model:
1.  **Socket Initialization**: Creates a TCP socket and binds it to all available interfaces on port 8080.
2.  **Listening Loop**: Continuously listens for incoming connections.
3.  **Request Handling**: For each connection:
    -   Reads the incoming data.
    -   Parses the request line to extract the method (e.g., GET) and the path (e.g., /hello).
    -   Routes the request based on the path to generate a response body.
    -   Constructs an HTTP/1.1 response with appropriate headers (`Content-Type`, `Content-Length`) and status codes (200 OK or 404 Not Found).
    -   Logs the request details (Timestamp, Client IP, Path, Status Code) to the console.
    -   Sends the response back and closes the client connection.

### Client Architecture
The client is a straightforward script that:
1.  Connects to the server's IP and port via a TCP socket.
2.  Sends a properly formatted HTTP GET request string.
3.  Receives and displays the raw response from the server.
4.  Closes the connection.

## Implementation Details
-   **Endpoints**:
    -   `/hello`: Greeting message.
    -   `/time`: Returns current server time.
    -   `/dns`: Explains DNS.
    -   `/http`: Explains HTTP.
    -   `/status`: Returns server health status.
    -   `/quote`: (Creative Bonus) Returns an inspirational quote.
    -   `/ask?question=...`: (Bonus) Echoes the user's question.
-   **Error Handling**: Unknown routes return `HTTP/1.1 404 Not Found`.
-   **Logging**: Every request is logged with a timestamp and the client's IP address.

## Sample Outputs

### Client Interaction
```text
$ python3 client.py /hello
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 34

Hello! Welcome to the mini server.

$ python3 client.py /time
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 43

Current server time is: 2026-04-15 02:47:52

$ python3 client.py /unknown
HTTP/1.1 404 Not Found
Content-Type: text/plain
Content-Length: 13

404 Not Found
```

### Server Logs
```text
Server is listening on port 8080...
[2026-04-15 02:47:52] 127.0.0.1 requested /hello - Status: 200
[2026-04-15 02:47:52] 127.0.0.1 requested /time - Status: 200
[2026-04-15 02:47:54] 127.0.0.1 requested /unknown - Status: 404
```
