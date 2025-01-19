import socket
import time
import threading
import sys

HEADER = 64
PORT = 5050
SERVER = "23.16.174.126"
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

username = input("What is your username? ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    """Send a message to the server."""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    """Receive messages from the server and log them."""
    while True:
        try:
            msg_len = client.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = client.recv(msg_len).decode(FORMAT)
                print(msg)
        except Exception as e:
            print(f"[ERROR] {e}")
            break

def start():
    """Start the chat client."""
    with open(f"chat_{username}.txt", "w") as f:  # Reset file at the start
        f.write(f"Chat log for {username}:\n")
    thread = threading.Thread(target=receive, daemon=True)
    thread.start()
    while True:
        msg = input("> ")
        if msg == "quit()":
            send(DISCONNECT_MESSAGE)
            print("[DISCONNECTING] Disconnecting from the server...")
            client.close()
            break
        send(f"{username}: {msg}")

start()

# import socket
# import time
# import threading
# import sys

# HEADER = 64
# PORT = 5050
# SERVER = "23.16.174.126"
# FORMAT = "utf-8"
# DISCONNECT_MESSAGE = "!DISCONNECT"
# ADDR = (SERVER, PORT)

# username = input("What is your username? ")

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)

# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b" " * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     time.sleep(1)

# def start():
#     open(f"chat_{username}.txt", "w")
#     thread = threading.Thread(target=recieve)
#     thread.start()
#     while True:
#         msg = input("> ")
#         if msg == "quit()":
#             send(DISCONNECT_MESSAGE)
#             socket.close()
#             break
        
        
#         send(msg)

        
# def recieve():
#     while True:
#         msg_len = client.recv(HEADER).decode(FORMAT)
#         if msg_len:
#             msg_len = int(msg_len)
#             msg = client.recv(msg_len).decode(FORMAT)
#             print(msg)



# start()