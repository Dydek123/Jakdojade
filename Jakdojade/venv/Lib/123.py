import sqlite3
conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

# print("Przystanek poczatkowy")
# # start=(input(), )
# start=("Politechnika", )
# c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",start)
# print(c.fetchall())
# print("Przystanek koncowy")
# koniec=(input(), )
koniec=("Dworzec Główny Zachód", )
# c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",koniec)
# print(c.fetchall())
#
#
# print("StreetID poczatek")
# c.execute("SELECT StreetID FROM RRoutes WHERE StopID=73 order by StreetID")
# print(c.fetchall())
#
# print("StreetID koniec")
# c.execute("SELECT StreetID FROM RRoutes WHERE StopID=81 order by StreetID")
# print(c.fetchall())


x=[0,0,0,0,0,0,0,0,0,0,0,0,0]
y=[]
i=0
print("Wypisuje linie pomiędzy przystankiem początkowym a końcowym przystankiem linii")
trasa = c.execute("SELECT LineName FROM StopDepartures WHERE StopID=73 and LastStopName=? order by LineName",koniec)
for row in trasa:

        if int(x[i])!=int(row[0]):
            x[i]=row[0]
            if x[i]!=x[i-1]:
                y.append(row[0])
                i+=1
print("y = ", y)



# # print("Przystanek poczatkowy")
# # start=(input(),)
# # print("Przystanek koncowy")
# # koniec=(input(),)
# #
# # print("Wypisuje linie i ilosc przystankow pomiędzy przystankiem początkowym a końcowym przystankiem linii")
# # c.execute("SELECT LineName,PointCount FROM Variants WHERE FirstStopName=(?) and LastStopName=(?)",(start,koniec))
#
# print("Wypisuje linie i ilosc przystankow pomiędzy przystankiem początkowym a końcowym przystankiem linii")
# c.execute("SELECT LineName,PointCount FROM Variants WHERE FirstStopName='Czyżyny Dworzec' and LastStopName='Mydlniki'")
# print(c.fetchall())
# for row in c.fetchall():
#     print(row)

c.close()
conn.close()