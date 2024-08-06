import re
import socket
import sqlite3
from datetime import datetime


def split_row(row):
    row = row.strip("'")
    timestamp_str, rest = row.split(' UTC ', 1)
    timestamp_str = timestamp_str[:-3]
    timestamp = datetime.strptime(timestamp_str, '%b %d, %Y %H:%M:%S.%f')
    pattern = r'"([^"]*)"\s+"([^"]*)"\s+"([^"]*)"\s+([\d.-]+)'
    matches = re.findall(pattern, rest)
    if matches:
        source_mac = matches[0][0]
        dest_mac = matches[0][1]
        rssi = int(matches[0][2])
        point = float(matches[0][3])
        return (timestamp, source_mac, dest_mac, rssi, point)
    else:
        raise ValueError("Row format is incorrect")

def add_row_to_table(data, conn):
    decoded_data = data.decode('utf-8')
    data = split_row(decoded_data)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO reference (Timestamp, Source_MAC, Destination_MAC, RSSI, Dictance)
            VALUES (?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e)
        conn.rollback()


def on_client(clientsocket, db_file='database.sqlite'):
    connected = True
    add = clientsocket.getpeername()
    conn = sqlite3.connect(db_file)

    while connected:
        print(f"Connected by {add}")
        data = clientsocket.recv(4096)
        if not data:
            connected = False
            break
        print("received: {}".format(data))
        add_row_to_table(data, conn)
        clientsocket.send(b"collection for this is done")

    conn.close()
    clientsocket.close()

HOST = "192.168.137.1"
PORT = 65431
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print("Server started!")
print("Waiting for a client")

db_conn = sqlite3.connect('database.sqlite')
cursor = db_conn.cursor()

server_running = True
while server_running:
    try:
        conn, addr = s.accept()
        on_client(conn)
    except KeyboardInterrupt:
        print("Server is shutting down...")
        server_running = False

db_conn.close()
s.close()