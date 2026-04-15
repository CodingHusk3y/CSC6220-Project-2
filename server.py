import socket
import datetime
import sys

def log_request(client_ip, path, status_code):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {client_ip} requested {path} - Status: {status_code}")
    sys.stdout.flush()

def handle_request(request_data, client_address):
    lines = request_data.split('\r\n')
    if not lines or not lines[0]:
        return "HTTP/1.1 400 Bad Request\r\n\r\n", 400

    request_line = lines[0]
    parts = request_line.split(' ')
    if len(parts) < 2:
        return "HTTP/1.1 400 Bad Request\r\n\r\n", 400

    method = parts[0]
    path = parts[1]

    if method != 'GET':
        log_request(client_address[0], path, 405)
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n", 405

    response_body = ""
    status_header = "200 OK"
    status_code = 200

    if path == '/hello':
        response_body = "Hello! Welcome to the mini server."
    elif path == '/time':
        response_body = f"Current server time is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elif path == '/dns':
        response_body = "DNS (Domain Name System) is the phonebook of the Internet. It translates domain names like google.com to IP addresses."
    elif path == '/http':
        response_body = "HTTP (Hypertext Transfer Protocol) is the foundation of data communication for the World Wide Web."
    elif path == '/status':
        response_body = "Server is running smoothly."
    elif path == '/quote':
        response_body = "The only way to do great work is to love what you do. - Steve Jobs"
    elif path.startswith('/ask?'):
        query = path.split('?', 1)[1]
        if query.startswith('question='):
            question = query.split('=', 1)[1].replace('%20', ' ')
            response_body = f"You asked: {question}. My answer is: That's a great question!"
        else:
            response_body = "Please ask a question using /ask?question=..."
    else:
        status_code = 404
        status_header = "404 Not Found"
        response_body = "404 Not Found"

    response = f"HTTP/1.1 {status_header}\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
    log_request(client_address[0], path, status_code)
    return response, status_code

def start_server():
    host = '0.0.0.0'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(f"Bind failed. Error: {e}")
        sys.exit()

    server_socket.listen(5)

    print(f"Server is listening on port {port}...")
    sys.stdout.flush()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            try:
                request_data = client_socket.recv(1024).decode('utf-8')
                if request_data:
                    response, status_code = handle_request(request_data, client_address)
                    client_socket.sendall(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling request: {e}")
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
