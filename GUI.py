import tkinter as tk
from tkinter import messagebox
import sqlite3
import copy
import Szukaj
from collections import defaultdict

FILE = "Logo.png"
BG_COLOR = "#aaaaaa"
FONT = "Times New Roman"

conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()


####Klasy
class Logo:
    def __init__(self):
        self.photo = tk.PhotoImage(file=FILE, )

    def pokaz(self):
        self.logo = tk.Label(root, image=self.photo, bd=0)
        self.logo.place(relx=0, rely=0)

    def destroy(self):
        self.logo.destroy()


class Napis:

    def __init__(self, x, y, tekst, font_size):
        self.x = x
        self.y = y
        self.tekst = tekst
        self.font = font_size

    def pokaz(self):
        self.napis = tk.Label(root, text=self.tekst, bg=BG_COLOR, font=(FONT, self.font))
        self.napis.place(relx=self.x, rely=self.y)

    def destroy(self):
        self.napis.destroy()


class Blad(Napis):

    def __init__(self, x, y, tekst, font_size):
        self.x = x
        self.y = y
        self.tekst = tekst
        self.font = font_size

    def pokaz(self):
        self.napis = tk.Label(root, text=" ", bg=BG_COLOR, font=(FONT, self.font), foreground='red')
        self.napis.place(relx=self.x, rely=self.y)

    def config(self):
        self.napis.config(text=self.tekst)


class Pole_do_wpisywania:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pokaz(self):
        self.pole = tk.Entry(root)
        self.pole.place(relwidth=0.4, relheight=0.05, relx=self.x, rely=self.y)

    def get(self):
        return self.pole.get()

    def destroy(self):
        self.pole.destroy()


class Przycisk:
    def __init__(self, width, height, x, y, tekst, funkcja):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.tekst = tekst
        self.funkcja = funkcja

    def pokaz(self):
        self.przycisk = tk.Button(root, text=self.tekst, command=self.funkcja)
        self.przycisk.place(relwidth=self.width, relheight=self.height, relx=self.x, rely=self.y)

    def destroy(self):
        self.przycisk.destroy()


class Trasa:
    def __init__(self, wybor, trasa_linii):
        self.wybor = wybor
        self.trasa_linii = trasa_linii

    def linie(self):
        j = 0
        pierwsza = []
        druga = []
        pierwsza.append([self.trasa_linii[0][0], self.trasa_linii[0][1]])
        for i in range(1, len(self.trasa_linii)):
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


class DrogaZPrzystankami:
    def __init__(self, start, koniec, gotowe, kara, trasa, ile, wynik, tmp):
        self.start = start
        self.koniec = koniec
        self.gotowe = gotowe
        self.kara = kara
        self.trasa = trasa
        self.ile = ile
        self.wynik = wynik
        self.tmp = tmp

    def wypisz_napis(self):
        koncowy_napis = " "
        for i in range(self.tmp, self.ile):
            pierwszy = self.start[0]
            z = i + 1
            tmp = str(z)
            koncowy_napis += "\n\nTrasa nr " + tmp + "\t\tWynik: " + str(self.wynik[self.ile - 1])
            koncowy_napis += "\nLinią " + str(self.gotowe[i][0]) + " na trasie: "
            for j in range(len(self.gotowe[i]) - 1):
                if self.gotowe[i][j] != self.gotowe[i][j + 1]:
                    koncowy_napis = koncowy_napis + str(pierwszy) + "-" + self.trasa[j + 1]
                    koncowy_napis = koncowy_napis + "\n"
                    koncowy_napis = koncowy_napis + "Linią " + str(self.gotowe[i][j + 1])
                    koncowy_napis = koncowy_napis + " na trasie"
                    pierwszy = self.trasa[j + 1]
            else:
                koncowy_napis = koncowy_napis + str(pierwszy) + "-" + str(self.koniec[0])

        self.x = Napis(0.36, 0.18, koncowy_napis, 12)
        self.x.pokaz()

    def destroy(self):
        self.x.destroy()

