import tictactoe
import json
import socket
import threading

from app import app

@app.route('/')
@app.route('/index')

def a():
    return ""
'''
def a():

    numConnections = 0
    lock = threading.Lock()
    waitingPlayersHuman = []
    waitingPlayersHybrid = []
    playerGo = threading.Condition()

    serverPort = 5000
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("",serverPort))
    serverSocket.listen(5)
    print("The server is ready to receive")

    def newClientServerGame(connectionSocket, addr):
        state = tictactoe.getNewPlayer("O")
        try:
            while not tictactoe.isGameOver(state):
                receiveMessage = connectionSocket.recv(1024).decode("utf-8")
                state = json.loads(receiveMessage)

                if(tictactoe.isGameOver(state)):
                    break

                state = tictactoe.computerTurn(state)
                sendMessage = json.dumps(state).encode("utf-8")
                connectionSocket.send(sendMessage)
        except:
            print("Error Occurred with ", addr)
        finally:
            print("Connection with", addr, " closed")
            connectionSocket.close()

            lock.acquire()
            nonlocal numConnections
            numConnections -= 1
            print("Active Connections: ", numConnections)
            lock.release()

    def new2PlayerGame(player1, player2):
        try:
            while True:
                state = json.loads(player1["connection"].recv(1024).decode("utf-8"))
                if tictactoe.isGameOver(state):
                    player2["connection"].send(json.dumps(state).encode("utf-8"))
                    break

                player2["connection"].send(json.dumps(state).encode("utf-8"))
                state = json.loads(player2["connection"].recv(1024).decode("utf-8"))
                if(tictactoe.isGameOver(state)):
                    player1["connection"].send(json.dumps(state).encode("utf-8"))
                    break
                player1["connection"].send(json.dumps(state).encode("utf-8"))
        except:
            print("Error Occurred with ", addr)
        finally:
            print("Connection with", player1["addr"], " closed")
            print("Connection with", player2["addr"], " closed")
            player1["connection"].close()
            player2["connection"].close()

            lock.acquire()
            nonlocal numConnections
            numConnections -= 2
            print("Active Connections: ", numConnections)
            lock.release()
        

    def waitForPlayer(connectionSocket, addr, opponentType):
        lock.acquire()
        nonlocal waitingPlayersHuman
        nonlocal waitingPlayersHybrid
        nonlocal numConnections

        if opponentType == "2":
            opponentType = "human"
            waitingPlayers = waitingPlayersHuman
        elif opponentType == "3":
            opponentType = "hybrid"
            waitingPlayers = waitingPlayersHybrid

        waitingPlayers.append((connectionSocket, addr))
        if(len(waitingPlayers) == 2):
            firstPlayerInfo = {
                "opponentIP": waitingPlayers[1][1][0],
                "opponentPort": waitingPlayers[1][1][1],
                "opponentType": opponentType,
                "player": "X",
            }
            secondPlayerInfo = {
                "opponentIP": waitingPlayers[0][1][0],
                "opponentPort": waitingPlayers[0][1][1],
                "opponentType": opponentType,
                "player": "O"
            }
            waitingPlayers[0][0].send(json.dumps(firstPlayerInfo).encode("utf-8"))
            waitingPlayers[1][0].send(json.dumps(secondPlayerInfo).encode("utf-8"))


            if opponentType == "human":
                firstPlayerInfo["connection"] = waitingPlayers[0][0]
                firstPlayerInfo["addr"] = waitingPlayers[0][1]
                secondPlayerInfo["connection"] = waitingPlayers[1][0]
                secondPlayerInfo["addr"] = waitingPlayers[1][1]

                waitingPlayers.clear()
                lock.release()
                new2PlayerGame(firstPlayerInfo, secondPlayerInfo)
                lock.acquire()

            # close client-server connections if hybrid
            # players will connect peer-to-peer
            elif opponentType == "hybrid":
                waitingPlayers[0][0].close()
                waitingPlayers[1][0].close()
                numConnections -= 2
                print("Active Connections: ", numConnections)
                waitingPlayers.clear()

        lock.release()

    def newClient(connectionSocket, addr):
        # opponent type
        message = "\nEnter 1 to play against the computer (client-server).\nEnter 2 to play against a human (client-server).\nEnter 3 to play against a human (hybrid / peer-to-peer).\n"
        connectionSocket.send(message.encode("utf-8"))
        opponentType = connectionSocket.recv(1024).decode("utf-8")

        if opponentType == "1":
            playerInfo = {
                "opponentType": "computer",
                "player": "X"
            }
            response = "You are playing against the computer.\nYou are player: X"
            connectionSocket.send(response.encode("utf-8"))
            connectionSocket.send(json.dumps(playerInfo).encode("utf-8"))
            newClientServerGame(connectionSocket, addr)
            
        elif opponentType == "2" or opponentType == "3":
            connectionSocket.send("Waiting for another human to connect...".encode("utf-8"))
            waitForPlayer(connectionSocket, addr, opponentType)

    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Got connection from ", addr)
        
        threading.Thread(target=newClient, args=(connectionSocket, addr)).start()

        lock.acquire()
        numConnections += 1
        print("Active Connections: ", numConnections)
        lock.release()


'''