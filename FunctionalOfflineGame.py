import os

# ========================
def padanje(mat, redni_br_igraca, kolona):
    for i in range(6):
        os.system('cls')

        if (redni_br_igraca == 0):
            mat[i][kolona] = 'X'
        else:
            mat[i][kolona] = 'O'

        prikazi_polje(mat)

        if (i == 5):
            break

        elif (mat[i + 1][kolona] == ' '):
            mat[i][kolona] = ' '

        else:
            break

# ========================
def prikazi_polje(mat):
    print("")

    #slova iznad
    for k in range(65,72):
        print(" " + chr(k), end='')
    print("")

    #matrica
    for i in range(6):
        print("",end=' ')
        for j in range(7):
            if(j < 6):
                print(mat[i][j],end='|')
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
def igraj(mat, prvi, drugi, brP):
    os.system('cls')
    prikazi_polje(mat)

    if(brP % 2 == 0):
        print(f'{prvi} je na potezu: ')
    else:
        print(f'{drugi} je na potezu: ')


    while(True):
        kolona = input()
        try:
            izbor = ord(kolona.upper()) #ascii predstava unetog slova

            if (izbor >= 65 and izbor < 72 and punaKolona(mat, izbor) == False):
                break
        except:
            print('Uneli ste pogresnu vrednost, probajte ponovo!')

    padanje(mat, brP % 2, izbor-65)
# ========================
def zavrsi(mat, endSignal, igrac = 'nebitno'):
    os.system('cls')
    prikazi_polje(mat)

    if (endSignal == 0):
        print("Igra je zavrsena NERESENO!")
    else:
        print(f'Pobednik je {igrac}!')
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
        zavrsi(mat, 0)
    elif (brP % 2 != 0 and proveri(mat, 'X') == True):
        zavrsi(mat,1, prvi)
    elif (proveri(mat, 'O') == True):
        zavrsi(mat, 2, drugi)
    else:
        return False

    return True

# ========================
def main():
    mat = [[' ' for j in range(7)] for i in range(6)]
    prviIgrac = input('\nIme prvog igraca: ')
    drugiIgrac = input('\nIme drugog igraca: ')
    brojPoteza = 0;

    print(f'\n{prviIgrac} ima oznaku "X", a {drugiIgrac} oznaku "O".\n==>Pritisnite bilo sta za START')
    os.system('pause')

    while(daLiJeKraj(mat, brojPoteza, prviIgrac, drugiIgrac) != True):
        igraj(mat, prviIgrac, drugiIgrac, brojPoteza)
        brojPoteza += 1

    input("\n\nPRITISNI BILO STA ZA KRAJ\n")
    os.system('pause')
# ==========================

main()