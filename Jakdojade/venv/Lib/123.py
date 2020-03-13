import sqlite3
conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

print("Przystanek poczatkowy")
# start=(input(), )
start=("Politechnika", )
c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",start)
print(c.fetchall())
print("Przystanek koncowy")
# koniec=(input(), )
koniec=("Krowodrza Górka", )
c.execute("SELECT StopID FROM Points WHERE StopName=? order by StopID",koniec)
print(c.fetchall())

# c.execute("SELECT PointName FROM RRoutes WHERE StopID=73")
# print(c.fetchall())

print("Wypisuje linie pomiędzy przystankiem początkowym a końcowym przystankiem linii")
c.execute("SELECT LineName FROM StopDepartures WHERE StopID=73 and LastStopName=?",koniec)
print(c.fetchall())