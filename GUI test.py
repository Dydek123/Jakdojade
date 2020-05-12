from tkinter import *
from tkinter import messagebox
import sqlite3
import copy
from BFS import *
from collections import defaultdict

conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

# import Main
def generujWierzchołkiGrafu():
    wierzcholki = set()
    postoj = c.execute("SELECT Id From Points")
    for rows in postoj:
        wierzcholki.add(rows[0])
    return wierzcholki

def generujKrawedzieGrafu():
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

def GenerujGraf(g):
    wierzchołki=generujWierzchołkiGrafu()
    # print(wierzchołki)

    polaczenia=generujKrawedzieGrafu()
    # print(polaczenia)
    # print(len(polaczenia))
    polaczenia=list(polaczenia)

    for i in range (len(polaczenia)):
        g.addEdge(polaczenia[i][0],polaczenia[i][1])

def SzukajWszystkieDrogi(StartPointID,EndPointID):
    aa = []
    bb = []
    z=[]
    rzutujNaInt(StartPointID)
    rzutujNaInt(EndPointID)
    x=[]
    for i in range(len(StartPointID)):
        x = g.bfs2(StartPointID[i], aa, bb)
        if len(x)!=1:
            test=int(x[0][0])
            for j in range (len(EndPointID)):
                test2=int(EndPointID[j])
                naj = g.najkrotsza(x,test,test2)
                if len(naj)!=2:
                    z.append(naj)
                # print(naj,len(naj))
    return z

def wybierzUnikalneTrasy(kolejnePrzystanki):
    for i in range (len(kolejnePrzystanki)):
        for j in range (len(kolejnePrzystanki[i])):
            kolejnePrzystanki[i][j]=PointID_to_StopName(kolejnePrzystanki[i][j])
    # for i in kolejnePrzystanki:
    #     print(i)

    x=[]
    for i in range (len(kolejnePrzystanki)):
        z=0
        tmp=kolejnePrzystanki[i][0]
        tmp2=kolejnePrzystanki[i][len(kolejnePrzystanki[i])-1]
        for j in range (1,len(kolejnePrzystanki[i])-1):
            if kolejnePrzystanki[i][j]==tmp or kolejnePrzystanki[i][j]==tmp2:
                z=1
                break
        if z==1:
            continue
        else:
            x.append(kolejnePrzystanki[i])
    # for i in x:
    #     print("!",i)

    kolejnePrzystanki=[]
    for i in range(len(x)):
        tmp=x[i]
        z=0
        for j in range (i+1,len(x)):
            if x[j]==tmp:
                z=1
                break
        if z==1:
            continue
        else:
            kolejnePrzystanki.append(x[i])
    return kolejnePrzystanki
#########################   POLĄCZENIA    #########################
def WprowadzPrzystanek():
    while(True):
        print("Przystanek:",end=" ")
        przystanek = (input(),)
        postoj = c.execute("SELECT Name FROM Stops")
        for rows in postoj:
            if przystanek[0] == rows[0]:
                return przystanek
        print("Nie ma takiego przystanku, spróbuj ponownie")

def WybierzKare():
    while(True):
        print("Wybierz kare za przesiadke (0:100)")
        kara = float(input())
        if kara>=0 and kara<101:
            return kara
        print("Niepoprawne dane! Wybierz kare z przedzialu od 0 do 100")

def sprawdz_ID(przystanek):
    postoj = c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID", przystanek)
    for rows in postoj:
        cos = rows[0]
    przystanek = (cos,)
    return przystanek[0]

def sprawdz_PointID(przystanekID):
    postoj = c.execute("SELECT ID From Points WHERE StopId=?", przystanekID)  # Name - z którego przystanka DODAC!!!
    pointID=[rows[0] for rows in postoj]
    return pointID

def PointID_to_StopName(przystanekID):
    x=(przystanekID,)
    postoj = c.execute("SELECT StopName From Points WHERE Id=?", x)
    stopName = [rows[0] for rows in postoj]
    return stopName

