from tkinter import *
from tkinter import messagebox
import sqlite3
# import Main

conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

####Klasy
class Napis:

    def __init__(self,x,y,tekst,font_size):
        self.x=x
        self.y=y
        self.tekst=tekst
        self.font = font_size

    def pokaz(self):
        self.napis = Label(root,text=self.tekst, bg="#374E53", font=("Times New Roman",self.font))
        self.napis.place(relx=self.x, rely=self.y)

    def destroy(self):
        self.napis.destroy()

class Pole_do_wpisywania:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def pokaz(self):
        self.pole = Entry(root)
        self.pole.place(relwidth=0.4, relheight=0.05, relx=self.x, rely=self.y)

    def get(self):
        return self.pole.get()

    def destroy(self):
        self.pole.destroy()

class Przycisk:
    def __init__(self,szerokosc,wysokosc,x,y,tekst,funkcja):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.x=x
        self.y=y
        self.tekst=tekst
        self.funkcja = funkcja

    def pokaz(self):
        self.przycisk = Button(root, text=self.tekst, command=self.funkcja, highlightcolor="#000000")
        self.przycisk.place(relwidth=self.szerokosc, relheight=self.wysokosc, relx=self.x, rely=self.y)

    def destroy(self):
        self.przycisk.destroy()

class Trasa:
    def __init__(self,wybor,trasa_linii):
        self.wybor = wybor
        self.trasa_linii = trasa_linii

    def linie(self):
        j = 0
        pierwsza = []
        druga = []
        pierwsza.append([self.trasa_linii[0][0], self.trasa_linii[0][1]])
        for i in range(1, len(trasa_linii)):
            if j == 0:
                if self.trasa_linii[i][0] == 0:
                    j += 1
                    druga.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
                    continue
                else:
                    pierwsza.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
            if j == 1:
                if self.trasa_linii[i][0] == 0:
                    j += 1
                else:
                    druga.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
            i += 1
        i = 0

        napis1 = " "
        napis2 = " "
        napis3 = " "
        napis4 = " "

        if self.wybor == 1:
            for i in range(len(pierwsza)):
                if i <= int(len(pierwsza) / 2):
                    napis1 += str(pierwsza[i][0]) + " " + pierwsza[i][1] + "\n"
                else:
                    napis2 += str(pierwsza[i][0]) + " " + pierwsza[i][1] + "\n"
                i += 1
        if self.wybor == 2:
            for i in range(len(druga)):
                if i <= int(len(druga) / 2):
                    napis3 += str(druga[i][0]) + " " + druga[i][1] + "\n"
                else:
                    napis4 += str(druga[i][0]) + " " + druga[i][1] + "\n"

        # Napisy
        if self.wybor == 1:
            self.wypisz_trase_napis1 = Napis(0.15, 0.1, napis1, 14)
            self.wypisz_trase_napis1.pokaz()

            self.wypisz_trase_napis2 = Napis(0.55, 0.1, napis2, 14)
            self.wypisz_trase_napis2.pokaz()
        if self.wybor == 2:
            self.wypisz_trase_napis3 = Napis(0.15, 0.1, napis3, 14)
            self.wypisz_trase_napis3.pokaz()

            self.wypisz_trase_napis4 = Napis(0.55, 0.1, napis4, 14)
            self.wypisz_trase_napis4.pokaz()

    def destroy(self):
        try:
            self.wypisz_trase_napis1.destroy()
            self.wypisz_trase_napis2.destroy()
        except:
            pass
        try:
            self.wypisz_trase_napis3.destroy()
            self.wypisz_trase_napis4.destroy()
        except:
            pass


### Funkcje

#Opisy
def NapisyWyszukiwanie():
    global Przystanek_poczatkowy_tekst
    Przystanek_poczatkowy_tekst = Napis(0.3,0.32,"Przystanek początkowy:",12)
    Przystanek_poczatkowy_tekst.pokaz()

    global Przystanek_koncowy_tekst
    Przystanek_koncowy_tekst = Napis(0.3,0.42,"Przystanek końcowy",12)
    Przystanek_koncowy_tekst.pokaz()

    global Kara_tekst
    Kara_tekst = Napis(0.3,0.52,"Kara za przesiadkę:",12)
    Kara_tekst.pokaz()

    global Linia_tekst
    Linia_tekst = Napis(0.3,0.75,"Wybierz linie",12)
    Linia_tekst.pokaz()

#Pola do wpisywania danych
def Pola():
    global poczatkowy
    poczatkowy = Pole_do_wpisywania(0.3,0.35)
    poczatkowy.pokaz()

    global koncowy
    koncowy = Pole_do_wpisywania(0.3,0.45)
    koncowy.pokaz()

    global przesiadka
    przesiadka = Pole_do_wpisywania(0.3,0.55)
    przesiadka.pokaz()

    global linia
    linia = Pole_do_wpisywania(0.3,0.78)
    linia.pokaz()

#Przyciski
def przyciskiWyszukiwanie():
    global szukaj_button
    szukaj_button = Przycisk(0.2, 0.05, 0.4, 0.65, "Szukaj połączeń",pobierz_wartosci_droga)
    szukaj_button.pokaz()

    global trasa_button
    trasa_button = Przycisk(0.2, 0.05, 0.4, 0.88,'Pokaż trasę linii', pobierz_wartosci_linia)
    trasa_button.pokaz()


