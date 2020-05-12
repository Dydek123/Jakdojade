import sqlite3
import copy
import collections
from collections import defaultdict
conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

#Klasa wyjątku
class BrakPrzystankuException(Exception):
    def __init__(self,przystanek):
        self.przystanek = przystanek

class KaraZlyPrzedialException(Exception):
    def __init__(self,kara):
        self.kara = kara

#Klasy generujące graf
queue = []
visited = []
previous = []

class Graph:
    def __init__(self):
        self.graph = collections.defaultdict(dict)

    # funkcja dodajaca krawedz do grafu
    def addEdge(self, u, v):
        x = []
        elementy = self.graph.get(u)
        if elementy == None:
            x.append(v)
        else:
            for i in elementy:
                x.append(i)
            x.append(v)
        self.graph[u] = x

    # Funkcja to przeszukiwania algorytmem bfs
    def bfs(self, node):
        x = []
        s = 0
        visited.append(node)
        queue.append(node)
        while queue:
            z = s
            s = queue.pop(0)
            # print(s, end=" ")
            x.append([s, z])
            z += 1
            for neighbour in self.graph[s]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
        return x

    # Funkcja to przeszukiwania algorytmem bfs
    def bfs2(self, node, queue, visited):
        x = []
        visited=[]
        s = 0
        visited.append(node)
        queue.append(node)
        ile = 1
        a = 0
        b = 0
        j = 0
        c = []
        while queue:
            for i in range(ile):
                s = queue.pop(0)
                # print(s, end=" ")
                x.append([s, b])
                for neighbour in self.graph[s]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)
                        a += 1
                c.append(a)
                a = 0
            ile = c.pop(0)
            b = x[j][0]
            j += 1
            if queue == []:
                break
        return x

    # Funkcja szukająca nakrótszej drogi miedzy punktami
    def najkrotsza(self, droga, poczatek, koniec):
        droga.reverse()
        # print(droga)
        a=poczatek
        b=koniec
        x = []
        z = []
        for j in range (0,1):
            x=[]
            poczatek=a
            koniec=b
            while True:
                for i in droga:
                    if i[0] == koniec:
                        x.append(i[0])
                        break
                    elif i[1] == 0:
                        return [-1,0]
                koniec = i[1]
                if koniec == poczatek:
                    x.append(koniec)
                    break
            z.append(x)
        droga.reverse()
        return z

class GenerujGraf():
    def __init__(self,g):
        self.g = g

    def generujWierzchołkiGrafu(self):
        wierzcholki = set()
        postoj = c.execute("SELECT Id From Points")
        for rows in postoj:
            wierzcholki.add(rows[0])
        return wierzcholki

    def generujKrawedzieGrafu(self):
        polaczenia = set()  # !!!!!!!!!!!!!!zmienic na set
        tmp = []
        postoj = c.execute("SELECT VariantId, No, PointId From Routes")
        for rows in postoj:
            tmp.append(rows)
        # print(tmp)
        for i in range(len(tmp) - 1):
            if tmp[i][1] < tmp[i + 1][1]:  # and and tmp[i][0]==tmp[i+1][0]
                polaczenia.add((tmp[i][2], tmp[i + 1][2]))  # zmienic na add
        return polaczenia

    def generuj(self, g):
        wierzchołki = self.generujWierzchołkiGrafu()
        # print(wierzchołki)

        polaczenia = self.generujKrawedzieGrafu()
        # print(polaczenia)
        # print(len(polaczenia))
        polaczenia = list(polaczenia)

        for i in range(len(polaczenia)):
            self.g.addEdge(polaczenia[i][0], polaczenia[i][1])