def sprawdz_VariantID(pointID): #list comprehension !!!
    variantID = []
    i=0
    for i in range(0, len(pointID)):
        postoj = c.execute("SELECT VariantID FROM StopDepartures WHERE PointID=? ORDER BY VariantID", (pointID[i],))
        for row in postoj:
            variantID.append(row[0])
    variantID = list(set(variantID))
    return variantID

def sprawdz_BothVariantID(StartVariantID,EndVariantID):
    BothVariantID =[]
    for i in range(0,len(StartVariantID)):
        for j in range(0,len(EndVariantID)):
            if StartVariantID[i]==EndVariantID[j]:
                BothVariantID.append(StartVariantID[i])
    return  BothVariantID

def zamien_ID_na_nr_linii(id):
    BothVariantLine = []
    BothVariantID=id[0]
    for i in range (0,len(BothVariantID)):
        id = (BothVariantID[i],)
        trasa = c.execute("SELECT * FROM Variants Where ID=?",id)
        for row in trasa:
            BothVariantLine.append(row[1])
    BothVariantLine=list(set(BothVariantLine))
    return BothVariantLine

def zamien_elementy_int_na_str(PointID):
    for i in range(0, len(PointID)):  # Zamienienie elementow listy z int na str
        PointID[i] = str(PointID[i])
    return PointID

def ktory_przystanek_linii(PointID,BothVariantID):
    No=[]
    for j in range (0,len(BothVariantID)):
        VariantID=BothVariantID[j]
        for i in range (0,len(PointID)):
            trasa = c.execute("SELECT No FROM Routes WHERE PointID=? and VariantID=?",(PointID[i],VariantID))
            for row in trasa:
                No.append(row[0])
    return No

def wybierz_odpowiednie_przystanki(No,No2):
    przystankiStart = [No[i] for i in range (len(No)) if No2[i]>No[i]]
    przystankiEnd = [No2[i] for i in range (len(No2)) if No2[i]>No[i]]
    przystanki=[]
    przystanki.append(przystankiStart)
    przystanki.append(przystankiEnd)
    return przystanki

def ile_przystankow(przystankiStart,przystankiEnd):
    IloscPrzystankow = [przystankiEnd[i] - przystankiStart[i] for i in range(len(przystankiStart))]
    return IloscPrzystankow

def najblizszy_przystanek(PointID):
    g = []
    for i in PointID:
        x = (i,)
        postoj = c.execute("SELECT VariantID, No, PointID From Routes WHERE PointID=?", x)
        for rows in postoj:
            print(rows)
            a = str(rows[0])
            d = int(rows[1]) + 1
            b = str(d)
            y = c.execute("SELECT VariantID, No, PointID From Routes WHERE VariantID=? and No=?",(a,b))
            for row in y:
                print("\t", row)
                g.append([rows[2], row[2]])
    return g

def szukajPolaczen(start,koniec):
    start=(start,)
    koniec=(koniec, )
    startID=(sprawdz_ID(start),)
    koniecID=(sprawdz_ID(koniec),)
    StartPointID = sprawdz_PointID(startID)
    EndPointID = sprawdz_PointID(koniecID)
    StartVariantID = sprawdz_VariantID(StartPointID)
    EndVariantID = sprawdz_VariantID(EndPointID)
    BothVariantID = sprawdz_BothVariantID(StartVariantID, EndVariantID)
    id = (BothVariantID,)
    BothVariantLine = zamien_ID_na_nr_linii(id)
    # print("Nazwa wspolnych linii!:", BothVariantLine)
    return BothVariantLine

def rzutujNaInt(lista):
    for i in range (len(lista)):
        lista[i]=int(lista[i])

def wybierzUnikalne(z):
    for i in range (len(z)):
        z[i][0].reverse()
    kolejnePrzystanki=[]
    for i in range (len(z)):
        kolejnePrzystanki.append(z[i][0])
    return kolejnePrzystanki

