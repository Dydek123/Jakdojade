""" The module contains the functions needed for proper program operation
    Typical usage example:
    bezposrednie = Bezposrednie()
    bezposrednie.szukaj()
    bezposrednie.wypisz()
    wszystkie = WszystkieTrasy()
    wszystkie.szukaj()
    wszystkie.wypisz()
    trasa = Droga()
    trasa.trasaLinii(152)
    trasa.wypisz()
"""

import sqlite3
import copy
import collections

try:
    import readline
except ImportError:
    from pyreadline import Readline as readline

conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()



class BrakPrzystankuException(Exception):
    """Raises when the entered stop does not exist. """
    def __init__(self, przystanek):
        super().__init__()
        self.przystanek = przystanek


class KaraZlyPrzedialException(Exception):
    """Raises when the entered penalty value is not correct. """
    def __init__(self, kara):
        super().__init__()
        self.kara = kara

def normalize(title):
    return title.replace('’', "'").lower()


class Completer:

    def __init__(self, titles):
        self.titles = collections.defaultdict(list)
        for title in titles:
            self.titles[normalize(title)[:2]].append(title)

    def complete(self, text, state):
        if state == 0:
            text = normalize(text)
            candidates = self.titles.get(text[:2], [])
            self.matches = [
                c for c in candidates if normalize(c).startswith(text)]
        return self.matches[state]

class Graph:
    """Functions in graph."""
    def __init__(self):
        self.graph = collections.defaultdict(dict)

    # funkcja dodajaca krawedz do grafu
    def add_edge(self, przystanek_a, przystanek_b):
        """Adds edge to graph."""
        krawedz = []
        elementy = self.graph.get(przystanek_a)
        if elementy is None:
            krawedz.append(przystanek_b)
        else:
            for i in elementy:
                krawedz.append(i)
            krawedz.append(przystanek_b)
        self.graph[przystanek_a] = krawedz

    # Funkcja to przeszukiwania algorytmem bfs
    def bfs2(self, node, queue):
        """Algorithm BFS."""
        polaczenia = []
        visited = [node]
        queue.append(node)
        ile = 1
        ile_sasiadow_nieodwiedzonych = 0
        drugie_point_id = 0
        index_w_kolejce = 0
        pierwszy_nieodwiedzony = []
        while queue:
            for i in range(ile):
                pierwsze_point_id = queue.pop(0)
                # print(point_id, end=" ")
                polaczenia.append([pierwsze_point_id, drugie_point_id])
                for neighbour in self.graph[pierwsze_point_id]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)
                        ile_sasiadow_nieodwiedzonych += 1
                pierwszy_nieodwiedzony.append(ile_sasiadow_nieodwiedzonych)
                ile_sasiadow_nieodwiedzonych = 0
            ile = pierwszy_nieodwiedzony.pop(0)
            drugie_point_id = polaczenia[index_w_kolejce][0]
            index_w_kolejce += 1
            if not queue:
                break
        return polaczenia

    def najkrotsza(self, droga, poczatek, koniec):
        """Searches the shortest eoute between two stops"""
        droga.reverse()
        # print(droga)
        start = poczatek
        end = koniec
        najkrotsza_droga = []
        ilosc_drog = 1
        for j in range(0, ilosc_drog):
            chwilowa_droga = []
            poczatek = start
            koniec = end
            while True:
                for i in droga:
                    tmp = i
                    if tmp[0] == koniec:
                        chwilowa_droga.append(tmp[0])
                        break
                    if tmp[1] == 0:
                        return [-1, 0]
                koniec = tmp[1]
                if koniec == poczatek:
                    chwilowa_droga.append(koniec)
                    break
            najkrotsza_droga.append(chwilowa_droga)
        droga.reverse()
        return najkrotsza_droga


class GenerujGraf():
    """Generates graph."""
    def __init__(self, graf):
        self.graf = graf

    def generuj_wierzchołki_grafu(self):
        """Generates graph vertices."""
        wierzcholki = set()
        postoj = c.execute("SELECT Id From Points")
        for rows in postoj:
            wierzcholki.add(rows[0])
        return wierzcholki

    def generuj_krawedzie_grafu(self):
        """Generates graph edges."""
        polaczenia = set()
        tmp = []
        postoj = c.execute("SELECT VariantId, No, PointId From Routes")
        for rows in postoj:
            tmp.append(rows)
        # print(tmp)
        for i in range(len(tmp) - 1):
            if tmp[i][1] < tmp[i + 1][1]:  # and and tmp[i][0]==tmp[i+1][0]
                polaczenia.add((tmp[i][2], tmp[i + 1][2]))  # zmienic na add
        return polaczenia

    def generuj(self):
        """Adds right edges to graph."""
        polaczenia = self.generuj_krawedzie_grafu()
        # print(polaczenia)
        # print(len(polaczenia))
        polaczenia = list(polaczenia)

        for i in range(len(polaczenia)):
            self.graf.add_edge(polaczenia[i][0], polaczenia[i][1])


