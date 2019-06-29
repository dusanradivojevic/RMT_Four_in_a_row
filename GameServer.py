from socket import *
import ClientClass, Gameplay

#===========================================
def greetings(clientSocket):
    clientSocket.send('>> Dobrodosli! Igra ce uskoro poceti.'.encode())

def beginGame(client1, client2):
    Gameplay.main(client1, client2)
    client1.clientSocket.close()
    client2.clientSocket.close()

def setUpGame(client1, client2):
    client1.clientSocket.send('\n===========\n'.encode())
    client1.clientSocket.send('>> Unesite korisnicko ime:'.encode())
    client1.name = client1.clientSocket.recv(4096).decode()
    client1.clientSocket.send(('>> Vase korisnicko ime je ' + client1.name).encode())

    client2.clientSocket.send('\n===========\n'.encode())
    client2.clientSocket.send('>> Unesite korisnicko ime:'.encode())
    client2.name = client2.clientSocket.recv(4096).decode()
    client2.clientSocket.send(('>> Vase korisnicko ime je ' + client2.name).encode())


    client1.clientSocket.send(('\n===========\n\n>> Vas protivnik je: ' + client2.name + '. \n>>Vi ste prvi igrac, srecno!').encode())
    client2.clientSocket.send(('\n===========\n\n>> Vas protivnik je: ' + client1.name + '. \n>>Vi ste drugi igrac, srecno!').encode())

    beginGame(client1, client2)

def main_openConnection():
    server_address = 'localhost'
    server_port = 17510

    # AF_INET - IPv4 protokol, SOCK_STREAM - TCP protokol
    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind((server_address, server_port))

    # Slusa za konekcije
    server_socket.listen()
    print('>> Cekanje na konekciju . . .')

    queueList = []

    while True:
        # Prihvata konekciju klijenta
        client_socket, client_address = server_socket.accept()

        greetings(client_socket)

        client = ClientClass.Client('noName',client_socket,client_address)
        queueList.append(client)

        print(f'>> Igrac je pristigao! U redu cekanja za igru ima ukupno {len(queueList)} igraca.')

        if(len(queueList) >= 2):
            print('>> Pokrecem igru . . . ')

            setUpGame(queueList[0],queueList[1])
            queueList.pop(0)
            queueList.pop(0) # Jer zbog prethodne linije nemamo element sa indeksom 1
            break #ovo ne treba da stoji kad se ubace niti

# ===========================================

main_openConnection()