#Klasa odpowiedzialna za funkcjonalność
class Wyszukiwanie():
    def __init__(self):
        self.start = ("Biprostal", )#self.WprowadzPrzystanek()
        self.koniec = ("Krowodrza Górka", )#self.WprowadzPrzystanek()
        self.kara = 2 #self.WybierzKare()

    def WprowadzPrzystanek(self):
        while (True):
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

    def WybierzKare(self):
        while (True):
            try:
                print("Wybierz kare za przesiadke (0:100)")
                kara = float(input())
                if kara >= 0 and kara < 101:
                    return kara
                else:
                    raise KaraZlyPrzedialException(kara)
            except KaraZlyPrzedialException:
                print("{} nie należy do danego przedziału ! Wybierz kare z przedzialu od 0 do 100".format(kara))
            except ValueError:
                print("To nie jest liczba !")

    def sprawdz_ID(self,przystanek):
        postoj = c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID", przystanek)
        for rows in postoj:
            cos = rows[0]
        przystanek = (cos,)
        return przystanek[0]

    def sprawdz_PointID(self, przystanekID):
        postoj = c.execute("SELECT ID From Points WHERE StopId=?", przystanekID)
        pointID = [rows[0] for rows in postoj]
        return pointID

    def PointID_to_StopName(self, przystanekID):
        x = (przystanekID,)
        postoj = c.execute("SELECT StopName From Points WHERE Id=?", x)
        stopName = [rows[0] for rows in postoj]
        return stopName

    def sprawdz_VariantID(self,pointID):  # list comprehension !!!
        variantID = []
        i = 0
        for i in range(0, len(pointID)):
            postoj = c.execute("SELECT VariantID FROM StopDepartures WHERE PointID=? ORDER BY VariantID", (pointID[i],))
            for row in postoj:
                variantID.append(row[0])
        variantID = list(set(variantID))
        return variantID

    def sprawdz_BothVariantID(self, StartVariantID, EndVariantID):
        BothVariantID = [StartVariantID[i] for i in range(0, len(StartVariantID)) for j in range(0, len(EndVariantID)) if StartVariantID[i] == EndVariantID[j]]
        return BothVariantID

    def zamien_ID_na_nr_linii(self, id):
        BothVariantLine = []
        BothVariantID = id[0]
        for i in range(0, len(BothVariantID)):
            id = (BothVariantID[i],)
            trasa = c.execute("SELECT * FROM Variants Where ID=?", id)
            for row in trasa:
                BothVariantLine.append(row[1])
        BothVariantLine = list(set(BothVariantLine))
        return BothVariantLine

    def zamien_elementy_int_na_str(self, PointID):
        for i in range(0, len(PointID)):  # Zamienienie elementow listy z int na str
            PointID[i] = str(PointID[i])
        return PointID

    def ktory_przystanek_linii(self, PointID, BothVariantID):
        No = []
        for j in range(0, len(BothVariantID)):
            VariantID = BothVariantID[j]
            for i in range(0, len(PointID)):
                trasa = c.execute("SELECT No FROM Routes WHERE PointID=? and VariantID=?", (PointID[i], VariantID))
                for row in trasa:
                    No.append(row[0])
        return No

    def ile_przystankow(self, przystankiStart, przystankiEnd):
        IloscPrzystankow = [przystankiEnd[i] - przystankiStart[i] for i in range(len(przystankiStart))]
        return IloscPrzystankow

    def wybierz_odpowiednie_przystanki(self, No, No2):
        przystankiStart = [No[i] for i in range(len(No)) if No2[i] > No[i]]
        przystankiEnd = [No2[i] for i in range(len(No2)) if No2[i] > No[i]]
        przystanki = []
        przystanki.append(przystankiStart)
        przystanki.append(przystankiEnd)
        return przystanki

    def rzutujNaInt(self, lista):
        for i in range(len(lista)):
            lista[i] = int(lista[i])

    def SzukajWszystkieDrogi(self, StartPointID, EndPointID):
        aa = []
        bb = []
        z = []
        self.rzutujNaInt(StartPointID)
        self.rzutujNaInt(EndPointID)
        x = []
        for i in range(len(StartPointID)):
            x = g.bfs2(StartPointID[i], aa, bb)
            if len(x) != 1:
                test = int(x[0][0])
                for j in range(len(EndPointID)):
                    test2 = int(EndPointID[j])
                    naj = g.najkrotsza(x, test, test2)
                    if len(naj) != 2:
                        z.append(naj)
                    # print(naj,len(naj))
        return z

    def wybierzUnikalne(self, z):
        for i in range(len(z)):
            z[i][0].reverse()
        kolejnePrzystanki = []
        for i in range(len(z)):
            kolejnePrzystanki.append(z[i][0])
        return kolejnePrzystanki

    def wybierzUnikalneTrasy(self, kolejnePrzystanki):
        for i in range(len(kolejnePrzystanki)):
            for j in range(len(kolejnePrzystanki[i])):
                kolejnePrzystanki[i][j] = self.PointID_to_StopName(kolejnePrzystanki[i][j])

        x = []
        for i in range(len(kolejnePrzystanki)):
            z = 0
            tmp = kolejnePrzystanki[i][0]
            tmp2 = kolejnePrzystanki[i][len(kolejnePrzystanki[i]) - 1]
            for j in range(1, len(kolejnePrzystanki[i]) - 1):
                if kolejnePrzystanki[i][j] == tmp or kolejnePrzystanki[i][j] == tmp2:
                    z = 1
                    break
            if z == 1:
                continue
            else:
                x.append(kolejnePrzystanki[i])

        kolejnePrzystanki = []
        for i in range(len(x)):
            tmp = x[i]
            z = 0
            for j in range(i + 1, len(x)):
                if x[j] == tmp:
                    z = 1
                    break
            if z == 1:
                continue
            else:
                kolejnePrzystanki.append(x[i])
        return kolejnePrzystanki

    def wybierzNajkrotszy(self, przystanki):
        tmp = przystanki[0]
        for i in range(len(przystanki)):
            q = len(przystanki[i])
            e = len(tmp)
            if len(przystanki[i]) < len(tmp):
                tmp = przystanki[i]
        return tmp

    def szukajPolaczen(self, start, koniec):
        start = (start,)
        koniec = (koniec,)
        startID = (self.sprawdz_ID(start),)
        koniecID = (self.sprawdz_ID(koniec),)
        StartPointID = self.sprawdz_PointID(startID)
        EndPointID = self.sprawdz_PointID(koniecID)
        StartVariantID = self.sprawdz_VariantID(StartPointID)
        EndVariantID = self.sprawdz_VariantID(EndPointID)
        BothVariantID = self.sprawdz_BothVariantID(StartVariantID, EndVariantID)
        id = (BothVariantID,)
        BothVariantLine = self.zamien_ID_na_nr_linii(id)
        return BothVariantLine

    def jakieLinieNaTrasie(self, pierwsze, x, wybierzlinie,dlugosc):
        for i in pierwsze:
            wybierzlinie.append([i])
        for i in range(1, len(x) - 1):
            drugie = self.szukajPolaczen(x[i], x[i + 1])
            for j in range(len(wybierzlinie)):
                if wybierzlinie[j][-1] in drugie:
                    wybierzlinie[j].append(wybierzlinie[j][-1])
                else:
                    for k in range(len(drugie)):
                        tmp = []
                        tmp = copy.deepcopy(wybierzlinie[j])
                        tmp.append(drugie[k])
                        wybierzlinie.append(tmp)
        gotowe = []
        for i in range(len(wybierzlinie)):
            if len(wybierzlinie[i]) == dlugosc:
                gotowe.append(wybierzlinie[i])
        return gotowe

    def policz(self, linie, kara):
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
    def __init__(self):
        super().__init__()

    def wypiszBezposrednie(self, trasa, ile):
        print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=",self.kara," na trasie", self.start[0], "-", self.koniec[0], ":")
        for i in range(len(ile)):
            pierwszy = self.start[0]
            print("\nTrasa nr ", i + 1)
            print("Linia {0} Ilosc przystankow {1}".format(trasa[i],ile[i]))

    def szukajBezposrednie(self):
        startID = (self.sprawdz_ID(self.start),)
        koniecID = (self.sprawdz_ID(self.koniec),)

        StartPointID = self.sprawdz_PointID(startID)
        EndPointID = self.sprawdz_PointID(koniecID)

        StartVariantID = self.sprawdz_VariantID(StartPointID)
        EndVariantID = self.sprawdz_VariantID(EndPointID)
        BothVariantID = self.sprawdz_BothVariantID(StartVariantID, EndVariantID)

        id = (BothVariantID,)
        BothVariantLine = self.zamien_ID_na_nr_linii(id)

        self.zamien_elementy_int_na_str(StartPointID)
        self.zamien_elementy_int_na_str(BothVariantID)
        self.zamien_elementy_int_na_str(EndPointID)

        No = self.ktory_przystanek_linii(StartPointID, BothVariantID)
        No2 = self.ktory_przystanek_linii(EndPointID, BothVariantID)

        przystanki = self.wybierz_odpowiednie_przystanki(No, No2)
        przystankiStart = przystanki[0]
        przystankiEnd = przystanki[1]

        IloscPrzystankow = self.ile_przystankow(przystankiStart, przystankiEnd)
        # self.wypiszBezposrednie(BothVariantLine,IloscPrzystankow)
        return (BothVariantLine,IloscPrzystankow)

