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
def unesiKolonu():
    while True:
        kol = input()
        kol = kol.upper()

        if(kol == 'A' or kol == 'B' or kol == 'C' or kol == 'D' or kol == 'E' or kol == 'F' or kol == 'G'):
            return kol
        else:
            print('>> Uneli ste pogresnu vrednost, probajte ponovo!')

def odigraj(mat, brIgraca):
    while True:
        kolona = unesiKolonu()
        try:
            izbor = ord(kolona)  # ascii predstava unetog slova

            if (punaKolona(mat, izbor) == False):
                break
        except:
            print('>> Kolona je puna, probajte ponovo!')

    unesiIzbor(mat, brIgraca, izbor)
    return json.dumps({"b": mat})
# ========================
def igraj(client_socket):
    try:
        matGl = []
        while True:
            s = client_socket.recv(4096).decode()
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
                try:
                    client_socket.send(odigraj(matGl,0).encode()) # 0 - prvi igrac na potezu
                except Exception as e:
                    print('\n\n Greska %prv send')
                    print(str(e))
            elif(prefiks == '%dru'):
                print(podatak)
                client_socket.send(odigraj(matGl,1).encode()) # 1 - drugi igrac na potezu
            elif(prefiks == '%end'):
                print(podatak)
                break
            else:
                print(podatak)
    except Exception as e:
        print('\n\n Greska na kraju igraj metode')
        print(str(e))
        sleep(40)
# ========================
def unesiIme():
    while True:
        ime = input()

        if(len(ime) < 3):
            print('>> Ime mora sadrzati vise od 3 karaktera! Probajte ponovo.')
        else:
            return ime
# ========================
def main_ConnectTo():
    server_address = 'localhost'
    server_port = 17510

    client_socket = socket(AF_INET, SOCK_STREAM)

    print('>> Konektujem se na server . . . ')
    brojPokusaja = 0
    while brojPokusaja < 3:
        try:
            client_socket.connect((server_address, server_port))
            print('>> Konekcija uspostavljena!\n')
            break
        except:
            print('>> Konekcija NIJE uspostavljena!')
            print('>> Pokusavam ponovo za 5 sekundi . . . ')
            sleep(5)
        brojPokusaja += 1

    while True and brojPokusaja < 3:
        str = client_socket.recv(4096).decode()
        print(str)
        if(str == '>> Unesite korisnicko ime:'):
            ime = unesiIme()
            client_socket.send(ime.encode())
        if('srecno' in str):
            try:
                igraj(client_socket)
            except Exception as e:
                print('greska kod igraj')
                print(str(e))
            break

    print('>> Prekidam konekciju . . .')
    client_socket.close()
    print('>> Konekcija je uspesno prekinuta.')

# ========================

main_ConnectTo()