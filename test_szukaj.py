"""The module tests the module szukaj."""
import unittest
import szukaj


class SearchRoutesTest(unittest.TestCase):
    """ Tests SearchRoutes class."""

    def setUp(self):
        self.search = szukaj.SearchRoutes()

    def test_check_id(self):
        self.assertEqual(self.search.check_id(("Biprostal",)), 84)
        self.assertEqual(self.search.check_id(("AGH",)), 80)
        self.assertRaises(szukaj.ValueIsNotTupleException, self.search.check_id, "AGH")
        self.assertRaises(szukaj.NoBusStopException, self.search.check_id, 0)
        self.assertRaises(szukaj.NoBusStopException, self.search.check_id, ("spam",))

    def test_check_point_id(self):
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.check_point_id, 0)
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.check_point_id, "84")
        self.assertRaises(szukaj.NoBusStopException,
                          self.search.check_point_id,
                          ("spam",))

    def test_point_id_to_stop_name(self):
        self.assertEqual(self.search.point_id_to_stop_name(7413),
                         ['Biprostal'])
        self.assertRaises(szukaj.NoBusStopException,
                          self.search.point_id_to_stop_name, 0)
        self.assertRaises(szukaj.NoBusStopException,
                          self.search.point_id_to_stop_name, "spam")
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.point_id_to_stop_name, ("84",))

    def test_check_variant_id(self):
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.check_variant_id, 745334)
        self.assertRaises(szukaj.NoBusStopException,
                          self.search.check_variant_id, ['spam'])
        self.assertRaises(szukaj.NoBusStopException,
                          self.search.check_variant_id, [0])

    def test_check_both_variant_id(self):
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.check_both_variant_id,
                          745334, 7413)
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.check_both_variant_id,
                          [745334], 7413)
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.check_both_variant_id,
                          745334, [7413])

    def test_id_to_bus_line(self):
        self.assertEqual(self.search.id_to_bus_line(("spam",)), [])
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.id_to_bus_line, 25)

    def test_int_to_str(self):
        self.assertEqual(self.search.int_to_str([12, 25]),
                         ['12', '25'])
        self.assertEqual(self.search.int_to_str(['12', '25']),
                         ['12', '25'])
        self.assertEqual(self.search.int_to_str(['12', 25]),
                         ['12', '25'])

    def which_bus_stop(self):
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.which_bus_stop,
                          113, 1085738)

    def test_how_many_bus_stops(self):
        self.assertEqual(self.search.how_many_bus_stops([2, 5], [3, 8]), [1, 3])
        self.assertRaises(szukaj.ValueIsNotTupleException, self.search.how_many_bus_stops, 2, 5)

    def test_change_to_int(self):
        self.assertEqual(self.search.change_to_int(['2', '5']), [2, 5])
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.change_to_int, 2)
        self.assertRaises(ValueError,
                          self.search.change_to_int, ['2', 'str'])

    def test_search_all_routes(self):
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.search_all_routes,
                          2098, 12076)
        self.assertRaises(szukaj.ValueIsNotTupleException,
                          self.search.search_all_routes,
                          ['2', 'st'], ['1235', '1207'])

    def test_choose_unique(self):
        self.assertEqual(self.search.choose_unique([[['12', '15'], ['12', '15']]]),
                         [['15', '12']])
        self.assertRaises(szukaj.ValueIsNotTupleException, self.search.choose_unique,
                          [['12', '15'], ['12']])

    def test_choose_shortest(self):
        self.assertEqual(self.search.choose_shortest([[12], [12, 15]]), [12])

    def test_search_connections(self):
        self.assertEqual(self.search.search_connections('Plac Inwalidów', 'AGH'), ['292'])
        self.assertRaises(Exception, self.search.choose_unique, 'Plac Inwalidów', 'AGHH')
        self.assertRaises(Exception, self.search.choose_unique, 'Plac Inwalidów', '12')

    def test_search(self):
        connections = szukaj.AllRoutes()
        connections.start = ("Biprostal",)
        connections.end_station = ("AGH",)
        bus_stops_list = connections.search()
        self.assertCountEqual(bus_stops_list, [{'24', '708'},
                                                  {'713', '708'},
                                                  {'704', '708'},
                                                  {'664', '708'},
                                                  {'708', '4'},
                                                  {'8', '708'},
                                                  {'13', '708'},
                                                  {'708', '14'},
                                                  {'708', '44'},
                                                  {'64', '708'}])

    def test_search_direct_connection(self):
        connections = szukaj.DirectConnections()
        connections.start = ("Politechnika",)
        connections.end = ("Miasteczko Studenckie AGH",)
        bus_stops_list = connections.search_direct_connection()
        self.assertCountEqual(bus_stops_list[0], ['501', '511', '208'])


if __name__ == '__main__':
    unittest.main()
