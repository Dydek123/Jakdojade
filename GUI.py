""" The module contains the functions needed for creating GUI

    Typical usage example:
    GUI()
"""
import tkinter as tk
from tkinter import messagebox
import sqlite3
import copy
import szukaj

FILE = "Logo.png"
BG_COLOR = "#aaaaaa"
FONT = "Times New Roman"

conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()


####Klasy
class Logo:
    """Creates logo on main screen."""

    def __init__(self):
        self.photo = tk.PhotoImage(file=FILE, )
        self.logo = tk.Label(root, image=self.photo, bd=0)

    def pokaz(self):
        """Creates logo."""
        self.logo.place(relx=0, rely=0)

    def destroy(self):
        """Destroys logo"""
        self.logo.destroy()


class Napis:
    """Creates description for entries"""

    def __init__(self, pozycja_x, pozycja_y, tekst, font_size):
        self.pozycja_x = pozycja_x
        self.pozycja_y = pozycja_y
        self.tekst = tekst
        self.font = font_size
        self.napis = tk.Label(root, text=self.tekst, bg=BG_COLOR, font=(FONT, self.font))

    def pokaz(self):
        """Creates string."""
        self.napis.place(relx=self.pozycja_x, rely=self.pozycja_y)

    def destroy(self):
        """Destroys string."""
        self.napis.destroy()


class Blad(Napis):
    """Creates string for errors."""

    def __init__(self, pozycja_x, pozycja_y, tekst, font_size):
        self.pozycja_x = pozycja_x
        self.pozycja_y = pozycja_y
        self.tekst = tekst
        self.font = font_size
        super().__init__(self.pozycja_x, self.pozycja_y, self.tekst, self.font)

    def pokaz(self):
        """Creates label."""
        self.napis = tk.Label(root, text=" ", bg=BG_COLOR, font=(FONT, self.font), foreground='red')
        self.napis.place(relx=self.pozycja_x, rely=self.pozycja_y)

    def config(self):
        """Change label text."""
        self.napis.config(text=self.tekst)


class PoleDoWpisywania:
    """Creates entry space."""

    def __init__(self, pozycja_x, pozycja_y):
        self.pozycja_x = pozycja_x
        self.pozycja_y = pozycja_y
        self.pole = tk.Entry(root)

    def pokaz(self):
        """Creates entry."""
        self.pole.place(relwidth=0.4, relheight=0.05, relx=self.pozycja_x, rely=self.pozycja_y)

    def get(self):
        """Gets entry value."""
        return self.pole.get()

    def destroy(self):
        """Destroy entry."""
        self.pole.destroy()


class Przycisk:
    """Creates button for given arguments."""

    def __init__(self, width, height, pozycja_x, pozycja_y, tekst, funkcja):
        self.width = width
        self.height = height
        self.pozycja_x = pozycja_x
        self.pozycja_y = pozycja_y
        self.tekst = tekst
        self.funkcja = funkcja
        self.przycisk = tk.Button(root, text=self.tekst, command=self.funkcja)

    def pokaz(self):
        """Creates button."""
        self.przycisk.place(relwidth=self.width, relheight=self.height,
                            relx=self.pozycja_x, rely=self.pozycja_y)

    def destroy(self):
        """Destroy button."""
        self.przycisk.destroy()


class Trasa:
    """Searches for all bus stops for given line."""

    def __init__(self, wybor, trasa_linii):
        self.wybor = wybor
        self.trasa_linii = trasa_linii

    def linie(self):
        """Prints all bus stops for given line."""
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

        rozmiar1 = len(pierwsza)
        rozmiar2 = len(druga)
        if self.wybor == 1:
            for i in range(rozmiar1):
                if i <= int(rozmiar1 / 2):
                    napis1 += "{} {} \n".format(str(pierwsza[i][0]), pierwsza[i][1])
                else:
                    napis2 += "{} {} \n".format(str(pierwsza[i][0]), pierwsza[i][1])
                i += 1
        if self.wybor == 2:
            for i in range(rozmiar2):
                if i <= int(rozmiar2 / 2):
                    napis3 += "{} {} \n".format(str(druga[i][0]), druga[i][1])
                else:
                    napis4 += "{} {} \n".format(str(druga[i][0]), druga[i][1])

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
        """Destroys strings."""
        try:
            self.wypisz_trase_napis1.destroy()
            self.wypisz_trase_napis2.destroy()
        except AttributeError:
            pass
        try:
            self.wypisz_trase_napis3.destroy()
            self.wypisz_trase_napis4.destroy()
        except AttributeError:
            pass