# Klasa odpowiedzialna za funkcjonalność
class Wyszukiwanie():
    """Searches routes between two bus stops."""
    def __init__(self):
        self.start = ("Biprostal",) #self.wprowadz_przystanek()
        self.koniec = ("AGH",)  # self.wprowadz_przystanek()
        self.kara = 2  # self.wybierz_kare()

    def wszystkie_przystanki(self):
        """Returns all bus stops in database."""
        przystanki = []
        postoj = c.execute("SELECT Name FROM Stops")
        for rows in postoj:
            przystanki.append(rows[0])
        return przystanki

    def wprowadz_przystanek(self):
        """Provides correct stop input."""
        lista_przystankow = self.wszystkie_przystanki()
        readline.parse_and_bind('tab: complete')
        readline.set_completer(Completer(lista_przystankow).complete)
        readline.set_completer_delims('')
        while True:
            try:
                print("Przystanek:", end=" ")
                przystanek = (input(),)
                postoj = c.execute("SELECT Name FROM Stops")
                for rows in postoj:
                    if przystanek[0] == rows[0]:
                        return przystanek
                else:
                    raise BrakPrzystankuException(przystanek)
            except BrakPrzystankuException:
                print("Przystanek {} nie istnieje, spróbuj ponownie".format(przystanek[0]))

    def wybierz_kare(self):
        """Provides correct penalty input."""
        while True:
            try:
                print("Wybierz kare za przesiadke (0:100)")
                kara = float(input())
                if 0 <= kara < 101:
                    return kara
                else:
                    raise KaraZlyPrzedialException(kara)
            except KaraZlyPrzedialException:
                print("{} nie należy do danego przedziału ! Wybierz kare od 0 do 100".format(kara))
            except ValueError:
                print("To nie jest liczba !")

    def sprawdz_id(self, przystanek):
        """Transform stop name to stop ID."""
        postoj = c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID", przystanek)
        for rows in postoj:
            cos = rows[0]
        przystanek = (cos,)
        return przystanek[0]

    def sprawdz_point_id(self, przystanek_id):
        """Checks available points to stop."""
        postoj = c.execute("SELECT ID From Points WHERE StopId=?", przystanek_id)
        point_id = [rows[0] for rows in postoj]
        return point_id

    def point_id_to_stop_name(self, przystanek_id):
        """Swaps point id to stop name"""
        point_id = (przystanek_id,)
        postoj = c.execute("SELECT StopName From Points WHERE Id=?", point_id)
        stop_name = [rows[0] for rows in postoj]
        return stop_name

    def sprawdz_variant_id(self, point_id):
        """Checks the possible ways for a bus to pass through a given stop."""
        variant_id = []
        for i in range(0, len(point_id)):
            postoj = c.execute("SELECT VariantID FROM StopDepartures WHERE PointID=? ORDER BY VariantID", (point_id[i],))
            for row in postoj:
                variant_id.append(row[0])
        variant_id = list(set(variant_id))
        return variant_id

    def sprawdz_both_variant_id(self, start_variant_id, end_variant_id):
        """Returns connection combinations."""
        both_variant_id = [start_variant_id[i] for i in range(0, len(start_variant_id))
                           for j in range(0, len(end_variant_id))
                           if start_variant_id[i] == end_variant_id[j]]
        return both_variant_id

    def zamien_id_na_nr_linii(self, variant_id):
        """Swaps id to line number."""
        both_variant_line = []
        both_variant_id = variant_id[0]
        for i in range(0, len(both_variant_id)):
            variant_id = (both_variant_id[i],)
            trasa = c.execute("SELECT * FROM Variants Where ID=?", variant_id)
            for row in trasa:
                both_variant_line.append(row[1])
        both_variant_line = list(set(both_variant_line))
        return both_variant_line

    def zamien_elementy_int_na_str(self, point_id):
        """Converts elements of type int to string."""
        for i in range(0, len(point_id)):  # Zamienienie elementow listy z int na str
            point_id[i] = str(point_id[i])
        return point_id

    def ktory_przystanek_linii(self, point_id, both_variant_id):
        """Checks which line stop is bus stop."""
        stop_no = []
        for j in range(0, len(both_variant_id)):
            variant_id = both_variant_id[j]
            for i in range(0, len(point_id)):
                trasa = c.execute("SELECT No FROM Routes WHERE PointID=? and VariantID=?", (point_id[i], variant_id))
                for row in trasa:
                    stop_no.append(row[0])
        return stop_no

    @staticmethod
    def ile_przystankow(przystanki_start, przystanki_end):
        """Retrurns number of line stops between two bus stops."""
        ilosc_przystankow = [przystanki_end[i] - przystanki_start[i] for i in range(len(przystanki_start))]
        return ilosc_przystankow

    @staticmethod
    def wybierz_odpowiednie_przystanki(stop_no, stop_no2):
        """Celects correct options for buses going in the right direction."""
        przystanki_start = [stop_no[i] for i in range(len(stop_no)) if stop_no2[i] > stop_no[i]]
        przystanki_end = [stop_no2[i] for i in range(len(stop_no2)) if stop_no2[i] > stop_no[i]]
        przystanki = [przystanki_start, przystanki_end]
        return przystanki

    @staticmethod
    def rzutuj_na_int(lista):
        """Convert all list elements to int."""
        for i in range(len(lista)):
            lista[i] = int(lista[i])

    def szukaj_wszystkie_drogi(self, start_point_id, end_point_id):
        """Searches whole routes."""
        przystanek_b = []
        wszystkie_drogi = []
        self.rzutuj_na_int(start_point_id)
        self.rzutuj_na_int(end_point_id)

        for i in range(len(start_point_id)):
            krawedz = graf_polaczen.bfs2(start_point_id[i], przystanek_b)
            if len(krawedz) != 1:
                test = int(krawedz[0][0])
                for j in range(len(end_point_id)):
                    test2 = int(end_point_id[j])
                    naj = graf_polaczen.najkrotsza(krawedz, test, test2)
                    if len(naj) != 2:
                        wszystkie_drogi.append(naj)
                    # print(naj,len(naj))
        return wszystkie_drogi

    @staticmethod
    def wybierz_unikalne(wszystkie_drogi):
        """Selects unique stops."""
        for i in range(len(wszystkie_drogi)):
            wszystkie_drogi[i][0].reverse()
        kolejne_przystanki = []
        for i in range(len(wszystkie_drogi)):
            kolejne_przystanki.append(wszystkie_drogi[i][0])
        return kolejne_przystanki

    def wybierz_unikalne_trasy(self, kolejne_przystanki):
        """Selects unique routes. """
        for i in range(len(kolejne_przystanki)):
            for j in range(len(kolejne_przystanki[i])):
                kolejne_przystanki[i][j] = self.point_id_to_stop_name(kolejne_przystanki[i][j])

        unikalna_trasa = []
        for i in range(len(kolejne_przystanki)):
            tmp = 0
            poczatkowy_przystanek = kolejne_przystanki[i][0]
            przystanek_koncowy = kolejne_przystanki[i][len(kolejne_przystanki[i]) - 1]
            for j in range(1, len(kolejne_przystanki[i]) - 1):
                if kolejne_przystanki[i][j] == poczatkowy_przystanek or kolejne_przystanki[i][j] == przystanek_koncowy:
                    tmp = 1
                    break
            if tmp == 1:
                continue
            else:
                unikalna_trasa.append(kolejne_przystanki[i])

        kolejne_przystanki = []
        for i in range(len(unikalna_trasa)):
            powtorzony = unikalna_trasa[i]
            tmp = 0
            for j in range(i + 1, len(unikalna_trasa)):
                if unikalna_trasa[j] == powtorzony:
                    tmp = 1
                    break
            if tmp == 1:
                continue
            else:
                kolejne_przystanki.append(unikalna_trasa[i])
        return kolejne_przystanki

    @staticmethod
    def wybierz_najkrotszy(przystanki):
        """Returns the shortest route."""
        tmp = przystanki[0]
        for i in range(len(przystanki)):
            if len(przystanki[i]) < len(tmp):
                tmp = przystanki[i]
        return tmp

    def szukaj_polaczen(self, start, koniec):
        """Returns list of lines number available between start and end stops."""
        start = (start,)
        koniec = (koniec,)
        start_id = (self.sprawdz_id(start),)
        koniec_id = (self.sprawdz_id(koniec),)
        start_point_id = self.sprawdz_point_id(start_id)
        end_point_id = self.sprawdz_point_id(koniec_id)
        start_variant_id = self.sprawdz_variant_id(start_point_id)
        end_variant_id = self.sprawdz_variant_id(end_point_id)
        both_variant_id = self.sprawdz_both_variant_id(start_variant_id, end_variant_id)
        stop_id = (both_variant_id,)
        both_variant_line = self.zamien_id_na_nr_linii(stop_id)
        return both_variant_line

    def jakie_linie_na_trasie(self, pierwsze_przystanki, nazwy_przystankow, wybierz_linie, dlugosc):
        """Returns the list of whole available travel combinations."""
        for i in pierwsze_przystanki:
            wybierz_linie.append([i])

        for i in range(1, len(nazwy_przystankow) - 1):
            drugie_przystanki = self.szukaj_polaczen(nazwy_przystankow[i], nazwy_przystankow[i + 1])
            for j in range(len(wybierz_linie)):
                if wybierz_linie[j][-1] in drugie_przystanki:
                    wybierz_linie[j].append(wybierz_linie[j][-1])
                else:
                    for k in range(len(drugie_przystanki)):
                        tmp = copy.deepcopy(wybierz_linie[j])
                        tmp.append(drugie_przystanki[k])
                        wybierz_linie.append(tmp)
        gotowe = []
        for i in range(len(wybierz_linie)):
            if len(wybierz_linie[i]) == dlugosc:
                gotowe.append(wybierz_linie[i])
        return gotowe

    @staticmethod
    def policz(linie, kara):
        """Calculates the total score of the given lines."""
        wynik = []
        for i in range(len(linie)):
            suma = 1
            for j in range(len(linie[i]) - 1):
                if linie[i][j] == linie[i][j + 1]:
                    suma += 1
                else:
                    suma = suma + kara + 1
            wynik.append(suma)
        return wynik


