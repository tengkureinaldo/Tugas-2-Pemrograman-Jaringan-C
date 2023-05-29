import sys
import socket
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(10)

    # Bind the socket to the port
    server_address = ('172.19.0.5', 45000) #--> gunakan 0.0.0.0 agar binding ke seluruh ip yang tersedia

    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(2)
    #1 = backlog, merupakan jumlah dari koneksi yang belum teraccept/dilayani yang bisa ditampung, diluar jumlah
    #             tsb, koneks akan direfuse
    while True:
        # Wait for a connection
        logging.info("waiting for a connection")
        connection, client_address = sock.accept()
        logging.info(f"connection from {client_address}")
        # Receive the data in small chunks and retransmit it
        while True:
            now = datetime.now()
            waktu = now.strftime("%H:%M:%S")
            data = connection.recv(1024).decode()
            tes = "TIME dan diakhiri dengan karakter 13 dan karakter 10"
            logging.info(f"received {data}")
            if data == tes:
                logging.info(f"sending the data to {client_address}")
                msg = "JAM {} karakter 13 dan karakter 10".format(waktu)
                connection.send(msg.encode())
            else:
                logging.info(f"wrong data from {client_address}")
                break
            
        # Clean up the connection
        connection.close()
        break 
    
except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
finally:
    logging.info('closing')
    sock.close()
