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

    data = json.dumps({"prefiks": prefiks, "podatak": podatak})
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
                break
            else:
                mat[i][kolona] = 'O'
                break

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

    if(s.decode() == '!q'):
        if(brP % 2 == 0):
            salji_1(drugi, prvi.name + ' je napustio igru! ', '%err')
            salji_1(prvi, 'Dovidjenja!', '%err')
        else:
            salji_1(prvi, drugi.name + ' je napustio igru! ', '%err')
            salji_1(drugi, 'Dovidjenja!', '%err')
        mat[0][0] = 'q'  # Signalna matrica
        return mat

    return unesiIzbor(mat, brP % 2, s.decode())

#    mat = json.loads(s.decode())
#    return mat.get("b")
# ========================
def zavrsi(mat, endSignal, prvi, drugi):

    if(endSignal == -1):
        print(f">> {prvi.name} je napustio igru! Igra je zavrsena.")
        sleep(3)
        return

    if(endSignal == -2):
        print(f">> {drugi.name} je napustio igru! Igra je zavrsena.")
        sleep(3)
        return

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
    if(mat[0][0] == 'q'):
        if(brP % 2 != 0):
            zavrsi(mat, -1, prvi, drugi) #  -1 -> Nagli prekid igre, prvi izasao (1)
        else:
            zavrsi(mat, -2, prvi, drugi)
        return True

    if (brP == 42):
        zavrsi(mat, 0, prvi, drugi)
    elif (brP % 2 != 0 and proveri(mat, 'X') == True):
        zavrsi(mat, 1, prvi, drugi)
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
        try:
            mat = igraj(mat, igrac1, igrac2, brojPoteza)
            brojPoteza += 1
        except:
            print(f"Igra {igrac1.name} vs {igrac2.name} je prekinuta usled prekida konekcije.")

            try:
                salji_1(igrac1, f'{igrac2.name} je napustio igru!', '%err')
            except:
                print()

            try:
                salji_1(igrac2, f'{igrac1.name} je napustio igru!', '%err')
            except:
                print()

            break

    # Ne gasim ovde konekciju vec na serveru

# ==========================

#main()