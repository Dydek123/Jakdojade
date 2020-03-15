import sqlite3
conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

print("\nPrzystanek poczatkowy")
# start=(input(), )
start=("Politechnika", )
przystanek=c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",start)
for rows in przystanek:
    startID=rows[0]
print("StopID ",start[0],"= ",startID)

print("\nPrzystanek koncowy")
# koniec=(input(), )
koniec=("Dworzec Główny Wschód", )
przystanek=c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",koniec)
for rows in przystanek:
    koniecID=rows[0]
print("StopID",koniec[0],"= ",koniecID)

# print("\nStreetID poczatek")
# c.execute("SELECT StreetID FROM RRoutes WHERE StopID=73 order by StreetID")
# print(c.fetchall())
#
# print("\nStreetID koniec")
# c.execute("SELECT StreetID FROM RRoutes WHERE StopID=81 order by StreetID")
# print(c.fetchall())


x=[0,0,0,0,0,0,0,0,0,0,0,0,0]
y=[]
i=0
print("\nWypisuje linie pomiędzy przystankiem Politechnika a końcowym Dworzec Główny Zachód")
trasa = c.execute("SELECT LineName FROM StopDepartures WHERE StopID=73 and LastStopName=? order by LineName",koniec)
for row in trasa:
        if int(x[i])!=int(row[0]):
            x[i]=row[0]
            if x[i]!=x[i-1]:
                y.append(row[0])
                i+=1
print("y = ", y)



# print("Przystanek poczatkowy")
# start=(input(),)
# print("Przystanek koncowy")
# koniec=(input(),)
#
# print("Wypisuje linie i ilosc przystankow pomiędzy przystankiem początkowym a końcowym przystankiem linii")
# c.execute("SELECT LineName,PointCount FROM Variants WHERE FirstStopName=? and LastStopName=?",{start,koniec})
# c.execute("SELECT LineName,PointCount FROM Variants WHERE FirstStopName=:start and LastStopName=:koniec",{"start": start, "koniec": koniec})

print("\nWypisuje linie i ilosc przystankow pomiędzy przystankiem Czyżyny Dworzec a końcowym przystankiem Mydlniki")
c.execute("SELECT LineName,PointCount FROM Variants WHERE FirstStopName='Czyżyny Dworzec' and LastStopName='Mydlniki'")
print(c.fetchall())
for row in c.fetchall():
    print(row)


####################################### GLOWNY PROGRAM ############################################

#Wyszukiwanie ID przystanku poczatkowego
print("\n\n\n\nPrzystanek poczatkowy")
start=(input(), )
# start=("Politechnika", )
przystanek=c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",start)
for rows in przystanek:
    cos=rows[0]
startID=(cos,)
print("StopID ",start[0],"= ",startID[0])

#Wyszukiwanie ID przystanku koncowego
print("\nPrzystanek koncowy")
koniec=(input(), )
# koniec=("Dworzec Główny Zachód", )
przystanek=c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",koniec)
for rows in przystanek:
    cos=rows[0]
koniecID=(cos,)
print("StopID",koniec[0],"= ",koniecID[0])

#Możliwe punkty zatrzymania autobusow na przystanku poczatkowym
StartPointID = []
print("\n StartPointID:")
c.execute("SELECT ID From Points WHERE StopId=?",startID)  #Name - z którego przystanka DODAC!!!
for rows in przystanek:
    StartPointID.append(rows[0])
print(StartPointID)
print(len(StartPointID))

#Możliwe punkty zatrzymania autobusow na przystanku koncowym
EndPointID = []
print("\n EndPointID:")
c.execute("SELECT ID From Points WHERE StopId=?",koniecID)  #Name - z którego przystanka DODAC!!!
for rows in przystanek:
    EndPointID.append(rows[0])
print(EndPointID)
print(len(EndPointID))


#Możliwe sposoby przejazdy linii przez dany przystanek początkowy

# StartVariantID=[]
# print("\nStartVariantID")
# trasa = c.execute("SELECT VariantID FROM StopDepartures WHERE StopID=? order by VariantID",startID)     #POMYSL zmienic startID na pointID
# for row in trasa:
#     StartVariantID.append(row[0])
# StartVariantID=list(set(StartVariantID))
# print("StartVariantID = ", StartVariantID)
# print(len(StartVariantID))

StartVariantID=[]
print("\nStartVariantID")
i=0
for i in range (0,len(StartPointID)):
    x=(StartPointID[i], )
    trasa = c.execute("SELECT VariantID FROM StopDepartures WHERE PointID=? ORDER BY VariantID",x)
    for row in trasa:
        StartVariantID.append(row[0])
StartVariantID=list(set(StartVariantID))
print("StartVariantID = ", StartVariantID)
print(len(StartVariantID))


#Możliwe sposoby przejazdy linii przez dany przystanek koncowy
EndVariantID=[]
i=0
print("\nEndVariantID")
for i in range (0,len(EndPointID)):
    x=(EndPointID[i], )
    trasa = c.execute("SELECT VariantID FROM StopDepartures WHERE PointID=? ORDER BY VariantID",x)
    for row in trasa:
        EndVariantID.append(row[0])
EndVariantID=list(set(EndVariantID))
print("EndVariantID = ", EndVariantID)
print(len(EndVariantID))

#Wspolne kombinacje polaczen
i=0
j=0
BothVariantID =[]
print("\nBothVariantID")
for i in range(0,len(StartVariantID)):
    for j in range(0,len(EndVariantID)):
        if StartVariantID[i]==EndVariantID[j]:
            BothVariantID.append(StartVariantID[i])
        j=j+1
    i=i+1
print("BothVariantID=",BothVariantID)

#Zamiana ID na nazwe linii
BothVariantLine = []
i=0
print("\nBothVariantLine")
for i in range (0,len(BothVariantID)):
    id = (BothVariantID[i],)
    trasa = c.execute("SELECT * FROM Variants Where ID=?",id)
    for row in trasa:
        BothVariantLine.append(row[1])
    i+=1

BothVariantLine=list(set(BothVariantLine))
print("Nazwa wspolnych linii:",BothVariantLine)
print(len(BothVariantLine) )

i=0
for i in range(0,len(BothVariantLine)):
    print(BothVariantLine[i])
# Obliczanie ile jest przystankow miedzy punktem A i B


#Zamkniecie
c.close()
conn.close()