def wybierzNajkrotszy(przystanki):
    tmp=przystanki[0]
    for i in range (len(przystanki)):
        q=len(przystanki[i])
        e=len(tmp)
        if len(przystanki[i])<len(tmp):
            tmp=przystanki[i]
    return tmp

def jakieLinieNaTrasie(pierwsze,x,wybierzlinie):
    for i in pierwsze:
        wybierzlinie.append([i])
    for i in range (1,len(x)-1):
        drugie=szukajPolaczen(x[i],x[i+1])
        for j in range (len(wybierzlinie)):
            if wybierzlinie[j][-1] in drugie:
                wybierzlinie[j].append(wybierzlinie[j][-1])
            else:
                for k in range (len(drugie)):
                    tmp=[]
                    tmp=copy.deepcopy(wybierzlinie[j])
                    tmp.append(drugie[k])
                    wybierzlinie.append(tmp)
    gotowe = []
    for i in range(len(wybierzlinie)):
        if len(wybierzlinie[i]) == dlugosc:
            gotowe.append(wybierzlinie[i])
    return gotowe

def policz(linie,kara):
    wynik=[]
    for i in range (len(linie)):
        suma=1
        for j in range (len(linie[i])-1):
            if linie[i][j] == linie[i][j+1]:
                suma+=1
            else:
                suma=suma+kara+1
        wynik.append(suma)
    return wynik

def wypisz(start,koniec,wynik,gotowe,kara):
    gotoweSet = copy.deepcopy(gotowe)
    tmp=wynik[0]
    i=0
    for i in range(len(gotoweSet)):
        gotoweSet[i] = set(gotoweSet[i])
    print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=",kara," na trasie", start[0], "-", koniec[0], ":")
    for i in range (len(wynik)):
        if wynik[i]<=tmp:
            print("Liniami: ",gotoweSet[i],wynik[i])
            i+=1
        else:
            break
    return i
def wypiszv2(start,koniec,gotowe,kara,trasa,ile):
    # print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=",kara," na trasie", start[0], "-", koniec[0], ":")
    for i in range (ile):
        pierwszy = start[0]
        print("\nTrasa nr ",i+1)
        print("Linią ",gotowe[i][0]," na trasie",end=": ")
        for j in range (len(gotowe[i])-1):
            if gotowe[i][j]!=gotowe[i][j+1]:
                print(pierwszy,"-",trasa[j+1])
                print("Linią ",gotowe[i][j+1]," na trasie",end=": ")
                pierwszy=trasa[j+1]
        else:
            print(pierwszy,"-",koniec[0])

g=Graph()
GenerujGraf(g)


#####################   SZUKAJ POłĄCZEń     ###############################

# def funkcja():
#     start = WprowadzPrzystanek()
#     koniec = WprowadzPrzystanek()
#     kara = WybierzKare()
#     # szukaj(start,koniec,kara)
#     # szukaj(("Politechnika",),("Miasteczko Studenckie AGH",),3)      #Wkleić kod
#     # szukaj(("Biprostal",),("Krowodrza Górka",),3)
#     startID = (sprawdz_ID(start),)
#     koniecID = (sprawdz_ID(koniec),)
#
#     # Możliwe punkty zatrzymania autobusow na przystanku
#     StartPointID = sprawdz_PointID(startID)
#     EndPointID = sprawdz_PointID(koniecID)
#
#     # Możliwe sposoby przejazdy linii przez dany przystanek
#     StartVariantID = sprawdz_VariantID(StartPointID)
#     EndVariantID = sprawdz_VariantID(EndPointID)
#
#     # Wspolne kombinacje polaczen
#     BothVariantID = sprawdz_BothVariantID(StartVariantID, EndVariantID)
#
#     # #Zamienienie elementow listy z int na str
#     zamien_elementy_int_na_str(StartPointID)
#     zamien_elementy_int_na_str(BothVariantID)
#     zamien_elementy_int_na_str(EndPointID)
#
#     # #Generuj graf (przed otwarciem okna)
#     # g = Graph()
#     # GenerujGraf(g)
#     z = []
#     z = SzukajWszystkieDrogi(StartPointID, EndPointID)
#     kolejnePrzystanki = wybierzUnikalne(z)
#     trasa = copy.deepcopy(kolejnePrzystanki)
#     kolejnePrzystanki = wybierzUnikalneTrasy(kolejnePrzystanki)
#     x = wybierzNajkrotszy(kolejnePrzystanki)
#     x = [i for k in x for i in k]
#
#     global dlugosc
#     dlugosc = len(x) - 1
#     wybierzlinie = []
#     pierwsze = szukajPolaczen(x[0], x[1])
#
#     gotowe = jakieLinieNaTrasie(pierwsze, x, wybierzlinie)
#     wynik = policz(gotowe, kara)
#     ile = wypisz(start, koniec, wynik, gotowe, kara)
#     wypiszv2(start, koniec, gotowe, kara, x, ile)