class WszystkieTrasy(Wyszukiwanie):
    def __init__(self,g):
        super().__init__()
        self.g = g

    def szukaj(self):
        # Wyszukiwanie ID przystanku
        startID = (self.sprawdz_ID(self.start),)
        koniecID = (self.sprawdz_ID(self.koniec),)

        # Możliwe punkty zatrzymania autobusow na przystanku
        StartPointID = self.sprawdz_PointID(startID)
        EndPointID = self.sprawdz_PointID(koniecID)

        # Możliwe sposoby przejazdy linii przez dany przystanek
        StartVariantID = self.sprawdz_VariantID(StartPointID)
        EndVariantID = self.sprawdz_VariantID(EndPointID)

        # Wspolne kombinacje polaczen
        BothVariantID = self.sprawdz_BothVariantID(StartVariantID, EndVariantID)

        # #Zamienienie elementow listy z int na str
        self.zamien_elementy_int_na_str(StartPointID)
        self.zamien_elementy_int_na_str(BothVariantID)
        self.zamien_elementy_int_na_str(EndPointID)

        # #Generuj graf (przed otwarciem okna)
        # g = Graph()
        # GenerujGraf(g)
        z = []
        z = self.SzukajWszystkieDrogi(StartPointID, EndPointID)
        kolejnePrzystanki = self.wybierzUnikalne(z)
        trasa = copy.deepcopy(kolejnePrzystanki)
        kolejnePrzystanki = self.wybierzUnikalneTrasy(kolejnePrzystanki)
        x = self.wybierzNajkrotszy(kolejnePrzystanki)
        x = [i for k in x for i in k]

        dlugosc = len(x) - 1
        wybierzlinie = []
        pierwsze = self.szukajPolaczen(x[0], x[1])

        gotowe = self.jakieLinieNaTrasie(pierwsze, x, wybierzlinie,dlugosc)
        wynik = self.policz(gotowe, self.kara)
        ile = self.wypisz(wynik, gotowe)
        self.wypiszv2(gotowe, x, ile)

    def wypisz(self, wynik, gotowe):
        gotoweSet = copy.deepcopy(gotowe)
        tmp = wynik[0]
        i = 0
        for i in range(len(gotoweSet)):
            gotoweSet[i] = set(gotoweSet[i])
        print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=", self.kara, " na trasie", self.start[0], "-", self.koniec[0], ":")
        for i in range(len(wynik)):
            if wynik[i] <= tmp:
                print("Liniami: ", gotoweSet[i], wynik[i])
                i += 1
            else:
                break
        return i

    def wypiszv2(self, gotowe, trasa, ile):
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

#Main

# g=Graph()
# graf = GenerujGraf(g)
# graf.generuj(g)
#
# a = Wyszukiwanie()
# a.szukajBezposrednie()

# x = Bezposrednie()
# print(x.szukajBezposrednie())

# y = WszystkieTrasy(g)
# y.szukaj()
# Zamkniecie
c.close()
conn.close()