class DrogaZPrzystankami:
    """Searches for shortest routes between two bus stops with total score."""

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
        """Prints routes between two bus stops."""
        koncowy_napis = " "
        for i in range(self.tmp, self.ile):
            pierwszy = self.start[0]
            ktora_trasa = i + 1
            tmp = str(ktora_trasa)
            koncowy_napis += "\nTrasa nr {} \t\tWynik: {}".format(tmp,
                                                                  str(self.wynik[ktora_trasa - 1]))
            koncowy_napis += "\nLinią {} na trasie: ".format(str(self.gotowe[i][0]))
            for j in range(len(self.gotowe[i]) - 1):
                if self.gotowe[i][j] != self.gotowe[i][j + 1]:
                    koncowy_napis += "{}-{}\n".format(str(pierwszy), self.trasa[j + 1])
                    koncowy_napis += "Linią {} na trasie".format(str(self.gotowe[i][j + 1]))
                    pierwszy = self.trasa[j + 1]
                    # print(koncowy_napis)
            else:
                koncowy_napis += "{}-{}\n".format(str(pierwszy), str(self.koniec[0]))
                # print(koncowy_napis)

        self.wypisane_trasy = Napis(0.36, 0.18, koncowy_napis, 12)
        self.wypisane_trasy.pokaz()

    def destroy(self):
        """Destroy routes string."""
        self.wypisane_trasy.destroy()


class DrogaZPrzystankamiBezposrednia:
    """Searches for direct routes between two bus stops."""

    def __init__(self, start, koniec, kara, both_variant_line, ile, wynik, tmp):
        self.start = start
        self.koniec = koniec
        self.both_variant_line = both_variant_line
        self.kara = kara
        self.ile = ile
        self.wynik = wynik
        self.tmp = tmp

    def wypisz_napis(self):
        """Prints routes between two bus stops."""
        koncowy_napis = " "
        for i in range(self.tmp, self.ile):
            ktora_trasa = i + 1
            koncowy_napis += "\n\nTrasa nr {} \t\tWynik: {}".format(str(ktora_trasa),
                                                                    str(self.wynik[i]))
            koncowy_napis += "\nLinią {} na trasie: {}-{} \n".format(str(self.both_variant_line[i]),
                                                                     str(self.start[0]),
                                                                     str(self.koniec[0]))
        if self.ile == 0:
            koncowy_napis += "\n\nBrak bezposrednich polaczen na danej trasie "
        self.wypisane_przystanki = Napis(0.36, 0.18, koncowy_napis, 12)
        self.wypisane_przystanki.pokaz()

    def destroy(self):
        """Destroy route string."""
        self.wypisane_przystanki.destroy()


def zamknij():
    """Closes the programm."""
    response = messagebox.askokcancel("Potwierdzenie", "Czy na pewno chcesz zamknąć program?")
    if response:
        root.quit()


def get_value(pole):
    """Returns bus names."""
    # Pobranie wartości z pól + kontrola wpisywanych wartości
    start = pole.get()
    postoj = c.execute("SELECT Name FROM Stops")
    for rows in postoj:
        if start == rows[0]:
            return start
    return 0