######################## WYSZUKAJ TRASY LINII #############################
def trasaLinii(linia):
    linia=(linia,)
    VariantID = []
    postoj = c.execute("SELECT Id FROM Variants WHERE LineName=?", linia)
    for row in postoj:
        VariantID.append(row[0])
    VariantID = list(set(VariantID))
    # print(VariantID)

    droga = []
    for i in range(len(VariantID)):
        postoj = c.execute("SELECT No, StopName FROM Routes  WHERE VariantID=?", (VariantID[i],))
        for row in postoj:
            droga.append([row[0], row[1]])
    for i in droga:
        print(i[0], i[1])

####Klasy
class Napis:

    def __init__(self,x,y,tekst,font_size):
        self.x=x
        self.y=y
        self.tekst=tekst
        self.font = font_size

    def pokaz(self):
        self.napis = Label(root,text=self.tekst, bg="#adaead", font=("Times New Roman",self.font))
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

class DrogaZPrzystankami:
    def __init__(self,start,koniec,gotowe, kara, trasa, ile,wynik):
        self.start = start
        self.koniec = koniec
        self.gotowe = gotowe
        self.kara = kara
        self.trasa = trasa
        self.ile = ile
        self.wynik = wynik

    def wypisz_napis(self):
        koncowy_napis = " "
        for i in range(self.ile):
            pierwszy = self.start[0]
            z = i + 1
            koncowy_napis +=  "\n\nTrasa nr " + str(z) + "\t\tWynik: " + str(self.wynik[self.ile-1])
            koncowy_napis += "\nLinią " + str(self.gotowe[i][0]) + " na trasie: "
            for j in range(len(self.gotowe[i]) - 1):
                if self.gotowe[i][j] != self.gotowe[i][j + 1]:
                    koncowy_napis = koncowy_napis + str(pierwszy) + "-" + self.trasa[j + 1] + "\n"
                    koncowy_napis = koncowy_napis + "Linią " + str(self.gotowe[i][j + 1]) + " na trasie"
                    pierwszy = self.trasa[j + 1]
            else:
                koncowy_napis = koncowy_napis + str(pierwszy) + "-" + str(self.koniec[0])

        self.x = Napis(0.4, 0.2, koncowy_napis, 12)
        self.x.pokaz()

    def destroy(self):
        self.x.destroy()


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

def getValue(pole):
    # Pobranie wartości z pól + kontrola wpisywanych wartości
    start = pole.get()
    postoj = c.execute("SELECT Name FROM Stops")
    for rows in postoj:
        if start == rows[0]:
            return start
    else:
        return 0

def sprawdzKare():
    kara = przesiadka.get()
    try:
        kara = float(kara)
        if (kara >= 0 or kara <= 100):
            kara = float(kara)
            return kara
    except:
        return -1

def zniszczPoczątkowy():
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

