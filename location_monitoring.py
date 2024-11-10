import csv
import io
import re
import sqlite3
import socket
import threading
from datetime import datetime


def split_row(row):
    rows = []
    for line in row.strip().split("\n"):
        parts = line.split()
        if len(parts) >= 6:
            timestamp = f"{parts[0]} {parts[1]} {parts[2]} {parts[3]}"  # Combine date and time components
            mac = parts[5]
            broadcast_mac = parts[6]
            # Check if signal strength exists (it may be absent in some cases)
            signal_strength = parts[7] if len(parts) > 7 else None
            point = parts[8]
            # Store the data in a dictionary
            rows.append({
                "Timestamp": timestamp,
                "Destination_MAC": mac,
                "Source_MAC": broadcast_mac,
                "RSSI": signal_strength,
                "Point": point
            })
    return rows

def add_row_to_table(data, conn):
    decoded_data = data.decode('utf-8')
    rows = split_row(decoded_data)
    cursor = conn.cursor()
    for row in rows:
        try:
            cursor.execute('''
                   INSERT INTO rssi_data (Timestamp, Source_MAC, Destination_MAC, RSSI, Point)
                   VALUES (?, ?, ?, ?, ?)
               ''', (row["Timestamp"], row["Source_MAC"], row["Destination_MAC"], row["RSSI"], row["Point"]))
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