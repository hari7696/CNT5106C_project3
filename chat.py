import socket
import threading
import os
import sys
import socket
import threading
import random
import struct


def send_message(sock, message):
    msg = struct.pack(">I", len(message)) + message
    sock.sendall(msg)


def receive_message(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack(">I", raw_msglen)[0]
    return recvall(sock, msglen)


def recvall(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def writing_thread():
    # This thread will take a port number from the keyboard and then connects to that port number.
    # After the connection (socket) is successfully established,
    # it goes into a loop of reading  a message from the KEYBOARD and writing the message to the connection (socket)
    while True:
        print("Writing Thread: Enter port number to connect to:")
        port_number = int(input())
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        client.connect((host, port_number))
        print(
            "CONNECTION ESTABLISHED WITH SERVER {} ON PORT {}".format(host, port_number)
        )

        while True:

            message = input()
            if message.startswith("transfer"):
                client.send(message.encode("utf-8"))
                file_name = message.split(" ")[1]
                with open(file_name, "rb") as f:
                    while True:
                        chunk = f.read(1024)  # Read 1KB chunks
                        if not chunk:
                            break  # End of file
                        send_message(client, chunk)
                        # print(chunk)
                send_message(client, b"")
                client.send("FROM SENDER: file transfer complete".encode("utf-8"))

            elif message == "exit":
                client.send(message.encode("utf-8"))
                client.shutdown(2)
                client.close()
                os._exit(1)
            else:
                client.send(message.encode("utf-8"))


def reading_thread():
    # This thread will attempt to read messages from the connection socket and print the messages on the screen.
    # If the message is “transfer filename”, it reads the file and stores locally
    # Also acts as main thread

    port_number = random.randint(5000, 10000)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    server.bind((host, port_number))
    server.listen(5)
    print(f"Reading thread Actively waiting to connect on {host}:{port_number}")
    client, addr = server.accept()
    print("Got connection from", addr)

    while True:
        message = client.recv(1024).decode("utf-8")
        if message.startswith("transfer"):
            print(message)
            file_name = message.split(" ")[1]
            filetodown = "new" + file_name
            with open(filetodown, "wb") as f:
                while True:
                    chunk = receive_message(client)
                    # print(chunk)
                    if chunk == b"":
                        break  # End of file
                    f.write(chunk)
            print("STATUS: File Downloaded.")

        elif message == "exit":
            print(message)
            client.shutdown(2)
            client.close()
            os._exit(1)
        else:
            print(message)


def main():

    _writing_thread = threading.Thread(target=writing_thread)
    _reading_thread = threading.Thread(target=reading_thread)
    print("Main program: Threads started")
    _reading_thread.start()
    _writing_thread.start()


if __name__ == "__main__":
    main()