#Funkcja zamknij
def zamknij():
    response = messagebox.askokcancel("Potwierdzenie","Czy na pewno chcesz zamknąć program?")
    if response == True:
        root.quit()

def trasaLinii(linia):
    linia=(linia,)
    VariantID = []
    postoj = c.execute("SELECT Id FROM Variants WHERE LineName=?", linia)
    for row in postoj:
        VariantID.append(row[0])
    VariantID = list(set(VariantID))

    droga = []
    for i in range(len(VariantID)):
        postoj = c.execute("SELECT No, StopName FROM Routes  WHERE VariantID=?", (VariantID[i],))
        for row in postoj:
            droga.append([row[0], row[1]])
    return droga

def pobierz_wartosci_droga():

    #Pobranie wartości z pól + kontrola wpisywanych wartości
    start = poczatkowy.get()
    postoj = c.execute("SELECT Name FROM Stops")
    for rows in postoj:
        if start == rows[0]:
            start = rows[0]
            break
    else:
        start = 0

    end = koncowy.get()
    postoj = c.execute("SELECT Name FROM Stops")
    for rows in postoj:
        if end == rows[0]:
            end = rows[0]
            break
    else:
        end = 0

    kara = przesiadka.get()
    try:
        kara=float(kara)
        if (kara>=0 or kara<=100):
            kara = float(kara)
    except:
        kara = -1

    #Zniszczenie pól
    if start != 0 and end!= 0 and kara !=-1:
        poczatkowy.destroy()
        koncowy.destroy()
        przesiadka.destroy()
        Przystanek_poczatkowy_tekst.destroy()
        Przystanek_koncowy_tekst.destroy()
        Kara_tekst.destroy()
        szukaj_button.destroy()
        Linia_tekst.destroy()
        linia.destroy()
        trasa_button.destroy()

        #Wypisanie wyników
        trasa = Label(root,text="Trasa " + start + " - " +end + " z karą za przesiadkę równą " + str(kara),bg="#374E53", font=("Times New Roman",16))
        trasa.place(relx=0.25,rely=0.1)

def wroc():
    trasa_napis.destroy()
    exit.destroy()
    again.destroy()
    odwroc.destroy()
    jakaDroga.destroy()

    NapisyWyszukiwanie()
    Pola()
    przyciskiWyszukiwanie()

def odwrocTrase():
    wybor = jakaDroga.wybor
    jakaDroga.destroy()
    if wybor == 1:
        jakaDroga.wybor=2
        jakaDroga.linie()
        # jakaDroga = Trasa(2,trasaLinii)
    elif wybor==2:
        jakaDroga.wybor = 1
        jakaDroga.linie()
        # jakaDroga = Trasa(1,trasaLinii)

def pobierz_wartosci_linia():
    global trasa_linii

    droga = linia.get()
    try:
        trasa = int(droga)
        postoj = c.execute("SELECT Name FROM Lines")
        for rows in postoj:
            if droga == rows[0]:
                droga = rows[0]
                break
        else:
            droga = -1
    except:
        droga = -1

    # Zniszczenie pól

    if droga != -1:
        poczatkowy.destroy()
        koncowy.destroy()
        przesiadka.destroy()
        Przystanek_poczatkowy_tekst.destroy()
        Przystanek_koncowy_tekst.destroy()
        Kara_tekst.destroy()
        szukaj_button.destroy()
        Linia_tekst.destroy()
        linia.destroy()
        trasa_button.destroy()

        trasa_linii = trasaLinii(droga)
        # Wypisanie wyników
        global trasa_napis
        trasa_napis= Napis(0.43,0.05,"Trasa linii:" + str(droga),16)
        trasa_napis.pokaz()

    j=0
    pierwsza = []
    druga = []
    pierwsza.append([trasa_linii[0][0], trasa_linii[0][1]])
    for i in range(1, len(trasa_linii)):
        if j == 0:
            if trasa_linii[i][0] == 0:
                j += 1
                druga.append([trasa_linii[i][0], trasa_linii[i][1]])
                continue
            else:
                pierwsza.append([trasa_linii[i][0], trasa_linii[i][1]])
        if j == 1:
            if trasa_linii[i][0] == 0:
                j += 1
            else:
                druga.append([trasa_linii[i][0], trasa_linii[i][1]])
    i = 0

    global wybor
    wybor = 2

    global jakaDroga
    jakaDroga = Trasa(wybor, trasa_linii)
    jakaDroga.linie()

    #Przyciski
    global exit
    exit = Przycisk(0.2,0.05,0.7,0.85,"Zamknij",zamknij)

    global again
    again = Przycisk(0.2,0.05,0.4,0.85,"Wróć",wroc)

    global odwroc
    odwroc = Przycisk(0.2,0.05,0.1,0.85,"Odwróc",odwrocTrase)

    exit.pokaz()
    again.pokaz()
    odwroc.pokaz()


###### GŁÓWNY PROGRAM ######
root = Tk()
root.geometry("1000x1000")

canvas= Canvas(root, height=1000, width=1000, bg="#374E53")
canvas.pack()


NapisyWyszukiwanie()
Pola()
przyciskiWyszukiwanie()



root.mainloop()
c.close()
conn.close()