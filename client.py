import socket
import tictactoe
import json
from time import sleep

# set server name to IP address of server
serverName = "localhost"
serverPort = 5000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def play(playerInfo, currentSocket):
    state = tictactoe.getNewPlayer(playerInfo["player"])

    if playerInfo["player"] == "O":
        print("Waiting on opponent's move...")
        receiveMessage = currentSocket.recv(1024).decode("utf-8")
        state = json.loads(receiveMessage)
        state["player"] = playerInfo["player"]

    while not tictactoe.isGameOver(state):
        print(tictactoe.printBoard(state))
        state = tictactoe.userTurn(state)
        state["player"] = playerInfo["player"]
        print(tictactoe.printBoard(state))

        sendMessage = json.dumps(state).encode("utf-8")
        currentSocket.send(sendMessage)

        if not tictactoe.isGameOver(state):
            receiveMessage = currentSocket.recv(1024).decode("utf-8")
            state = json.loads(receiveMessage)
            state["player"] = playerInfo["player"]
        if tictactoe.isGameOver(state):
            print(tictactoe.printBoard(state))

    print(tictactoe.isGameOver(state))
    print("Client closed")
    currentSocket.close()

# choose opponent type
print(clientSocket.recv(1024).decode("utf-8"))
mode = input()
clientSocket.send(mode.encode("utf-8"))

print(clientSocket.recv(1024).decode("utf-8"))

playerInfo = json.loads(clientSocket.recv(1024).decode("utf-8"))


if playerInfo["opponentType"] != "computer":
    print("Found Opponent: (IP: %s, Port: %s)" % (playerInfo["opponentIP"], playerInfo["opponentPort"]))
    print("You are player: %s" % playerInfo["player"])

# Hybrid Mode: Peer-to-peer connection
# Player X acts as client. Player O acts as server.
if mode == "3":
    if playerInfo["player"] == "X":
        p2pClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                p2pClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                p2pClientSocket.connect((playerInfo["opponentIP"], playerInfo["opponentPort"]))
                break
            except Exception as e:
                print(e)
                sleep(1)

        print("P2P Connected to: ", playerInfo["opponentIP"], playerInfo["opponentPort"])
        play(playerInfo, p2pClientSocket)


    else:
        p2pServerIP, p2pServerPort = clientSocket.getsockname()

        p2pServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p2pServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        p2pServerSocket.bind((p2pServerIP, p2pServerPort))
        p2pServerSocket.listen(1)
        print("P2P Listening on: ", p2pServerIP, p2pServerPort)

        while True:
            connectionSocket, addr = p2pServerSocket.accept()
            print("Got connection from ", addr)
            play(playerInfo, connectionSocket)
            break


else:
    play(playerInfo, clientSocket)