class GUI(Trasa, szukaj.WszystkieTrasy, szukaj.Bezposrednie, DrogaZPrzystankami):
    """Creates GUI"""

    def __init__(self):
        self.trasa_linii2 = szukaj.Droga()
        self.istnieje = 0
        self.tmp = 0
        self.tymczasowa = 1

        self.blad = Blad(0.73, 0.79, "Taka linia nie isnieje", 14)
        self.blad.pokaz()

        self.blad_start = Blad(0.73, 0.36, "Taki przystanek nie isnieje", 14)
        self.blad_start.pokaz()

        self.blad_koniec = Blad(0.73, 0.46, "Taka przystanek nie isnieje", 14)
        self.blad_koniec.pokaz()

        self.blad_kara = Blad(0.73, 0.56, "Wprowadzono zle dane", 14)
        self.blad_kara.pokaz()

        self.pierwsza = []
        self.druga = []

    def ekran_poczatkowy(self):
        """Creates main screen."""
        self.logo()
        self.napisy_wyszukiwanie()
        self.pola()
        self.przyciski_wyszukiwanie()

    def logo(self):
        """Shows logo."""
        self.zdjecie = Logo()
        self.zdjecie.pokaz()

    def napisy_wyszukiwanie(self):
        """Creates strings."""
        self.przystanek_poczatkowy_tekst = Napis(0.3, 0.32, "Przystanek początkowy:", 12)
        self.przystanek_poczatkowy_tekst.pokaz()

        self.przystanek_koncowy_tekst = Napis(0.3, 0.42, "Przystanek końcowy", 12)
        self.przystanek_koncowy_tekst.pokaz()

        self.kara_tekst = Napis(0.3, 0.52, "Kara za przesiadkę:", 12)
        self.kara_tekst.pokaz()

        self.linia_tekst = Napis(0.3, 0.75, "Wybierz linie", 12)
        self.linia_tekst.pokaz()

    # Pola do wpisywania danych
    def pola(self):
        """Creates entry spaces."""
        self.poczatkowy = PoleDoWpisywania(0.3, 0.35)
        self.poczatkowy.pokaz()

        self.koncowy = PoleDoWpisywania(0.3, 0.45)
        self.koncowy.pokaz()

        self.przesiadka = PoleDoWpisywania(0.3, 0.55)
        self.przesiadka.pokaz()

        self.linia = PoleDoWpisywania(0.3, 0.78)
        self.linia.pokaz()

    # Przyciski
    def przyciski_wyszukiwanie(self):
        """Creates search buttons"""
        self.szukaj_button = Przycisk(0.19, 0.05, 0.3, 0.65, "Szukaj najkrótszych polaczen",
                                      self.pobierz_wartosci_droga)
        self.szukaj_button.pokaz()

        self.szukaj_bezposrednie_button = Przycisk(0.19, 0.05, 0.51, 0.65,
                                                   "Szukaj bezpośrednich polaczen",
                                                   self.bezposrednie_pobierz_wartosci_droga)
        self.szukaj_bezposrednie_button.pokaz()

        self.trasa_button = Przycisk(0.2, 0.05, 0.4, 0.88,
                                     'Pokaż trasę linii', self.pobierz_wartosci_linia)
        self.trasa_button.pokaz()

    # Funkcja zamknij

    def sprawdz_kare(self):
        """Returns penalty for change line."""
        self.kara = self.przesiadka.get()
        try:
            self.kara = float(self.kara)
            if 0 <= self.kara <= 100:
                return self.kara
            return -1
        except ValueError:
            return -1

    def zniszcz_początkowy(self):
        """Destroy all start elements on screen"""
        self.poczatkowy.destroy()
        self.koncowy.destroy()
        self.przesiadka.destroy()
        self.przystanek_poczatkowy_tekst.destroy()
        self.przystanek_koncowy_tekst.destroy()
        self.kara_tekst.destroy()
        self.szukaj_button.destroy()
        self.szukaj_bezposrednie_button.destroy()
        self.linia_tekst.destroy()
        self.linia.destroy()
        self.trasa_button.destroy()
        self.zdjecie.destroy()

    def pobierz_wartosci_droga(self):
        """Gets bus stops name"""
        # Pobranie wartości + obsługa błędów
        self.start = get_value(self.poczatkowy)
        self.end = get_value(self.koncowy)
        self.kara = self.sprawdz_kare()

        if self.start == 0:
            self.blad_start.config()

        if self.end == 0:
            self.blad_koniec.config()

        if self.kara == -1:
            self.blad_kara.config()

        if self.start != 0:
            self.blad_start.destroy()
            self.blad_start = Blad(0.73, 0.36, "Taki przystanek nie isnieje", 14)
            self.blad_start.pokaz()

        if self.end != 0:
            self.blad_koniec.destroy()
            self.blad_koniec = Blad(0.73, 0.46, "Taka przystanek nie isnieje", 14)
            self.blad_koniec.pokaz()

        if self.kara != -1:
            self.blad_kara.destroy()
            self.blad_kara = Blad(0.73, 0.56, "Wprowadzono zle dane", 14)
            self.blad_kara.pokaz()

        if self.start != 0 and self.end != 0 and self.kara != -1:
            # Zniszczenie pól
            self.zniszcz_początkowy()
            self.dzialanie()

    def bezposrednie_pobierz_wartosci_droga(self):
        """Gets bus stops name."""
        # Pobranie wartości + obsługa błędów
        self.start = get_value(self.poczatkowy)
        self.end = get_value(self.koncowy)
        self.kara = self.sprawdz_kare()

        if self.start == 0:
            self.blad_start.config()

        if self.end == 0:
            self.blad_koniec.config()

        if self.kara == -1:
            self.blad_kara.config()

        if self.start != 0:
            self.blad_start.destroy()
            self.blad_start = Blad(0.73, 0.36, "Taki przystanek nie isnieje", 14)
            self.blad_start.pokaz()

        if self.end != 0:
            self.blad_koniec.destroy()
            self.blad_koniec = Blad(0.73, 0.46, "Taka przystanek nie isnieje", 14)
            self.blad_koniec.pokaz()

        if self.kara != -1:
            self.blad_kara.destroy()
            self.blad_kara = Blad(0.73, 0.56, "Wprowadzono zle dane", 14)
            self.blad_kara.pokaz()

        if self.start != 0 and self.end != 0 and self.kara != -1:
            # Zniszczenie pól
            self.zniszcz_początkowy()
            self.dzialanie_bezposrednie()

    def wypisz(self):
        """Returns how many results are."""
        gotowe_set = copy.deepcopy(self.gotowe)
        tmp = self.wynik[0]
        i = 0
        rozmiar = len(gotowe_set)
        for i in range(rozmiar):
            gotowe_set[i] = set(gotowe_set[i])
        for i in range(len(self.wynik)):
            if self.wynik[i] <= tmp:
                i += 1
            else:
                break
        # ile = i
        # for i in range(ile):
        #     pierwszy = self.start[0]
        #     for j in range(len(self.gotowe[i]) - 1):
        #         if self.gotowe[i][j] != self.gotowe[i][j + 1]:
        #             pierwszy = self.trasa[j + 1]
        return i-1

    def dzialanie(self):
        """Searches for routes with total score."""
        # Wypisanie wyników
        napis = "Trasa {} - {} z karąza przesiadkę równą {}".format(self.start, self.end, self.kara)
        self.trasa_szukaj = Napis(0.27, 0.1, napis, 16)
        self.trasa_szukaj.pokaz()

        self.start = (self.start,)
        self.end = (self.end,)
        # Szukanie trasy
        klasa = szukaj.WszystkieTrasy()
        start_id = (klasa.sprawdz_id(self.start),)
        koniec_id = (klasa.sprawdz_id(self.end),)

        # Możliwe punkty zatrzymania autobusow na przystanku
        start_point_id = klasa.sprawdz_point_id(start_id)
        end_point_id = klasa.sprawdz_point_id(koniec_id)

        # Możliwe sposoby przejazdy linii przez dany przystanek
        start_variant_id = klasa.sprawdz_variant_id(start_point_id)
        end_variant_id = klasa.sprawdz_variant_id(end_point_id)

        # Wspolne kombinacje polaczen
        both_variant_id = klasa.sprawdz_both_variant_id(start_variant_id, end_variant_id)

        # #Zamienienie elementow listy z int na str
        klasa.zamien_elementy_int_na_str(start_point_id)
        klasa.zamien_elementy_int_na_str(both_variant_id)
        klasa.zamien_elementy_int_na_str(end_point_id)

        wszystkie_drogi = klasa.szukaj_wszystkie_drogi(start_point_id, end_point_id)
        kolejne_przystanki = klasa.wybierz_unikalne(wszystkie_drogi)
        self.trasa = copy.deepcopy(kolejne_przystanki)
        kolejne_przystanki = klasa.wybierz_unikalne_trasy(kolejne_przystanki)
        self.przystanki = klasa.wybierz_najkrotszy(kolejne_przystanki)
        self.przystanki = [i for k in self.przystanki for i in k]
        self.dlugosc = len(self.przystanki) - 1
        wybierzlinie = []
        pierwsze = klasa.szukaj_polaczen(self.przystanki[0], self.przystanki[1])

        self.gotowe = klasa.jakie_linie_na_trasie(pierwsze, self.przystanki,
                                                  wybierzlinie, self.dlugosc)
        self.wynik = klasa.policz(self.gotowe, self.kara)

        self.ile = self.wypisz() + 1

        if self.ile < 8:
            self.zmienna = DrogaZPrzystankami(self.start, self.end, self.gotowe,
                                              self.kara, self.przystanki,
                                              self.ile, self.wynik, self.tmp)
            self.zmienna.wypisz_napis()

        else:
            self.zmienna = DrogaZPrzystankami(self.start, self.end, self.gotowe, self.kara,
                                              self.przystanki, 7, self.wynik, self.tmp)
            self.zmienna.wypisz_napis()
            self.tmp += 7

            self.wiecej = Przycisk(0.3, 0.05, 0.35, 0.78, "Pokaż więcej", self.pokaz_wiecej)
            self.wiecej.pokaz()
            self.istnieje = 1

        # Przyciski

        self.wyjscie = Przycisk(0.3, 0.05, 0.15, 0.85, "Zamknij", zamknij)
        self.wyjscie.pokaz()

        self.powrot = Przycisk(0.3, 0.05, 0.55, 0.85, "Wróć", self.wroc_trasa)
        self.powrot.pokaz()

    def pokaz_wiecej(self):
        """Shows more routes."""
        self.zmienna.destroy()
        if self.tmp > self.ile:
            self.tmp = 0
            self.tymczasowa = 0
        self.tymczasowa += 1
        do_ilu = 7 * self.tymczasowa
        if do_ilu > self.ile:
            do_ilu = self.ile
        self.zmienna = DrogaZPrzystankami(self.start, self.end, self.gotowe,
                                          self.kara, self.przystanki,
                                          do_ilu, self.wynik, self.tmp)
        self.zmienna.wypisz_napis()
        self.tmp += 7

    def dzialanie_bezposrednie(self):
        """Searches for direct routes between two bus stops."""
        # Wypisanie wyników
        str1 = "Trasa {} - {} z karą za przesiadkę równą {}".format(self.start, self.end, self.kara)
        self.trasa_szukaj = Napis(0.27, 0.1, str1, 16)
        self.trasa_szukaj.pokaz()

        self.start = (self.start,)
        self.end = (self.end,)
        # Szukanie trasy
        klasa = szukaj.Bezposrednie()
        start_id = (klasa.sprawdz_id(self.start),)
        koniec_id = (klasa.sprawdz_id(self.end),)

        # Możliwe punkty zatrzymania autobusow na przystanku
        start_point_id = klasa.sprawdz_point_id(start_id)
        end_point_id = klasa.sprawdz_point_id(koniec_id)

        # Możliwe sposoby przejazdy linii przez dany przystanek
        start_variant_id = klasa.sprawdz_variant_id(start_point_id)
        end_variant_id = klasa.sprawdz_variant_id(end_point_id)

        # Wspolne kombinacje polaczen
        both_variant_id = klasa.sprawdz_both_variant_id(start_variant_id, end_variant_id)

        variant_id = (both_variant_id,)
        self.both_variant_line = klasa.zamien_id_na_nr_linii(variant_id)

        klasa.zamien_elementy_int_na_str(start_point_id)
        klasa.zamien_elementy_int_na_str(both_variant_id)
        klasa.zamien_elementy_int_na_str(end_point_id)

        self.stop_no = klasa.ktory_przystanek_linii(start_point_id, both_variant_id)
        self.stop_no2 = klasa.ktory_przystanek_linii(end_point_id, both_variant_id)

        przystanki = klasa.wybierz_odpowiednie_przystanki(self.stop_no, self.stop_no2)
        przystanki_start = przystanki[0]
        przystanki_end = przystanki[1]

        self.ilosc_przystankow = self.ile_przystankow(przystanki_start, przystanki_end)
        self.ile_tras = len(self.both_variant_line)

        if self.ile_tras < 8:
            self.zmienna = DrogaZPrzystankamiBezposrednia(self.start, self.end, self.kara,
                                                          self.both_variant_line, self.ile_tras,
                                                          self.ilosc_przystankow, self.tmp)
            self.zmienna.wypisz_napis()
        else:
            self.zmienna = DrogaZPrzystankamiBezposrednia(self.start, self.end, self.kara,
                                                          self.both_variant_line, 7,
                                                          self.ilosc_przystankow, self.tmp)
            self.zmienna.wypisz_napis()
            self.tmp += 7

            # Przyciski
            self.wiecej = Przycisk(0.3, 0.05, 0.35, 0.78, "Pokaż więcej",
                                   self.pokaz_wiecej_bezposrednie)
            self.wiecej.pokaz()
            self.istnieje = 1

        self.wyjscie = Przycisk(0.3, 0.05, 0.15, 0.85, "Zamknij", zamknij)
        self.wyjscie.pokaz()

        self.powrot = Przycisk(0.3, 0.05, 0.55, 0.85, "Wróć", self.wroc_trasa)
        self.powrot.pokaz()

    def pokaz_wiecej_bezposrednie(self):
        """Shows more connections."""
        self.zmienna.destroy()
        if self.tmp > self.ile_tras:
            self.tmp = 0
            self.tymczasowa = 0
        self.tymczasowa += 1
        do_ilu = 7 * self.tymczasowa
        if do_ilu > self.ile_tras:
            do_ilu = self.ile_tras
        self.zmienna = DrogaZPrzystankamiBezposrednia(self.start, self.end, self.kara,
                                                      self.both_variant_line, do_ilu,
                                                      self.ilosc_przystankow, self.tmp)
        self.zmienna.wypisz_napis()
        self.tmp += 7

    def wroc_linie(self):
        """Backs to previous screen."""
        self.blad = Blad(0.73, 0.79, "Taka linia nie isnieje", 14)
        self.blad.pokaz()
        self.trasa_napis.destroy()
        self.exit.destroy()
        self.again.destroy()
        self.odwroc.destroy()
        self.jaka_droga.destroy()

        self.logo()
        self.napisy_wyszukiwanie()
        self.pola()
        self.przyciski_wyszukiwanie()

    def wroc_trasa(self):
        """Backs to previous screen."""
        self.tymczasowa = 1
        self.tmp = 0
        self.zmienna.destroy()
        self.trasa_szukaj.destroy()
        self.wyjscie.destroy()
        self.powrot.destroy()
        if self.istnieje == 1:
            self.wiecej.destroy()
            # self.istnieje == 0

        self.logo()
        self.napisy_wyszukiwanie()
        self.pola()
        self.przyciski_wyszukiwanie()

    def odwroc_trase(self):
        """Revesres route."""
        self.wybor = self.jaka_droga.wybor
        self.jaka_droga.destroy()
        if self.wybor == 1:
            self.jaka_droga.wybor = 2
            self.jaka_droga.linie()
            # print(self.trasa_linii)
            # self.jakaDroga = Trasa(2,self.trasa_linii)
        elif self.wybor == 2:
            self.jaka_droga.wybor = 1
            self.jaka_droga.linie()
            # print(self.trasa_linii)
            # self.jakaDroga = Trasa(1,self.trasa_linii)

    def zniszcz_ekran_startowy(self):
        """Destroys all elements on start menu."""
        self.blad.destroy()
        self.zdjecie.destroy()
        self.poczatkowy.destroy()
        self.koncowy.destroy()
        self.przesiadka.destroy()
        self.przystanek_poczatkowy_tekst.destroy()
        self.przystanek_koncowy_tekst.destroy()
        self.kara_tekst.destroy()
        self.szukaj_button.destroy()
        self.szukaj_bezposrednie_button.destroy()
        self.linia_tekst.destroy()
        self.linia.destroy()
        self.trasa_button.destroy()

    def pobierz_wartosci_linia(self):
        """Gets line name."""
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
        except ValueError:
            self.droga = -1
            self.blad.config()

        # Zniszczenie pól

        if self.droga != -1:
            self.zniszcz_ekran_startowy()

            self.trasa_linii = self.trasa_linii2.trasa_linii(self.droga)

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
                    self.pierwsza.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
                if j == 1:
                    if self.trasa_linii[i][0] == 0:
                        j += 1
                    self.druga.append([self.trasa_linii[i][0], self.trasa_linii[i][1]])
            i = 0

            self.wybor = 2
            self.jaka_droga = Trasa(self.wybor, self.trasa_linii)
            self.jaka_droga.linie()

            # Przyciski
            self.exit = Przycisk(0.2, 0.05, 0.7, 0.85, "Zamknij", zamknij)

            self.again = Przycisk(0.2, 0.05, 0.4, 0.85, "Wróć", self.wroc_linie)

            self.odwroc = Przycisk(0.2, 0.05, 0.1, 0.85, "Odwróc", self.odwroc_trase)

            self.exit.pokaz()
            self.again.pokaz()
            self.odwroc.pokaz()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1000x1000")
    root.resizable(width=False, height=False)

    canvas = tk.Canvas(root, height=1000, width=1000, bg=BG_COLOR)
    canvas.pack()

    gui = GUI()
    gui.ekran_poczatkowy()

    root.mainloop()

    c.close()
    conn.close()
