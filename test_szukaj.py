"""The module tests the module szukaj."""
import unittest
import szukaj


class WyszukiwainieTest(unittest.TestCase):
    """ Tests Wyszukiwanie class."""

    def setUp(self):
        self.wyszukiwarka = szukaj.Wyszukiwanie()

    def test_sprawdz_id(self):
        self.assertEqual(self.wyszukiwarka.sprawdz_id(("Biprostal",)), 84)
        self.assertEqual(self.wyszukiwarka.sprawdz_id(("AGH",)), 80)
        self.assertRaises(szukaj.ZlaFormaArgumentow, self.wyszukiwarka.sprawdz_id, "AGH")
        self.assertRaises(szukaj.BrakPrzystankuException, self.wyszukiwarka.sprawdz_id, 0)
        self.assertRaises(szukaj.BrakPrzystankuException, self.wyszukiwarka.sprawdz_id, ("spam",))

    def test_sprawdz_point_id(self):
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.sprawdz_point_id, 0)
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.sprawdz_point_id, "84")
        self.assertRaises(szukaj.BrakPrzystankuException,
                          self.wyszukiwarka.sprawdz_point_id,
                          ("spam",))

    def test_point_id_to_stop_name(self):
        self.assertEqual(self.wyszukiwarka.point_id_to_stop_name(7413),
                         ['Biprostal'])
        self.assertRaises(szukaj.BrakPrzystankuException,
                          self.wyszukiwarka.point_id_to_stop_name, 0)
        self.assertRaises(szukaj.BrakPrzystankuException,
                          self.wyszukiwarka.point_id_to_stop_name, "spam")
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.point_id_to_stop_name, ("84",))

    def test_sprawdz_variant_id(self):
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.sprawdz_variant_id, 745334)
        self.assertRaises(szukaj.BrakPrzystankuException,
                          self.wyszukiwarka.sprawdz_variant_id, ['spam'])
        self.assertRaises(szukaj.BrakPrzystankuException,
                          self.wyszukiwarka.sprawdz_variant_id, [0])

    def test_sprawdz_both_variant_id(self):
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.sprawdz_both_variant_id,
                          745334, 7413)
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.sprawdz_both_variant_id,
                          [745334], 7413)
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.sprawdz_both_variant_id,
                          745334, [7413])

    def test_zamien_id_na_nr_linii(self):
        self.assertEqual(self.wyszukiwarka.zamien_id_na_nr_linii(("spam",)), [])
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.zamien_id_na_nr_linii, 25)

    def test_zamien_elementy_int_na_str(self):
        self.assertEqual(self.wyszukiwarka.zamien_elementy_int_na_str([12, 25]),
                         ['12', '25'])
        self.assertEqual(self.wyszukiwarka.zamien_elementy_int_na_str(['12', '25']),
                         ['12', '25'])
        self.assertEqual(self.wyszukiwarka.zamien_elementy_int_na_str(['12', 25]),
                         ['12', '25'])

    def test_ktory_przystanek_linii(self):
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.ktory_przystanek_linii,
                          113, 1085738)

    def test_ile_przystankow(self):
        self.assertEqual(self.wyszukiwarka.ile_przystankow([2, 5], [3, 8]), [1, 3])
        self.assertRaises(szukaj.ZlaFormaArgumentow, self.wyszukiwarka.ile_przystankow, 2, 5)

    def test_rzutuj_na_int(self):
        self.assertEqual(self.wyszukiwarka.rzutuj_na_int(['2', '5']), [2, 5])
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.rzutuj_na_int, 2)
        self.assertRaises(ValueError,
                          self.wyszukiwarka.rzutuj_na_int, ['2', 'str'])

    def test_szukaj_wszystkie_drogi(self):
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.szukaj_wszystkie_drogi,
                          2098, 12076)
        self.assertRaises(szukaj.ZlaFormaArgumentow,
                          self.wyszukiwarka.szukaj_wszystkie_drogi,
                          ['2', 'st'], ['1235', '1207'])

    def test_wybierz_unikalne(self):
        self.assertEqual(self.wyszukiwarka.wybierz_unikalne([[['12', '15'], ['12', '15']]]),
                         [['15', '12']])
        self.assertRaises(szukaj.ZlaFormaArgumentow, self.wyszukiwarka.wybierz_unikalne,
                          [['12', '15'], ['12']])

    def test_wybierz_najkrotszy(self):
        self.assertEqual(self.wyszukiwarka.wybierz_najkrotszy([[12], [12, 15]]), [12])

    def test_szukaj_polaczen(self):
        self.assertEqual(self.wyszukiwarka.szukaj_polaczen('Plac Inwalidów', 'AGH'), ['292'])
        self.assertRaises(Exception, self.wyszukiwarka.wybierz_unikalne, 'Plac Inwalidów', 'AGHH')
        self.assertRaises(Exception, self.wyszukiwarka.wybierz_unikalne, 'Plac Inwalidów', '12')

    def test_szukaj(self):
        polaczenia = szukaj.WszystkieTrasy()
        polaczenia.start = ("Biprostal",)
        polaczenia.koniec = ("AGH",)
        lista_przystankow = polaczenia.szukaj()
        for i in lista_przystankow:
            self.assertIn(i, [{'24', '708'},
                              {'713', '708'},
                              {'704', '708'},
                              {'664', '708'},
                              {'708', '4'},
                              {'8', '708'},
                              {'13', '708'},
                              {'708', '14'},
                              {'708', '44'},
                              {'64', '708'}])

    def test_szukaj_bezposrednie(self):
        polaczenia = szukaj.Bezposrednie()
        polaczenia.start = ("Politechnika",)
        polaczenia.koniec = ("Miasteczko Studenckie AGH",)
        lista_przystankow = polaczenia.szukaj_bezposrednie()
        for i in lista_przystankow[0]:
            self.assertIn(i, ['501', '511', '208'])


if __name__ == '__main__':
    unittest.main()
