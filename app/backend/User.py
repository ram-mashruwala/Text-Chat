import socket
import threading

HEADER = 64
PORT = 5050
SERVER = "127.0.0.1"
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)


def send(msg, client):
    """Send a message to the server."""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive(client):
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

def start(username):
    """Start the chat client."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    thread = threading.Thread(target=receive, daemon=True, args=(client))
    thread.start()
    while True:
        msg = input("> ")
        if msg == "quit()":
            send(DISCONNECT_MESSAGE)
            print("[DISCONNECTING] Disconnecting from the server...")
            client.close()
            break
        send(f"{username}: {msg}", client=client)

if __name__ == "__main__":
    username = input("What is your username? ")
    start(username)


# import socket
# import time
# import threading

# HEADER = 64
# PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
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
#             break

#         with open (f"chat_{username}.txt", "a") as f:
#             f.write(msg + "\n")
#             send(msg)

        
# def recieve():
#     while True:
#         msg_len = client.recv(HEADER).decode(FORMAT)
#         if msg_len:
#             msg_len = int(msg_len)
#             msg = client.recv(msg_len).decode(FORMAT)
#             print(msg)


# start()