class Bezposrednie(Wyszukiwanie):
    """Searches for direct routes between two bus stop."""
    def wypisz(self):
        """Prints direct routes."""
        print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=", self.kara, " na trasie",
              self.start[0], "-", self.koniec[0], ":")
        for i in range(len(self.IloscPrzystankow)):
            print("\nTrasa nr ", i + 1)
            print("Linia {0} Ilosc przystankow {1}".format(self.BothVariantLine[i], self.IloscPrzystankow[i]))

    def szukaj(self):
        """Searches for direct routes."""
        start_id = (self.sprawdz_id(self.start),)
        koniec_id = (self.sprawdz_id(self.koniec),)

        start_point_id = self.sprawdz_point_id(start_id)
        end_point_id = self.sprawdz_point_id(koniec_id)

        start_variant_id = self.sprawdz_variant_id(start_point_id)
        end_variant_id = self.sprawdz_variant_id(end_point_id)
        both_variant_id = self.sprawdz_both_variant_id(start_variant_id, end_variant_id)

        stop_id = (both_variant_id,)
        self.BothVariantLine = self.zamien_id_na_nr_linii(stop_id)

        self.zamien_elementy_int_na_str(start_point_id)
        self.zamien_elementy_int_na_str(both_variant_id)
        self.zamien_elementy_int_na_str(end_point_id)

        stop_no = self.ktory_przystanek_linii(start_point_id, both_variant_id)
        stop_no2 = self.ktory_przystanek_linii(end_point_id, both_variant_id)

        przystanki = self.wybierz_odpowiednie_przystanki(stop_no, stop_no2)
        przystanki_start = przystanki[0]
        przystanki_end = przystanki[1]

        self.IloscPrzystankow = self.ile_przystankow(przystanki_start, przystanki_end)
        # self.wypisz(self.BothVariantLine,self.IloscPrzystankow)
        return self.BothVariantLine, self.IloscPrzystankow