# self.zmienna = DrogaZPrzystankamiBezposrednia(self.start, self.end, self.gotowe, self.kara, self.x, doIlu, self.wynik, self.tmp)
class DrogaZPrzystankamiBezposrednia:
    def __init__(self, start, koniec, kara, BothVariantLine, ile, wynik, tmp):
        self.start = start
        self.koniec = koniec
        self.BothVariantLine = BothVariantLine
        self.kara = kara
        self.ile = ile
        self.wynik = wynik
        self.tmp = tmp

    def wypisz_napis(self):
        koncowy_napis = " "
        for i in range(self.tmp,self.ile):
            z = i + 1
            koncowy_napis += "\n\nTrasa nr " + str(z) + "\t\tWynik: " + str(self.wynik[i])
            koncowy_napis += "\nLinią " + str(self.BothVariantLine[i]) + " na trasie: " + str(self.start[0]) + "-" + str(self.koniec[0]) + "\n"
        if self.ile == 0:
            koncowy_napis += "\n\nBrak bezposrednich polaczen na danej trasie "
        self.x = Napis(0.36, 0.18, koncowy_napis, 12)
        self.x.pokaz()

    def destroy(self):
        self.x.destroy()


class GUI(Trasa, Szukaj.WszystkieTrasy, Szukaj.Bezposrednie, DrogaZPrzystankami):
    def __init__(self):
        self.logo()
        self.NapisyWyszukiwanie()
        self.Pola()
        self.przyciskiWyszukiwanie()

        self.istnieje = 0
        self.tmp = 0
        self.tymczasowa = 1

        self.blad = Blad(0.73, 0.79, "Taka linia nie isnieje", 14)
        self.blad.pokaz()

        self.bladStart = Blad(0.73, 0.36, "Taki przystanek nie isnieje", 14)
        self.bladStart.pokaz()

        self.bladKoniec = Blad(0.73, 0.46, "Taka przystanek nie isnieje", 14)
        self.bladKoniec.pokaz()

        self.bladKara = Blad(0.73, 0.56, "Wprowadzono zle dane", 14)
        self.bladKara.pokaz()

    # Opisy
    def logo(self):
        self.zdjecie = Logo()
        self.zdjecie.pokaz()

    def NapisyWyszukiwanie(self):
        self.Przystanek_poczatkowy_tekst = Napis(0.3, 0.32, "Przystanek początkowy:", 12)
        self.Przystanek_poczatkowy_tekst.pokaz()

        self.Przystanek_koncowy_tekst = Napis(0.3, 0.42, "Przystanek końcowy", 12)
        self.Przystanek_koncowy_tekst.pokaz()

        self.Kara_tekst = Napis(0.3, 0.52, "Kara za przesiadkę:", 12)
        self.Kara_tekst.pokaz()

        self.Linia_tekst = Napis(0.3, 0.75, "Wybierz linie", 12)
        self.Linia_tekst.pokaz()

    # Pola do wpisywania danych
    def Pola(self):
        self.poczatkowy = Pole_do_wpisywania(0.3, 0.35)
        self.poczatkowy.pokaz()

        self.koncowy = Pole_do_wpisywania(0.3, 0.45)
        self.koncowy.pokaz()

        self.przesiadka = Pole_do_wpisywania(0.3, 0.55)
        self.przesiadka.pokaz()

        self.linia = Pole_do_wpisywania(0.3, 0.78)
        self.linia.pokaz()

    # Przyciski
    def przyciskiWyszukiwanie(self):
        self.szukaj_button = Przycisk(0.19, 0.05, 0.3, 0.65, "Szukaj najkrótszych polaczen",
                                      self.pobierz_wartosci_droga)
        self.szukaj_button.pokaz()

        self.szukajBezposrednie_button = Przycisk(0.19, 0.05, 0.51, 0.65, "Szukaj bezpośrednich polaczen",
                                                  self.bezposrednie_pobierz_wartosci_droga)
        self.szukajBezposrednie_button.pokaz()

        self.trasa_button = Przycisk(0.2, 0.05, 0.4, 0.88, 'Pokaż trasę linii', self.pobierz_wartosci_linia)
        self.trasa_button.pokaz()

    # Funkcja zamknij
    def zamknij(self):
        response = messagebox.askokcancel("Potwierdzenie", "Czy na pewno chcesz zamknąć program?")
        if response == True:
            root.quit()

    def trasaLinii(self, linia):
        linia = (linia,)
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

    def getValue(self, pole):
        # Pobranie wartości z pól + kontrola wpisywanych wartości
        start = pole.get()
        postoj = c.execute("SELECT Name FROM Stops")
        for rows in postoj:
            if start == rows[0]:
                return start
        else:
            return 0

    def sprawdzKare(self):
        self.kara = self.przesiadka.get()
        try:
            self.kara = float(self.kara)
            if (self.kara >= 0 or self.kara <= 100):
                self.kara = float(self.kara)
                return self.kara
        except:
            return -1

    def zniszczPoczątkowy(self):
        self.poczatkowy.destroy()
        self.koncowy.destroy()
        self.przesiadka.destroy()
        self.Przystanek_poczatkowy_tekst.destroy()
        self.Przystanek_koncowy_tekst.destroy()
        self.Kara_tekst.destroy()
        self.szukaj_button.destroy()
        self.szukajBezposrednie_button.destroy()
        self.Linia_tekst.destroy()
        self.linia.destroy()
        self.trasa_button.destroy()
        self.zdjecie.destroy()

    def pobierz_wartosci_droga(self):

        # Pobranie wartości + obsługa błędów
        self.start = self.getValue(self.poczatkowy)
        self.end = self.getValue(self.koncowy)
        self.kara = self.sprawdzKare()

        if self.start == 0:
            self.bladStart.config()

        if self.end == 0:
            self.bladKoniec.config()

        if self.kara == -1:
            self.bladKara.config()

        if self.start != 0:
            self.bladStart.destroy()
            self.bladStart = Blad(0.73, 0.36, "Taki przystanek nie isnieje", 14)
            self.bladStart.pokaz()

        if self.end != 0:
            self.bladKoniec.destroy()
            self.bladKoniec = Blad(0.73, 0.46, "Taka przystanek nie isnieje", 14)
            self.bladKoniec.pokaz()

        if self.kara != -1:
            self.bladKara.destroy()
            self.bladKara = Blad(0.73, 0.56, "Wprowadzono zle dane", 14)
            self.bladKara.pokaz()

        if self.start != 0 and self.end != 0 and self.kara != -1:
            # Zniszczenie pól
            self.zniszczPoczątkowy()
            self.dzialanie()

    def bezposrednie_pobierz_wartosci_droga(self):

        # Pobranie wartości + obsługa błędów
        self.start = self.getValue(self.poczatkowy)
        self.end = self.getValue(self.koncowy)
        self.kara = self.sprawdzKare()

        if self.start == 0:
            self.bladStart.config()

        if self.end == 0:
            self.bladKoniec.config()

        if self.kara == -1:
            self.bladKara.config()

        if self.start != 0:
            self.bladStart.destroy()
            self.bladStart = Blad(0.73, 0.36, "Taki przystanek nie isnieje", 14)
            self.bladStart.pokaz()

        if self.end != 0:
            self.bladKoniec.destroy()
            self.bladKoniec = Blad(0.73, 0.46, "Taka przystanek nie isnieje", 14)
            self.bladKoniec.pokaz()

        if self.kara != -1:
            self.bladKara.destroy()
            self.bladKara = Blad(0.73, 0.56, "Wprowadzono zle dane", 14)
            self.bladKara.pokaz()

        if self.start != 0 and self.end != 0 and self.kara != -1:
            # Zniszczenie pól
            self.zniszczPoczątkowy()
            self.dzialanieBezposrednie()

    def wypisz(self):
        gotoweSet = copy.deepcopy(self.gotowe)
        tmp = self.wynik[0]
        i = 0
        for i in range(len(gotoweSet)):
            gotoweSet[i] = set(gotoweSet[i])
        for i in range(len(self.wynik)):
            if self.wynik[i] <= tmp:
                i += 1
            else:
                break
        ile = i
        for i in range(ile):
            pierwszy = self.start[0]
            for j in range(len(self.gotowe[i]) - 1):
                if self.gotowe[i][j] != self.gotowe[i][j + 1]:
                    pierwszy = self.trasa[j + 1]
        return i

    def dzialanie(self):
        # Wypisanie wyników
        self.trasaSzukaj = Napis(0.27, 0.1,
                                 "Trasa " + self.start + " - " + self.end + " z karą za przesiadkę równą " + str(
                                     self.kara), 16)
        self.trasaSzukaj.pokaz()

        self.start = (self.start,)
        self.end = (self.end,)
        # Szukanie trasy
        klasa = Szukaj.WszystkieTrasy()
        startID = (klasa.sprawdz_ID(self.start),)
        koniecID = (klasa.sprawdz_ID(self.end),)

        # Możliwe punkty zatrzymania autobusow na przystanku
        StartPointID = klasa.sprawdz_PointID(startID)
        EndPointID = klasa.sprawdz_PointID(koniecID)

        # Możliwe sposoby przejazdy linii przez dany przystanek
        StartVariantID = klasa.sprawdz_VariantID(StartPointID)
        EndVariantID = klasa.sprawdz_VariantID(EndPointID)

        # Wspolne kombinacje polaczen
        BothVariantID = klasa.sprawdz_BothVariantID(StartVariantID, EndVariantID)

        # #Zamienienie elementow listy z int na str
        klasa.zamien_elementy_int_na_str(StartPointID)
        klasa.zamien_elementy_int_na_str(BothVariantID)
        klasa.zamien_elementy_int_na_str(EndPointID)

        z = []
        z = klasa.SzukajWszystkieDrogi(StartPointID, EndPointID)
        kolejnePrzystanki = klasa.wybierzUnikalne(z)
        self.trasa = copy.deepcopy(kolejnePrzystanki)
        kolejnePrzystanki = klasa.wybierzUnikalneTrasy(kolejnePrzystanki)
        self.x = klasa.wybierzNajkrotszy(kolejnePrzystanki)
        self.x = [i for k in self.x for i in k]

        self.dlugosc = len(self.x) - 1
        wybierzlinie = []
        pierwsze = klasa.szukajPolaczen(self.x[0], self.x[1])

        self.gotowe = klasa.jakieLinieNaTrasie(pierwsze, self.x, wybierzlinie, self.dlugosc)
        self.wynik = klasa.policz(self.gotowe, self.kara)

        self.ile = self.wypisz() + 1

        if self.ile < 8:
            self.zmienna = DrogaZPrzystankami(self.start, self.end, self.gotowe, self.kara, self.x, self.ile, self.wynik,self.tmp)
            self.zmienna.wypisz_napis()

        else:
            self.zmienna = DrogaZPrzystankami(self.start, self.end, self.gotowe, self.kara, self.x, 7, self.wynik, self.tmp)
            self.zmienna.wypisz_napis()
            self.tmp += 7

            self.wiecej = Przycisk(0.3, 0.05, 0.35, 0.78, "Pokaż więcej", self.pokazWiecej)
            self.wiecej.pokaz()
            self.istnieje = 1

        # Przyciski

        self.wyjscie = Przycisk(0.3, 0.05, 0.15, 0.85, "Zamknij", self.zamknij)
        self.wyjscie.pokaz()

        self.powrot = Przycisk(0.3, 0.05, 0.55, 0.85, "Wróć", self.wrocTrasa)
        self.powrot.pokaz()

    def pokazWiecej(self):
        self.zmienna.destroy()
        if self.tmp > self.ile:
            self.tmp = 0
            self.tymczasowa = 0
        self.tymczasowa += 1
        doIlu = 7 * self.tymczasowa
        if doIlu > self.ile:
            doIlu = self.ile
        self.zmienna = DrogaZPrzystankami(self.start, self.end, self.gotowe, self.kara, self.x, doIlu, self.wynik, self.tmp)
        self.zmienna.wypisz_napis()
        self.tmp += 7


    def dzialanieBezposrednie(self):
        # Wypisanie wyników
        self.trasaSzukaj = Napis(0.27, 0.1,
                                 "Trasa " + self.start + " - " + self.end + " z karą za przesiadkę równą " + str(
                                     self.kara), 16)
        self.trasaSzukaj.pokaz()

        self.start = (self.start,)
        self.end = (self.end,)
        # Szukanie trasy
        klasa = Szukaj.Bezposrednie()
        startID = (klasa.sprawdz_ID(self.start),)
        koniecID = (klasa.sprawdz_ID(self.end),)

        # Możliwe punkty zatrzymania autobusow na przystanku
        StartPointID = klasa.sprawdz_PointID(startID)
        EndPointID = klasa.sprawdz_PointID(koniecID)

        # Możliwe sposoby przejazdy linii przez dany przystanek
        StartVariantID = klasa.sprawdz_VariantID(StartPointID)
        EndVariantID = klasa.sprawdz_VariantID(EndPointID)

        # Wspolne kombinacje polaczen
        BothVariantID = klasa.sprawdz_BothVariantID(StartVariantID, EndVariantID)

        id = (BothVariantID,)
        self.BothVariantLine = klasa.zamien_ID_na_nr_linii(id)

        klasa.zamien_elementy_int_na_str(StartPointID)
        klasa.zamien_elementy_int_na_str(BothVariantID)
        klasa.zamien_elementy_int_na_str(EndPointID)

        self.No = klasa.ktory_przystanek_linii(StartPointID, BothVariantID)
        self.No2 = klasa.ktory_przystanek_linii(EndPointID, BothVariantID)

        przystanki = klasa.wybierz_odpowiednie_przystanki(self.No, self.No2)
        przystankiStart = przystanki[0]
        przystankiEnd = przystanki[1]

        self.IloscPrzystankow = self.ile_przystankow(przystankiStart, przystankiEnd)
        self.ileTras = len(self.BothVariantLine)

        if self.ileTras < 8:
            self.zmienna = DrogaZPrzystankamiBezposrednia(self.start, self.end, self.kara, self.BothVariantLine, self.ileTras, self.IloscPrzystankow, self.tmp)
            self.zmienna.wypisz_napis()
        else:
            self.zmienna = DrogaZPrzystankamiBezposrednia(self.start, self.end, self.kara, self.BothVariantLine, 7, self.IloscPrzystankow, self.tmp)
            self.zmienna.wypisz_napis()
            self.tmp += 7

            # Przyciski
            self.wiecej = Przycisk(0.3, 0.05, 0.35, 0.78, "Pokaż więcej", self.pokazWiecejBezposrednie)
            self.wiecej.pokaz()
            self.istnieje = 1

        self.wyjscie = Przycisk(0.3, 0.05, 0.15, 0.85, "Zamknij", self.zamknij)
        self.wyjscie.pokaz()

        self.powrot = Przycisk(0.3, 0.05, 0.55, 0.85, "Wróć", self.wrocTrasa)
        self.powrot.pokaz()

    def pokazWiecejBezposrednie(self):
        self.zmienna.destroy()
        if self.tmp > self.ileTras:
            self.tmp = 0
            self.tymczasowa = 0
        self.tymczasowa += 1
        doIlu = 7 * self.tymczasowa
        if doIlu > self.ileTras:
            doIlu = self.ileTras
        self.zmienna = DrogaZPrzystankamiBezposrednia(self.start, self.end, self.kara, self.BothVariantLine, doIlu, self.IloscPrzystankow, self.tmp)
        self.zmienna.wypisz_napis()
        self.tmp += 7

    def wrocLinie(self):
        droga = -1
        self.blad = Blad(0.73, 0.79, "Taka linia nie isnieje", 14)
        self.blad.pokaz()
        self.trasa_napis.destroy()
        self.exit.destroy()
        self.again.destroy()
        self.odwroc.destroy()
        self.jakaDroga.destroy()

        self.logo()
        self.NapisyWyszukiwanie()
        self.Pola()
        self.przyciskiWyszukiwanie()

    def wrocTrasa(self):
        self.tymczasowa = 1
        self.tmp =0
        self.zmienna.destroy()
        self.trasaSzukaj.destroy()
        self.wyjscie.destroy()
        self.powrot.destroy()
        if self.istnieje == 1:
            self.wiecej.destroy()
            self.istnieje == 0

        self.logo()
        self.NapisyWyszukiwanie()
        self.Pola()
        self.przyciskiWyszukiwanie()

    def odwrocTrase(self):
        self.wybor = self.jakaDroga.wybor
        self.jakaDroga.destroy()
        if self.wybor == 1:
            self.jakaDroga.wybor = 2
            self.jakaDroga.linie()
            # jakaDroga = Trasa(2,trasaLinii)
        elif self.wybor == 2:
            self.jakaDroga.wybor = 1
            self.jakaDroga.linie()
            # jakaDroga = Trasa(1,trasaLinii)

    def pobierz_wartosci_linia(self):
        self.droga = self.linia.get()
        try:
            self.trasa = int(self.droga)
            postoj = c.execute("SELECT Name FROM Lines")
            for rows in postoj:
                if self.droga == rows[0]:
                    self.droga = rows[0]
                    break
            else:
                self.droga = -1
                self.blad.config()
        except:
            self.droga = -1
            self.blad.config()

        # Zniszczenie pól

        if self.droga != -1:
            self.blad.destroy()
            self.zdjecie.destroy()
            self.poczatkowy.destroy()
            self.koncowy.destroy()
            self.przesiadka.destroy()
            self.Przystanek_poczatkowy_tekst.destroy()
            self.Przystanek_koncowy_tekst.destroy()
            self.Kara_tekst.destroy()
            self.szukaj_button.destroy()
            self.szukajBezposrednie_button.destroy()
            self.Linia_tekst.destroy()
            self.linia.destroy()
            self.trasa_button.destroy()

            self.trasa_linii2 = Szukaj.Droga()
            self.trasa_linii = self.trasa_linii2.trasaLinii(self.droga)
            # Wypisanie wyników

            self.trasa_napis = Napis(0.43, 0.05, "Trasa linii:" + str(self.droga), 16)
            self.trasa_napis.pokaz()

            j = 0
            self.pierwsza = []
            self.druga = []
            self.pierwsza.append([self.trasa_linii[0][0], self.trasa_linii[0][1]])
            for i in range(1, len(self.trasa_linii)):
                if j == 0:
                    if self.trasa_linii[i][0] == 0:
                        j += 1
                        self.druga.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
                        continue
                    else:
                        self.pierwsza.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
                if j == 1:
                    if self.trasa_linii[i][0] == 0:
                        j += 1
                    else:
                        self.druga.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
            i = 0

            self.wybor = 2

            self.jakaDroga = Trasa(self.wybor, self.trasa_linii)
            self.jakaDroga.linie()

            # Przyciski
            self.exit = Przycisk(0.2, 0.05, 0.7, 0.85, "Zamknij", self.zamknij)

            self.again = Przycisk(0.2, 0.05, 0.4, 0.85, "Wróć", self.wrocLinie)

            self.odwroc = Przycisk(0.2, 0.05, 0.1, 0.85, "Odwróc", self.odwrocTrase)

            self.exit.pokaz()
            self.again.pokaz()
            self.odwroc.pokaz()


###### GŁÓWNY PROGRAM ######
root = tk.Tk()
root.geometry("1000x1000")

canvas = tk.Canvas(root, height=1000, width=1000, bg=BG_COLOR)
canvas.pack()

GUI()
# NapisyWyszukiwanie()
# Pola()
# przyciskiWyszukiwanie()


root.mainloop()
c.close()
conn.close()