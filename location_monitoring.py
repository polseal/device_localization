import csv
import io
import re
import sqlite3
import socket
import threading
from datetime import datetime


def split_row(row):
    row = row.strip("'")
    timestamp_str, rest = row.split(' UTC ', 1)
    timestamp_str = timestamp_str[:-3]
    timestamp = datetime.strptime(timestamp_str, '%b %d, %Y %H:%M:%S.%f')
    pattern = r'"([^"]*)"|\(([^)]*)\)'
    matches = re.findall(pattern, rest)
    source_mac = matches[0][0]
    dest_mac = matches[1][0]
    rssi = int(matches[2][0])
    point = matches[3][1]
    return (timestamp, source_mac, dest_mac, rssi, point)

def add_row_to_table(data, conn):
    decoded_data = data.decode('utf-8')
    data = split_row(decoded_data)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO rssi_data (Timestamp, Source_MAC, Destination_MAC, RSSI, Point)
            VALUES (?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e)
        conn.rollback()


def on_new_client(clientsocket):
    connected = True
    add = clientsocket.getpeername()
    conn = sqlite3.connect("database.sqlite")
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

#HOST = "0.0.0.0" for testing
HOST = "192.168.137.1"
PORT = 65432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print("Server started!")
print("Waiting for a client")

db_conn = sqlite3.connect("database.sqlite")
cursor = db_conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS rssi_data (
        Timestamp TEXT,
        Source_MAC TEXT,
        Destination_MAC TEXT,
        RSSI TEXT,
        Point TEXT
    )
''')
db_conn.commit()
db_conn.close()

server_running = True
while server_running:
    try:
        conn, addr = s.accept()
        threading.Thread(target=on_new_client, args=(conn,)).start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
        server_running = False

db_conn.close()
s.close()