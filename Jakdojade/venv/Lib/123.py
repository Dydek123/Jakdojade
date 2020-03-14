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
koniec=("Przybyszewskiego", )
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





print("\n\n\n\nPrzystanek poczatkowy")
# start=(input(), )
start=("Politechnika", )
przystanek=c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",start)
for rows in przystanek:
    cos=rows[0]
startID=(cos,)
print("StopID ",start[0],"= ",startID[0])

print("\nPrzystanek koncowy")
# koniec=(input(), )
koniec=("Przybyszewskiego", )
przystanek=c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",koniec)
for rows in przystanek:
    cos=rows[0]
koniecID=(cos,)
print("StopID",koniec[0],"= ",koniecID[0])

StartPointID = []
print("\n StartPointID:")
c.execute("SELECT ID From Points WHERE StopId=?",startID)
for rows in przystanek:
    StartPointID.append(rows[0])
print(StartPointID)

EndPointID = []
print("\n EndPointID:")
c.execute("SELECT ID From Points WHERE StopId=?",koniecID)
for rows in przystanek:
    EndPointID.append(rows[0])
print(EndPointID)

c.close()
conn.close()