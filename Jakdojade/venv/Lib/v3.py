import sqlite3
import copy
from BFS import *

from collections import defaultdict
conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

####################################### FUNKCJE ##################################################

#########################   GRAF    #########################
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
    print(tmp)
    for i in range(len(tmp) - 1):
        if tmp[i][1] < tmp[i + 1][1]:  # and and tmp[i][0]==tmp[i+1][0]
            polaczenia.add((tmp[i][2], tmp[i + 1][2]))  # zmienic na add
    return polaczenia

#########################   POLĄCZENIA    #########################
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
            trasa = c.execute("SELECT No FROM Routes WHERE PointID="+PointID[i]+" and VariantID="+VariantID)
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
            y = c.execute("SELECT VariantID, No, PointID From Routes WHERE VariantID=" + a + " and No=" + b)
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
    print("Nazwa wspolnych linii!:", BothVariantLine)
    return BothVariantLine

####################################### GLOWNY PROGRAM ############################################
# Wyszukiwanie ID przystanku poczatkowego
print("Przystanek poczatkowy")
# start = (input(),)
start=("Biprostal", )
startID=(sprawdz_ID(start),)
print("StopID ", start[0], "= ", startID[0])

#Wyszukiwanie ID przystanku koncowego
print("\nPrzystanek koncowy")
# koniec=(input(), )
koniec=("Krowodrza Górka", )
koniecID=(sprawdz_ID(koniec),)
print("StopID",koniec[0],"= ",koniecID[0])

#Kara za przesiadkę
print("\nWybierz kare za przesiadkę")
# kara=int(input()
kara=2

#Możliwe punkty zatrzymania autobusow na przystanku poczatkowym
print("\n StartPointID:")
StartPointID=sprawdz_PointID(startID)
print(StartPointID)
print(len(StartPointID))

#Możliwe punkty zatrzymania autobusow na przystanku koncowym
print("\n EndPointID:")
EndPointID=sprawdz_PointID(koniecID)
print(EndPointID)
print(len(EndPointID))

#Możliwe sposoby przejazdy linii przez dany przystanek początkowy
print("\nStartVariantID")
StartVariantID=sprawdz_VariantID(StartPointID)
print("StartVariantID = ", StartVariantID)
print(len(StartVariantID))


#Możliwe sposoby przejazdy linii przez dany przystanek koncowy
print("\nEndVariantID")
EndVariantID=sprawdz_VariantID(EndPointID)
print("EndVariantID = ", EndVariantID)
print(len(EndVariantID))

#Wspolne kombinacje polaczen
print("\nBothVariantID")
BothVariantID=sprawdz_BothVariantID(StartVariantID,EndVariantID)
print("BothVariantID=",BothVariantID)


#Zamiana ID na nazwe linii
print("\nBothVariantLine")
id=(BothVariantID,)
BothVariantLine=zamien_ID_na_nr_linii(id)
print("Nazwa wspolnych linii:",BothVariantLine)
print(len(BothVariantLine) )

#Wypisanie linii osobno
# for i in range(0,len(BothVariantLine)):
#     print(BothVariantLine[i])


# Obliczanie ile jest przystankow miedzy punktem A i B
print("\nObliczanie ilosci przstankow")


# #Zamienienie elementow listy z int na str
zamien_elementy_int_na_str(StartPointID)
zamien_elementy_int_na_str(BothVariantID)
zamien_elementy_int_na_str(EndPointID)

#Obliczanie ktorym z kolei przystankiem jest dany przystanek
No=ktory_przystanek_linii(StartPointID,BothVariantID)
print("Przystanek poczatkowy: ",No)
No2=ktory_przystanek_linii(EndPointID,BothVariantID)
print("Przystanek koncowy: ",No2)

#Wybiera odpowiednie przystanki, które jadą w dobrą stronę
przystanki=wybierz_odpowiednie_przystanki(No,No2)
przystankiStart=przystanki[0]
przystankiEnd=przystanki[1]
print(przystankiStart)
print(przystankiEnd)

#Obliczanie ilosci przystankow miedzy dwoma punktami
IloscPrzystankow=ile_przystankow(przystankiStart,przystankiEnd)
print(IloscPrzystankow)
####################################### GENERUJ GRAF   ############################################
##############  Przed uruchomieniem okna    ##############
print("\n\n\n")

