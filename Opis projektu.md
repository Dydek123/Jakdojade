Dawid Mazurkiewicz 130547

Projekt – Wyszukiwarka połączeń komunikacji miejskiej dla miasta Kraków

Link do projektu: https://github.com/Dydek123/Jakdojade

Założenia projektowe kodu:

Głównym zadaniem projektu jest wyszukiwanie bezpośrednich oraz najkrótszych połączeń komunikacji miejskiej oraz znalezienie rozkładów jazdy danej linii. Całość projektu opiera się na bazie danych MPK Kraków. Wyszukiwanie najkrótszych tras będzie opierało się na zliczaniu przystanków pomiędzy dwoma punktami i wybraniu trasy z najmniejszą liczbą przystanków.

Ogólny opis kodu:

Połączenia bezpośrednie:
Algorytm wyszukiwania połączeń bezpośrednich opiera się wyłącznie na tworzeniu kolejnych zapytań do bazy danych. Użytkownik wprowadza przystanek startowy i końcowy jako dane. Po wykonaniu odpowiednich funkcji, na ekran zostaje wypisana liczba znalezionych tras bezpośrednich oraz odpowiadające tym trasom numery linii.

Najkrótsze trasy:
Na początku programu tworzony jest graf dostępnych połączeń pomiędzy przystankami autobusowymi. Graf zostaje wygenerowany tylko raz przy uruchomieniu programu. Jako krawędzie grafu zapisuję możliwe połączenia pomiędzy dwoma najbliższymi przystankami . Następnie, po wprowadzeniu danych przez użytkownika, za pomocą algorytmu BFS zostają znalezione najkrótsze trasy pomiędzy wprowadzonymi przystankami.

Rozkład linii
Jako dane użytkownik wprowadza numer linii, dla której ma zostać wyświetlona trasa. Za pomocą zapytań do bazy danych znajduję wszystkie przystanki pośrednie dla danej linii i wypisuję je na ekran

Co udało się zrobić, z czym były problemy

Udało się zrealizować wszystkie główne założenia programu, jednak zostały napotkane pewne problemy:

• W bazie danych brak jest jakichkolwiek danych odnośnie czasów odjazdu autobusów/tramwajów z przystanków, dlatego wybieranie najkrótszej trasy, odbywa się na podstawie ilości przystanków pomiędzy przystankami, zamiast czasu jazdy.

• Przy wyszukiwaniu najkrótszych tras, zdarza się, że ilość znalezionych kombinacji połączeń jest ogromna i uniemożliwia sensowne przeglądanie wyników, dlatego na ekran wypisywane zostają jedynie połączenia z najmniejszą liczbą przesiadek.

• Okazało się, porównywanie znalezionych wyników na różnych trasach z uwzględnieniem kary za przesiadkę trwała zbyt długo, dlatego postanowiłem ograniczyć wyszukiwanie tras do jednej najkrótszej.

Brak zauważonych problemów z testami.

Linki do istotnych fragmentów kodu:

List comprehensions :

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L290

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L329-L331

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L376-L377

Klasy:

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L228-L536

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L705-L742

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L539-L593

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L596-L702


Wyjątki:

• Zdefiniowane własnych klas wyjątku:

https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L42-L63

• Rzucanie/łapanie wyjątków

https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L213-L225

https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L247-L263

Podział na moduły:

• https://github.com/Dydek123/Jakdojade/blob/master/szukaj.py

• https://github.com/Dydek123/Jakdojade/blob/master/GUI.py

Podpowiedzi przy wprowadzaniu przystanków(po naciśnięciu przycisku tab, funkcja może nie działać w przypadku uruchamiania przez programy np. PyCharm)

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L66-L82

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L247-L263

Generowanie grafu i algorytm BFS

• https://github.com/Dydek123/Jakdojade/blob/c3fc5864b620aea365b3456332ccb2686b400f4e/szukaj.py#L85-L184