class WszystkieTrasy(Wyszukiwanie):
    """Searches for shortest routes between two bus stop."""
    def __init__(self):
        super().__init__()
        graf = Graph()
        generowany_graf = GenerujGraf(graf)
        generowany_graf.generuj()
        self.wynik = 0
        self.gotowe = 0

    def szukaj(self):
        """Searches for shortest routes with total score."""
        # Wyszukiwanie ID przystanku
        start_id = (self.sprawdz_id(self.start),)
        koniec_id = (self.sprawdz_id(self.koniec),)

        # Możliwe punkty zatrzymania autobusow na przystanku
        start_point_id = self.sprawdz_point_id(start_id)
        end_point_id = self.sprawdz_point_id(koniec_id)

        # Możliwe sposoby przejazdy linii przez dany przystanek
        start_variant_id = self.sprawdz_variant_id(start_point_id)
        end_variant_id = self.sprawdz_variant_id(end_point_id)

        # Wspolne kombinacje polaczen
        both_variant_id = self.sprawdz_both_variant_id(start_variant_id, end_variant_id)

        # #Zamienienie elementow listy z int na str
        self.zamien_elementy_int_na_str(start_point_id)
        self.zamien_elementy_int_na_str(both_variant_id)
        self.zamien_elementy_int_na_str(end_point_id)

        wszystkie_drogi = self.szukaj_wszystkie_drogi(start_point_id, end_point_id)
        kolejne_przystanki = self.wybierz_unikalne(wszystkie_drogi)
        self.trasa = copy.deepcopy(kolejne_przystanki)
        kolejne_przystanki = self.wybierz_unikalne_trasy(kolejne_przystanki)
        self.przystanki = self.wybierz_najkrotszy(kolejne_przystanki)
        self.przystanki = [i for k in self.przystanki for i in k]
        dlugosc = len(self.przystanki) - 1
        wybierzlinie = []
        pierwsze = self.szukaj_polaczen(self.przystanki[0], self.przystanki[1])

        self.gotowe = self.jakie_linie_na_trasie(pierwsze, self.przystanki, wybierzlinie, dlugosc)
        self.wynik = self.policz(self.gotowe, self.kara)
        # ile = self.wypisz()
        # self.wypiszv2(gotowe, x, ile)

    def wypisz(self):
        """Prints final results."""
        gotowe_set = copy.deepcopy(self.gotowe)
        tmp = self.wynik[0]
        i = 0
        for i in range(len(gotowe_set)):
            gotowe_set[i] = set(gotowe_set[i])
        print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=", self.kara, " na trasie",
              self.start[0], "-", self.koniec[0], ":")
        for i in range(len(self.wynik)):
            if self.wynik[i] <= tmp:
                # print("Liniami: ", gotoweSet[i], wynik[i])
                i += 1
            else:
                break
        ile = i
        for i in range(ile):
            pierwszy = self.start[0]
            print("\nTrasa nr ", i + 1)
            print("Linią ", self.gotowe[i][0], " na trasie", end=": ")
            for j in range(len(self.gotowe[i]) - 1):
                if self.gotowe[i][j] != self.gotowe[i][j + 1]:
                    print(pierwszy, "-", self.przystanki[j + 1])
                    print("Linią ", self.gotowe[i][j + 1], " na trasie", end=": ")
                    pierwszy = self.przystanki[j + 1]
            else:
                print(pierwszy, "-", self.koniec[0])
        return i

    def wypiszv2(self, gotowe, trasa, ile):
        """Prints final results."""
        # print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=",kara," na trasie", start[0], "-", koniec[0], ":")
        for i in range(ile):
            pierwszy = self.start[0]
            print("\nTrasa nr ", i + 1)
            print("Linią ", gotowe[i][0], " na trasie", end=": ")
            for j in range(len(gotowe[i]) - 1):
                if gotowe[i][j] != gotowe[i][j + 1]:
                    print(pierwszy, "-", trasa[j + 1])
                    print("Linią ", gotowe[i][j + 1], " na trasie", end=": ")
                    pierwszy = trasa[j + 1]
            else:
                print(pierwszy, "-", self.koniec[0])
                break


