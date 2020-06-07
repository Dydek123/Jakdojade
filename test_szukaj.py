"""The module tests the module szukaj."""
import unittest
import szukaj

class WyszukiwainieTest(unittest.TestCase):
    """ Tests Wyszukiwanie class."""

    def setUp(self):
        self.wyszukiwarka = szukaj.Wyszukiwanie()


    def test_sprawdz_id(self):
        """Tests sprawdz_id function."""
        self.assertEqual(self.wyszukiwarka.sprawdz_id(("Biprostal",)), 84)
        self.assertEqual(self.wyszukiwarka.sprawdz_id(("AGH",)), 80)
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_id, 0)
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_id, "AGH")
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_id, ("spam",))

    def test_sprawdz_point_id(self):
        """Tests sprawdz_point_id function."""
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_point_id, 0)
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_point_id, "84")
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_point_id, ("spam",))

    def test_point_id_to_stop_name(self):
        """Tests point_id_to_stop_name function."""
        self.assertEqual(self.wyszukiwarka.point_id_to_stop_name(7413), ['Biprostal'])
        self.assertRaises(Exception, self.wyszukiwarka.point_id_to_stop_name, 0)
        self.assertRaises(Exception, self.wyszukiwarka.point_id_to_stop_name, "spam")
        self.assertRaises(Exception, self.wyszukiwarka.point_id_to_stop_name, ("84",))

    def test_sprawdz_variant_id(self):
        """Tests sprawdz_variant_id function."""
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_variant_id, 745334)
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_variant_id, ['spam'])
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_variant_id, [0])

    def test_sprawdz_both_variant_id(self):
        """Tests sprawdz_both_variant_id function."""
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_both_variant_id, 745334,7413)
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_both_variant_id, [745334],7413)
        self.assertRaises(Exception, self.wyszukiwarka.sprawdz_both_variant_id, 745334,[7413])

    def test_zamien_id_na_nr_linii(self):
        """Tests zamien_id_na_nr_linii function."""
        self.assertEqual(self.wyszukiwarka.zamien_id_na_nr_linii(("spam",)), [])
        self.assertRaises(Exception, self.wyszukiwarka.zamien_id_na_nr_linii, 25)

    def test_zamien_elementy_int_na_str(self):
        """Tests if function convert integer to string."""
        self.assertEqual(self.wyszukiwarka.zamien_elementy_int_na_str([12,25]), ['12','25'])
        self.assertEqual(self.wyszukiwarka.zamien_elementy_int_na_str(['12','25']), ['12','25'])
        self.assertEqual(self.wyszukiwarka.zamien_elementy_int_na_str(['12',25]), ['12','25'])

    def test_ktory_przystanek_linii(self):
        """Tests ktory_przystanek_linii function."""
        self.assertRaises(Exception, self.wyszukiwarka.ktory_przystanek_linii, 113, 1085738)
        self.assertRaises(Exception, self.wyszukiwarka.ktory_przystanek_linii, [113], [1085738])

    def test_ile_przystankow(self):
        """Tests ile_przystankow function."""
        self.assertEqual(self.wyszukiwarka.ile_przystankow([2,5],[3,8]), [1,3])
        self.assertRaises(Exception, self.wyszukiwarka.ile_przystankow, 2, 5)

    def test_rzutuj_na_int(self):
        """Tests if function convert string to integer."""
        self.assertEqual(self.wyszukiwarka.rzutuj_na_int(['2', '5']), [2, 5])
        self.assertRaises(Exception, self.wyszukiwarka.rzutuj_na_int, 2)
        self.assertRaises(Exception, self.wyszukiwarka.rzutuj_na_int, ['2','str'])

    def test_szukaj_wszystkie_drogi(self):
        """Tests szukaj_wszystkie drogi function."""
        self.assertRaises(Exception, self.wyszukiwarka.rzutuj_na_int, 2098,12076)
        self.assertRaises(Exception, self.wyszukiwarka.rzutuj_na_int, ['2', 'str'],['12350','12078'])

    def test_wybierz_unikalne(self):
        """Selects only unique routes."""
        self.assertEqual(self.wyszukiwarka.wybierz_unikalne([[['12','15'],['12','15']]]), [['15', '12']])
        self.assertRaises(Exception, self.wyszukiwarka.wybierz_unikalne, [['12','15'],['12','15']])

    def test_wybierz_najkrotszy(self):
        """Selects the shortest route."""
        self.assertEqual(self.wyszukiwarka.wybierz_najkrotszy([[12],[12,15]]),[12])

    def test_szukaj_polaczen(self):
        """Tests search function."""
        self.assertEqual(self.wyszukiwarka.szukaj_polaczen('Plac Inwalidów', 'AGH'),['292'])
        self.assertRaises(Exception, self.wyszukiwarka.wybierz_unikalne, 'Plac Inwalidów', 'AGHH')
        self.assertRaises(Exception, self.wyszukiwarka.wybierz_unikalne, 'Plac Inwalidów', '12')


if __name__ == '__main__':
    unittest.main()
