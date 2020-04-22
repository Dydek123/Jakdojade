from tkinter import *

root = Tk()
canvas= Canvas(root, height=1000, width=1000, bg="#263D42")
canvas.pack()

#######################         FUNKCJE          ##########################################
def Polski():
    # Szukaj = Button(root, text='Szukaj połączeń')
    # Szukaj.place(relwidth=0.2,relheight=0.05,relx=0.4,rely=0.85)

    Przystanek_poczatkowy_tekst = Label(root, text="Przystanek początkowy:",bg="#263D42",)
    Przystanek_poczatkowy_tekst.place(relx=0.3, rely=0.52)

    Przystanek_koncowy_tekst = Label(root, text="Przystanek koncowy:",bg="#263D42")
    Przystanek_koncowy_tekst.place(relx=0.3, rely=0.62)

    Kara_tekst = Label(root, text="Kara za przesiadkę:",bg="#263D42")
    Kara_tekst.place(relx=0.3, rely=0.72)

def English():
    Szukaj = Button(root, text='Search')
    Szukaj.place(relwidth=0.2,relheight=0.05,relx=0.4,rely=0.85)

    Przystanek_poczatkowy_tekst = Label(root, text="Start point:",bg="#263D42")
    Przystanek_poczatkowy_tekst.place(relx=0.3, rely=0.32)

    Przystanek_koncowy_tekst = Label(root, text="Destination:",bg="#263D42")
    Przystanek_koncowy_tekst.place(relx=0.3, rely=0.52)

    Kara_tekst = Label(root, text="Penalty for changing lines:",bg="#263D42")
    Kara_tekst.place(relx=0.3, rely=0.72)

#######################         PROGRAM          ##########################################

Polski()
poczatkowy = Entry(root)
poczatkowy.place(relwidth=0.4, relheight=0.05, relx=0.3, rely=0.55)

# starts=start.get()

koncowy = Entry(root)
koncowy.place(relwidth=0.4, relheight=0.05, relx=0.3, rely=0.65)

# koniecs=koniec.get()

przesiadka = Entry(root)
przesiadka.place(relwidth=0.4, relheight=0.05, relx=0.3, rely=0.75)

# karas=kara.get()

def Szukaj():
    global start
    start = poczatkowy.get()
    global koniec
    koniec = koncowy.get()
    global kara
    kara = przesiadka.get()

Szukaj = Button(root, text='Szukaj połączeń',command=Szukaj)
Szukaj.place(relwidth=0.2,relheight=0.05,relx=0.4,rely=0.85)



root.mainloop()