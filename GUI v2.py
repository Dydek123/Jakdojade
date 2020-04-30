from tkinter import *
import sqlite3

conn = sqlite3.connect("rozklady.sqlite3")
c = conn.cursor()

### Funkcje
def SprawdzPrzystanek(nazwa):
    przystanek = (nazwa.get(),)
    postoj = c.execute("SELECT Name FROM Stops")
    for rows in postoj:
        if przystanek[0] == rows[0]:
            return przystanek[0]
    print("Nie ma takiego przystanku, spróbuj ponownie")

root = Tk()
root.geometry("1000x1000")

canvas= Canvas(root, height=1000, width=1000, bg="#374E53")
canvas.pack()

def pobierz_wartosci():

    #Pobranie wartości z pól + kontrola wpisywanych wartości
    start = poczatkowy.get()
    postoj = c.execute("SELECT Name FROM Stops")
    for rows in postoj:
        if start == rows[0]:
            start = rows[0]
            break
    else:
        start = 0

    end = koncowy.get()
    postoj = c.execute("SELECT Name FROM Stops")
    for rows in postoj:
        if end == rows[0]:
            end = rows[0]
            break
    else:
        end = 0

    kara = przesiadka.get()
    try:
        kara=float(kara)
        if (kara>=0 or kara<=100):
            kara = float(kara)
    except:
        kara = -1

    #Zniszczenie pól

    if start != 0 and end!= 0 and kara !=-1:
        poczatkowy.destroy()
        koncowy.destroy()
        przesiadka.destroy()
        Przystanek_poczatkowy_tekst.destroy()
        Przystanek_koncowy_tekst.destroy()
        Kara_tekst.destroy()
        szukaj_button.destroy()

        trasa = Label(root,text="Trasa " + start + " - " +end + " z karą za przesiadkę równą " + str(kara),bg="#374E53", font=("Times New Roman",16))
        trasa.place(relx=0.25,rely=0.1)

# def napisy():

Przystanek_poczatkowy_tekst = Label(root, text="Przystanek początkowy:", bg="#374E53")
Przystanek_poczatkowy_tekst.place(relx=0.3, rely=0.52)

Przystanek_koncowy_tekst = Label(root, text="Przystanek koncowy:", bg="#374E53")
Przystanek_koncowy_tekst.place(relx=0.3, rely=0.62)

Kara_tekst = Label(root, text="Kara za przesiadkę:", bg="#374E53")
Kara_tekst.place(relx=0.3, rely=0.72)

poczatkowy = Entry(root)
poczatkowy.place(relwidth=0.4, relheight=0.05, relx=0.3, rely=0.55)

koncowy = Entry(root)
koncowy.place(relwidth=0.4, relheight=0.05, relx=0.3, rely=0.65)

przesiadka = Entry(root)
przesiadka.place(relwidth=0.4, relheight=0.05, relx=0.3, rely=0.75)

szukaj_button = Button(root,text='Szukaj połączeń',command=pobierz_wartosci)
szukaj_button.place(relwidth=0.2,relheight=0.05,relx=0.4,rely=0.85)

# napisy()


root.mainloop()
c.close()
conn.close()