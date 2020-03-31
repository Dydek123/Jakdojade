import sqlite3
conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

####################################### GLOWNY PROGRAM ############################################

#Wyszukiwanie ID przystanku poczatkowego
print("Przystanek poczatkowy")
start=(input(), )
# start=("Biprostal", )
przystanek=c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",start)
for rows in przystanek:
    cos=rows[0]
startID=(cos,)
print("StopID ",start[0],"= ",startID[0])

#Wyszukiwanie ID przystanku koncowego
print("\nPrzystanek koncowy")
koniec=(input(), )
# koniec=("Krowodrza Górka", )
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

print("\nObliczanie ilosci przstankow")

###########################################Start
for i in range (0,len(StartPointID)):
    StartPointID[i]=str(StartPointID[i])

for i in range (0,len(BothVariantID)):
    BothVariantID[i]=str(BothVariantID[i])

No=[]
for j in range (0,len(BothVariantID)):
    VariantID=BothVariantID[j]
    for i in range (0,len(StartPointID)):
        StartPoint=StartPointID[i]
        trasa = c.execute("SELECT No FROM Routes WHERE PointID="+StartPoint+" and VariantID="+VariantID)
        for row in trasa:
            No.append(row[0])
# No=No[0]
print(No)
###########################################EnD
for i in range (0,len(EndPointID)):
    EndPointID[i]=str(EndPointID[i])

No2=[]
for j in range (0,len(BothVariantID)):
    VariantID=BothVariantID[j]
    for i in range (0,len(EndPointID)):
        EndPoint=EndPointID[i]
        trasa = c.execute("SELECT No FROM Routes WHERE PointID="+EndPoint+" and VariantID="+VariantID)
        for row in trasa:
            No2.append(row[0])
# No2=No2[0]
print(No2)

przystankiStart=[]
przystankiEnd=[]

i=0
for i in range (0,len(No)):
    if No2[i]>No[i]:
        przystankiStart.append(No[i])
        przystankiEnd.append(No2[i])
print(przystankiStart)
print(przystankiEnd)
print(len(przystankiEnd))

IloscPrzystankow=[]
for i in range (0,len(przystankiStart)):
    IloscPrzystankow.append(przystankiEnd[i]-przystankiStart[i])

wynik=[]
for i in range (0,len(przystankiEnd)):
    wynik.append([BothVariantLine[i],IloscPrzystankow[i]])

print("Trasa", start[0] , " - ", koniec[0],": ")
print("Dostepne linie bezposrednie:")
i=0
for i in range(0,len(BothVariantLine)):    #BothVariantLine?
    print("Linia: ",wynik[i][0]," Przystankow: ",wynik[i][1])
#Zamkniecie
c.close()
conn.close()