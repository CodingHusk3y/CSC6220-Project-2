import socket
import sys

def send_request(path):
    host = '127.0.0.1'
    port = 8080
    client_socket = None

    try:
        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((host, port))

        # Prepare the HTTP-style GET request
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

        # Send the request
        client_socket.sendall(request.encode('utf-8'))

        # Receive the response
        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        # Display the response
        print(response.decode('utf-8'))

    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        if client_socket:
            client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '/hello'

    send_request(path)