wierzchołki=generujWierzchołkiGrafu()
print(wierzchołki)

polaczenia=generujKrawedzieGrafu()
print(polaczenia)
print(len(polaczenia))
polaczenia=list(polaczenia)

g=Graph()
for i in range (len(polaczenia)):
    g.addEdge(polaczenia[i][0],polaczenia[i][1])

##############  Po uruchomieniem okna       ##############
def rzutujNaInt(lista):
    for i in range (len(lista)):
        lista[i]=int(lista[i])

aa = []
bb = []
z=[]

print(StartPointID,len(StartPointID))

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
rzutujNaInt(StartPointID)
rzutujNaInt(EndPointID)
for i in range(len(StartPointID)):
    x = g.bfs2(StartPointID[i], aa, bb)
    if len(x)!=1:
        test=int(x[0][0])
        for j in range (len(EndPointID)):
            test2=int(EndPointID[j])
            naj = g.najkrotsza(x,test,test2)
            if len(naj)!=2:
                z.append(naj)
            print(naj,len(naj))

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
for i in z:
    print(i[0],len(i[0]))
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n\n")
for i in range (len(z)):
    z[i][0].reverse()
kolejnePrzystanki=[]
for i in range (len(z)):
    kolejnePrzystanki.append(z[i][0])
trasa=copy.deepcopy(kolejnePrzystanki)
print("%%%%%%%%%%%%%%%%%%",trasa)
for i in range (len(kolejnePrzystanki)):
    for j in range (len(kolejnePrzystanki[i])):
        kolejnePrzystanki[i][j]=PointID_to_StopName(kolejnePrzystanki[i][j])
for i in kolejnePrzystanki:
    print(i)

def wybierzNajkrotszy(przystanki):
    tmp=przystanki[0]
    for i in range (len(przystanki)):
        q=len(przystanki[i])
        e=len(tmp)
        if len(przystanki[i])<len(tmp):
            tmp=przystanki[i]
    return tmp

print("\n\n\n\n Najkrótsza droga między wprowadzonymi przystankami to :")
x=wybierzNajkrotszy(kolejnePrzystanki)
print(x)
# x=wybierzNajkrotszy(trasa)
x = [i for k in x for i in k]
print("Na pointID",x)

# linie=[szukajPolaczen(x[i],x[i+1]) for i in range (len(x)-1)]
# print(linie)

# wybierzlinie=[]
# for i in range (len(linie)-1):
#     for j in range (len(linie[i])):
#         if linie[i][j] in linie[i+1]:
#             print(linie[i][j])
#             break

dlugosc=len(x)-1
wybierzlinie=[]
pierwsze=szukajPolaczen(x[0],x[1])
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
#WYPISZ LINIE
gotowe=[]
for i in range(len(wybierzlinie)):
    if len(wybierzlinie[i]) == dlugosc:
        gotowe.append(wybierzlinie[i])

print(gotowe)
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
wynik=policz(gotowe,kara)

for i in range (len(gotowe)):
    gotowe[i]=set(gotowe[i])
print(gotowe)

print("\n\n\n\n\n")
def wypisz(start,koniec,wynik,gotowe,kara):
    print("Łączne wyniki z uwzględnieniem przesiadek oraz karą za przesiadkę=",kara," na trasie", start[0], "-", koniec[0], ":")
    for i in range (len(wynik)):
        print("Liniami: ",gotowe[i],wynik[i])

wypisz(start,koniec,wynik,gotowe,kara)
#####################   SZUKAJ POłĄCZEń     ###############################



####################################################################    WYPISZ ###############################
# wynik=[[BothVariantLine[i],IloscPrzystankow[i]] for i in range (len(przystankiEnd))]
#
# print("Trasa", start[0] , " - ", koniec[0],": ")
# print("Dostepne linie bezposrednie:")
# i=0
# for i in range(0,len(BothVariantLine)):    #BothVariantLine?
#     print("Linia: ",wynik[i][0]," Przystankow: ",wynik[i][1])


# Zamkniecie
c.close()
conn.close()