def pobierz_wartosci_droga():

    #Pobranie wartości + obsługa błędów
    start = getValue(poczatkowy)
    end = getValue(koncowy)
    kara = sprawdzKare()

    if start != 0 and end!= 0 and kara !=-1:
        # Zniszczenie pól
        zniszczPoczątkowy()
        dzialanie(start,end,kara)

def dzialanie(start,koniec,kara):
    #Wypisanie wyników
    global trasaSzukaj
    trasaSzukaj = Napis(0.27,0.1,"Trasa " + start + " - " +koniec + " z karą za przesiadkę równą " + str(kara),16)
    trasaSzukaj.pokaz()

    start=(start,)
    koniec=(koniec,)
    #Szukanie trasy
    startID = (sprawdz_ID(start),)
    koniecID = (sprawdz_ID(koniec),)

    # Możliwe punkty zatrzymania autobusow na przystanku
    StartPointID = sprawdz_PointID(startID)
    EndPointID = sprawdz_PointID(koniecID)

    # Możliwe sposoby przejazdy linii przez dany przystanek
    StartVariantID = sprawdz_VariantID(StartPointID)
    EndVariantID = sprawdz_VariantID(EndPointID)

    # Wspolne kombinacje polaczen
    BothVariantID = sprawdz_BothVariantID(StartVariantID, EndVariantID)

    # #Zamienienie elementow listy z int na str
    zamien_elementy_int_na_str(StartPointID)
    zamien_elementy_int_na_str(BothVariantID)
    zamien_elementy_int_na_str(EndPointID)

    z = []
    z = SzukajWszystkieDrogi(StartPointID, EndPointID)
    kolejnePrzystanki = wybierzUnikalne(z)
    trasa = copy.deepcopy(kolejnePrzystanki)
    kolejnePrzystanki = wybierzUnikalneTrasy(kolejnePrzystanki)
    x = wybierzNajkrotszy(kolejnePrzystanki)
    x = [i for k in x for i in k]

    global dlugosc
    dlugosc = len(x) - 1
    wybierzlinie = []
    pierwsze = szukajPolaczen(x[0], x[1])

    gotowe = jakieLinieNaTrasie(pierwsze, x, wybierzlinie)
    wynik = policz(gotowe, kara)
    ile = wypisz(start, koniec, wynik, gotowe, kara)
    wypiszv2(start, koniec, gotowe, kara, x, ile)

    global zmienna
    zmienna = DrogaZPrzystankami(start,koniec,gotowe,kara,x,ile,wynik)
    zmienna.wypisz_napis()

    #Przyciski
    global wyjscie
    wyjscie = Przycisk(0.3, 0.05, 0.15, 0.85, "Zamknij", zamknij)
    wyjscie.pokaz()

    global powrot
    powrot = Przycisk(0.3, 0.05, 0.55, 0.85, "Wróć", wrocTrasa)
    powrot.pokaz()

def wrocLinie():
    droga = -1
    trasa_napis.destroy()
    exit.destroy()
    again.destroy()
    odwroc.destroy()
    jakaDroga.destroy()

    NapisyWyszukiwanie()
    Pola()
    przyciskiWyszukiwanie()

def wrocTrasa():
    zmienna.destroy()
    trasaSzukaj.destroy()
    wyjscie.destroy()
    powrot.destroy()

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

    global droga
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
        again = Przycisk(0.2,0.05,0.4,0.85,"Wróć",wrocLinie)

        global odwroc
        odwroc = Przycisk(0.2,0.05,0.1,0.85,"Odwróc",odwrocTrase)

        exit.pokaz()
        again.pokaz()
        odwroc.pokaz()


###### GŁÓWNY PROGRAM ######
root = Tk()
root.geometry("1000x1000")

canvas= Canvas(root, height=1000, width=1000, bg="#adaead")
canvas.pack()


NapisyWyszukiwanie()
Pola()
przyciskiWyszukiwanie()



root.mainloop()
c.close()
conn.close()