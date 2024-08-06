import sys
import socket

def send_data_to_endpoint(data):
    host = '192.168.137.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(data.encode('utf-8'))
        response = sock.recv(1024)
        print(f"Received: {response.decode('utf-8')}")

def main():
    for line in sys.stdin:
        send_data_to_endpoint(line.strip())

if __name__ == "__main__":
    main()