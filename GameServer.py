from socket import *
import ClientClass, Gameplay
from threading import *
from time import sleep

#===========================================
class ClientHandler(Thread):
    def __init__(self, cl1, cl2):
        super().__init__()

        self.client1 = cl1
        self.client2 = cl2

        self.start()

    def run(self):
        self.setUpGame(self.client1, self.client2)

    def enterName(self, clientSocket):
        clientSocket.send('\n===========\n'.encode())
        clientSocket.send('>> Unesite korisnicko ime:'.encode())
        name = clientSocket.recv(4096).decode()
        clientSocket.send(('>> Vase korisnicko ime je ' + name).encode())

        return name

    def beginGame(self, client1, client2):
        print('>> Igra je uspesno pokrenuta!')
        Gameplay.main(client1, client2)
        client1.clientSocket.close()
        client2.clientSocket.close()

    def setUpGame(self, client1, client2):
        client1.name = self.enterName(client1.clientSocket)
        client2.name = self.enterName(client2.clientSocket)

        client1.clientSocket.send(('\n===========\n\n>> Vas protivnik je: ' + client2.name + '. \n>>Vi ste prvi igrac, srecno!').encode())
        client2.clientSocket.send(('\n===========\n\n>> Vas protivnik je: ' + client1.name + '. \n>>Vi ste drugi igrac, srecno!').encode())

        sleep(3)  # Da bi stigli da procitaju info

        self.beginGame(client1, client2)
#===========================================
def greetings(clientSocket):
    clientSocket.send('>> Dobrodosli! Igra ce uskoro poceti.'.encode())

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
        client = ClientClass.Client("noName", client_socket, client_address)
        queueList.append(client)

        print(f'>> Igrac je pristigao! U redu cekanja za igru ima ukupno {len(queueList)} igraca.')

        if(len(queueList) >= 2):
            print('>> Pokrecem igru . . . ')

            try:
            #    th = threading.Thread(target=setUpGame, args=(queueList[0], queueList[1]))
            #    th.start()
                ClientHandler(queueList[0], queueList[1])
                queueList.pop(0)
                queueList.pop(0)  # Jer zbog prethodne linije nemamo element sa indeksom 1
            except:
                print('>> Doslo je do greske prilikom pokretanja igre!')


# ===========================================

main_openConnection()
