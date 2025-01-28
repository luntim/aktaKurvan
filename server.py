import socket
from _thread import *
import sys

server = "92.33.213.25"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(str):
    str = str.split(",")
    return float(str[0]), float(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(580,230),(1020,670)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())

            if not data:
                print("Disconnected")
                break
            else:
                pos[player] = data
                print(f"pos[{player}]: {pos[player]}\ndata: {data}")
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1] 
                
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    print("currentplayer: ", currentPlayer)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1