class Droga:
    """Searches for all stops on a given bus line. """
    def __init__(self):
        self.droga = []
        self.linia = ()

    def trasa_linii(self, linia):
        """Returns tuple of stop number and stop name"""
        self.linia = (linia,)
        variant_id = []
        postoj = c.execute("SELECT Id FROM Variants WHERE LineName=?", self.linia)
        for row in postoj:
            variant_id.append(row[0])
        variant_id = list(set(variant_id))
        # print(VariantID)

        for i in enumerate(variant_id):
            postoj = c.execute("SELECT No, StopName FROM Routes  WHERE VariantID=?", (variant_id[i[0]],))
            for row in postoj:
                self.droga.append([row[0], row[1]])
        return self.droga

    def wypisz(self):
        """Prints route of the line"""
        for i in self.droga:
            print(i[0], i[1])


# Main

graf_polaczen = Graph()
wygenerowany_graf = GenerujGraf(graf_polaczen)
wygenerowany_graf.generuj()

# bezposrednie = Bezposrednie()
# bezposrednie.szukaj()
# bezposrednie.wypisz()

wszystkie = WszystkieTrasy()
wszystkie.szukaj()
wszystkie.wypisz()

# spis_przystankow = Droga()
# spis_przystankow.trasa_linii(152)
# spis_przystankow.wypisz()

# Zamkniecie
# c.close()
# conn.close()