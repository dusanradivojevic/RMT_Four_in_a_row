from time import sleep
import json

# ========================
def salji_1(igrac, podatak, prefiks):
    podatak = '>> ' + podatak
    data = json.dumps({"prefiks": prefiks, "podatak": podatak})
    igrac.clientSocket.send(data.encode())

def salji_2(igrac1, igrac2, podatak, prefiks = ''):
    # Salje isti podatak igracima
    if(prefiks != '%mat'):
        podatak = '>> ' + podatak

    data = json.dumps({"prefiks":prefiks, "podatak":podatak})
    igrac1.clientSocket.send(data.encode())
    sleep(0.1)
    igrac2.clientSocket.send(data.encode())
# ========================
def unesiIzbor(mat, redni_br_igraca, kolona):
    kolona = int(kolona)

    for i in range(6):
        if(i < 5 and mat[i + 1][kolona] == ' '):
            continue
        else:
            if (redni_br_igraca == 0):
                mat[i][kolona] = 'X'
            else:
                mat[i][kolona] = 'O'

    return mat
# ========================
def igraj(mat, prvi, drugi, brP):
    salji_2(prvi, drugi, '', '%cls')
    salji_2(prvi, drugi, mat, '%mat')
    sleep(0.1)  # Da ne bi spojio podatak koji sadrzi matricu i obavestenje o tome ko je na potezu

    if(brP % 2 == 0):
        salji_1(prvi, prvi.name + ' je na potezu: ', '%prv')
        salji_1(drugi, prvi.name + ' je na potezu: ', '')
        s = prvi.clientSocket.recv(4096)

    else:
        salji_1(prvi, drugi.name + ' je na potezu: ', '')
        salji_1(drugi, drugi.name + ' je na potezu: ', '%dru')
        s = drugi.clientSocket.recv(4096)

    return unesiIzbor(mat, brP % 2, s.decode())

#    mat = json.loads(s.decode())
#    return mat.get("b")
# ========================
def zavrsi(mat, endSignal, prvi, drugi):
    salji_2(prvi, drugi, '', '%cls')
    salji_2(prvi, drugi, mat, '%mat')

    sleep(0.1)

    if (endSignal == 0):
        salji_2(prvi, drugi, '\n>> Igra je zavrsena NERESENO! Hvala na igri!', '%end')
        print(f">> Igra je uspesno zavrsena. {prvi.name} vs {drugi.name}, zavrsena je NERESENO!")
    elif (endSignal == 1):
        # Prvi igrac je pobednik
        salji_1(prvi, '\n>> Cestitam, pobedili ste! Hvala na igri!', '%end')
        salji_1(drugi, '\n>> Nazalost, pobedio/la je ' + prvi.name + '! Hvala na igri, vise srece drugi put!', '%end')
        print(f">> Igra je uspesno zavrsena. {prvi.name} vs {drugi.name}, pobednik je {prvi.name}!")
    else:
        salji_1(drugi, '\n>> Cestitam, pobedili ste! Hvala na igri!', '%end')
        salji_1(prvi, '\n>> Nazalost, pobedio/la je ' + drugi.name + '! Hvala na igri, vise srece drugi put!', '%end')
        print(f">> Igra je uspesno zavrsena. {prvi.name} vs {drugi.name}, pobednik je {drugi.name}!")

    sleep(3) # Da bi stigli da procitaju info
# ========================
def proveri(mat, znak):
    for i in range(6):
        for j in range(7):
            #dijagonalno u desno
            if(i + 3 < 6 and j + 3 < 7):
                if(mat[i][j] == znak and mat[i+1][j+1] == znak and
                        mat[i+2][j+2] == znak and mat[i+3][j+3] == znak):
                    return True
            #dijagonalno u levo
            if (i + 3 < 6 and j - 3 >= 0):
                if (mat[i][j] == znak and mat[i + 1][j - 1] == znak and
                        mat[i + 2][j - 2] == znak and mat[i + 3][j - 3] == znak):
                    return True
            #vodoravno
            if (j + 3 < 7):
                if (mat[i][j] == znak and mat[i][j + 1] == znak and
                        mat[i][j + 2] == znak and mat[i][j + 3] == znak):
                    return True
            #uspravno
            if (i + 3 < 6):
                if (mat[i][j] == znak and mat[i + 1][j] == znak and
                        mat[i + 2][j] == znak and mat[i + 3][j] == znak):
                    return True

    return False
# ========================
def daLiJeKraj(mat, brP, prvi, drugi):
    if (brP == 42):
        zavrsi(mat, 0, prvi, drugi)
    elif (brP % 2 != 0 and proveri(mat, 'X') == True):
        zavrsi(mat,1, prvi, drugi)
    elif (proveri(mat, 'O') == True):
        zavrsi(mat, 2, prvi, drugi)
    else:
        return False

    return True

# ========================
def main(igrac1, igrac2):
    mat = [[' ' for j in range(7)] for i in range(6)]
    brojPoteza = 0;

    while(daLiJeKraj(mat, brojPoteza, igrac1, igrac2) != True):
        mat = igraj(mat, igrac1, igrac2, brojPoteza)
        brojPoteza += 1

    # Ne gasim ovde konekciju vec na serveru

# ==========================

#main()