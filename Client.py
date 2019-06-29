from socket import *
from time import sleep
import os, json

#=========================
def prikazi_polje(mat):
    print("")

    #slova iznad
    for k in range(65,72):
        print(" " + chr(k), end='')
    print("")

    #matrica
    for i in range(6):
        print("", end=' ')
        for j in range(7):
            if(j < 6):
                print(mat[i][j], end='|')
            else:
                print(mat[i][j])
    print("")

# ========================
def punaKolona(mat, izbor):
    izbor -= 65
    if (mat[0][izbor] != ' '):
        return True
    else:
        return False

# ========================
def unesiIzbor(mat, redni_br_igraca, kolona):
    kolona = kolona - 65
    for i in range(6):
        if(i < 5 and mat[i + 1][kolona] == ' '):
            continue
        else:
            if (redni_br_igraca == 0):
                mat[i][kolona] = 'X'
            else:
                mat[i][kolona] = 'O'

# ========================
def odigraj(mat, brIgraca):
    while (True):
        kolona = input()
        try:
            izbor = ord(kolona.upper())  # ascii predstava unetog slova

            if (izbor >= 65 and izbor < 72 and punaKolona(mat, izbor) == False):
                break
        except:
            print('>> Uneli ste pogresnu vrednost, probajte ponovo!')

    unesiIzbor(mat, brIgraca, izbor)
    return json.dumps({"b":mat})
# ========================
def igraj(client_socket):
#    print(client_socket.recv(4096).decode())  # Prijem oznaka
#   input()
 #   client_socket.send('%%%'.encode())

    matGl = []
    while True:
        s = client_socket.recv(4096).decode()
#        print(s)
        s = json.loads(s)
        prefiks = s.get("prefiks")
        podatak = s.get("podatak")

        if(prefiks == '%cls'):
            os.system('cls')
            continue

        if(prefiks == '%mat'):
            # Prijem matrice
            matGl = podatak
            prikazi_polje(matGl)
        elif(prefiks == '%prv'):
            print(podatak)
            client_socket.send(odigraj(matGl,0).encode()) # 0 - prvi igrac na potezu
        elif(prefiks == '%dru'):
            print(podatak)
            client_socket.send(odigraj(matGl,1).encode()) # 1 - drugi igrac na potezu
        elif(prefiks == '%end'):
            print(podatak)
            break
        else:
            print(podatak)
# ========================
def main_ConnectTo():
    server_address = 'localhost'
    server_port = 17510

    client_socket = socket(AF_INET, SOCK_STREAM)

    print('>> Konektujem se na server . . . ')
    brojPokusaja = 0
    while brojPokusaja < 3:
        brojPokusaja += 1
        try:
            client_socket.connect((server_address, server_port))
            print('>> Konekcija uspostavljena!')
            break
        except:
            print('>> Konekcija NIJE uspostavljena!')
            print('>> Pokusavam ponovo za 5 sekundi . . . ')
            sleep(5)

    while True:
        str = client_socket.recv(4096).decode()
        print(str)
        if(str == '>> Unesite korisnicko ime:'):
            ime = input()
            client_socket.send(ime.encode())
        if('srecno' in str):
            igraj(client_socket)
            break

    print('>> Prekidam konekciju . . .')
    client_socket.close()
    print('>> Konekcija je uspesno prekinuta.')

# ========================

main_ConnectTo()