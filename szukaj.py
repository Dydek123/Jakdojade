""" The module contains the functions needed for proper program operation
    Typical usage example:
    wyszukiwarka = Wyszukiwanie()

    while True:
        print("\nWybierz opcje:")
        print("1.Polaczenia bezposrednie:")
        print("2.Najkrótsze połączenia:")
        print("3.Trasa danej linii:")
        print("4.Koniec")

        wybor = input()
        if wybor == '1':
            bezposrednie = Bezposrednie()
            bezposrednie.wprowadz_dane()
            bezposrednie.szukaj_bezposrednie()
            bezposrednie.wypisz()
        if wybor == '2':
            wszystkie = WszystkieTrasy()
            wszystkie.wprowadz_dane()
            wszystkie.szukaj()
            wszystkie.wypisz()
        if wybor == '3':
            linia = input("Podaj numer linii")
            spis_przystankow = Droga()
            spis_przystankow.trasa_linii(linia)
            spis_przystankow.wypisz()
        if wybor == '4':
            break
"""

import sqlite3
import copy
import collections

try:
    import readline
except ImportError:
    from pyreadline import Readline as readline


class NoBusStopException(Exception):
    """Raises when the entered stop does not exist. """

    def __init__(self, bus_stop):
        super().__init__()
        self.bus_stop = bus_stop


class PenaltyNotCorrectException(Exception):
    """Raises when the entered penalty value is not correct. """

    def __init__(self, penalty):
        super().__init__()
        self.penalty = penalty


class ValueIsNotTupleException(Exception):
    """Raises when the entered stop bus id value is not tuple. """

    def __init__(self, penalty):
        super().__init__()
        self.penalty = penalty


class Completer:
    """Helps to complete bus stop name"""

    def __init__(self, bus_stops):
        self.bus_stops = collections.defaultdict(list)
        for bus_stop in bus_stops:
            self.bus_stops[bus_stop.lower()[:2]].append(bus_stop)
            self.matches = []

    def complete(self, text, state):
        """Helps to complete bus stop name"""
        if state == 0:
            text = text.lower()
            candidates = self.bus_stops.get(text[:2], [])
            self.matches = [
                char for char in candidates if char.lower().startswith(text)]
        return self.matches[state]


def shortest(route, bus_start, bus_end):
    """Searches the shortest route between two stops"""
    route.reverse()
    # print(droga)
    start = bus_start
    end = bus_end
    shortest_route = []
    # ilosc_drog = 1
    # for j in range(0, ilosc_drog):
    temp_route = []
    bus_start = start
    bus_end = end
    while True:
        for i in route:
            tmp = i
            if tmp[0] == bus_end:
                temp_route.append(tmp[0])
                break
            if tmp[1] == 0:
                return [-1, 0]
        bus_end = tmp[1]
        if bus_end == bus_start:
            temp_route.append(bus_end)
            break
    shortest_route.append(temp_route)
    route.reverse()
    return shortest_route


class Graph:
    """Functions in graph."""

    def __init__(self):
        self.conn = sqlite3.connect("rozklady.sqlite3")
        self.c = self.conn.cursor()

        self.graph = collections.defaultdict(dict)

    def add_edge(self, first_bus_stop, second_bus_stop):
        """Adds edge to graph."""
        edge = []
        elements = self.graph.get(first_bus_stop)
        if elements is None:
            edge.append(second_bus_stop)
        else:
            for i in elements:
                edge.append(i)
            edge.append(second_bus_stop)
        self.graph[first_bus_stop] = edge

    def bfs2(self, node, queue):
        """Algorithm BFS."""
        connections = []
        visited = [node]
        queue.append(node)
        amount = 1
        neighbors_not_visited = 0
        second_point_id = 0
        index_in_queue = 0
        first_not_visited = []
        while queue:
            for i in range(amount):
                first_point_id = queue.pop(0)
                # print(point_id, end=" ")
                connections.append([first_point_id, second_point_id])
                for neighbour in self.graph[first_point_id]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)
                        neighbors_not_visited += 1
                first_not_visited.append(neighbors_not_visited)
                neighbors_not_visited = 0
            amount = first_not_visited.pop(0)
            second_point_id = connections[index_in_queue][0]
            index_in_queue += 1
            if not queue:
                break
        return connections

    def generate(self):
        """Adds right edges to graph."""
        connections = self.generate_graph_edges()
        # print(connections)
        # print(len(connections))
        connections = list(connections)
        for i in connections:
            self.add_edge(i[0], i[1])

    def generate_graph_edges(self):
        """Generates graph edges."""
        connections = set()
        tmp = []
        stop = self.c.execute("SELECT VariantId, No, PointId From Routes")
        for rows in stop:
            tmp.append(rows)
        # print(tmp)
        for i in range(len(tmp) - 1):
            if tmp[i][1] < tmp[i + 1][1]:  # and and tmp[i][0]==tmp[i+1][0]
                connections.add((tmp[i][2], tmp[i + 1][2]))  # zmienic na add
        return connections


def generate_graph_vertices():
    """Generates graph vertices."""
    conn = sqlite3.connect("rozklady.sqlite3")
    c = conn.cursor()
    vertices = set()
    stop = c.execute("SELECT Id From Points")
    for rows in stop:
        vertices.add(rows[0])
    return vertices


# class GenerateGraph():
#     """Generates graph."""
#     def __init__(self, graph):
#         self.graph = graph
#
#     def generuj(self):
#         """Adds right edges to graph."""
#         connections = generate_graph_edges()
#         # print(polaczenia)
#         # print(len(polaczenia))
#         connections = list(connections)
#
#         for i in connections:
#             self.graph.add_edge(i[0], i[1])

def choose_penalty():
    """Provides correct penalty input."""
    while True:
        try:
            print("Wybierz kare za przesiadke (0:100)")
            penalty = float(input())
            if 0 <= penalty < 101:
                return penalty
            raise PenaltyNotCorrectException(penalty)
        except PenaltyNotCorrectException:
            print("{} nie należy do danego przedziału ! Wybierz kare od 0 do 100".format(penalty))
        except ValueError:
            print("To nie jest liczba !")


class SearchRoutes():
    """Searches routes between two bus stops."""

    def __init__(self):
        self.conn = sqlite3.connect("rozklady.sqlite3")
        self.c = self.conn.cursor()

        self.start = ("Biprostal",)  # self.wprowadz_przystanek()
        self.end_station = ("AGH",)  # self.wprowadz_przystanek()
        self.penalty = 2  # self.wybierz_kare()

    def all_bus_stops(self):
        """Returns all bus stops in database."""
        bus_stops = []
        stop = self.c.execute("SELECT Name FROM Stops")
        for rows in stop:
            bus_stops.append(rows[0])
        return bus_stops

    def enter_bus_stop(self):
        """Provides correct stop input."""
        bus_stops_list = self.all_bus_stops()
        readline.parse_and_bind('tab: complete')
        readline.set_completer(Completer(bus_stops_list).complete)
        readline.set_completer_delims('')
        while True:
            try:
                print("Przystanek:", end=" ")
                bus_stop = (input(),)
                stop = self.c.execute("SELECT Name FROM Stops")
                for rows in stop:
                    if bus_stop[0] == rows[0]:
                        return bus_stop
                raise NoBusStopException(bus_stop)
            except NoBusStopException:
                print("Przystanek {} nie istnieje, spróbuj ponownie".format(bus_stop[0]))

    def enter_data(self):
        """Enters data."""
        self.start = self.enter_bus_stop()
        self.end_station = self.enter_bus_stop()
        self.penalty = choose_penalty()

    def check_id(self, bus_stop):
        """Transform stop name to stop ID."""
        try:
            stop = self.c.execute("SELECT StopID FROM Points"
                                    " WHERE StopName=? "
                                    "order by StopID", bus_stop)
            for rows in stop:
                cos = rows[0]
            bus_stop = (cos,)
            return bus_stop[0]
        except (UnboundLocalError, ValueError):
            raise NoBusStopException("Not a valid bus stop name")
        except sqlite3.ProgrammingError:
            raise ValueIsNotTupleException("Bus stop id not in tuple")

    def check_point_id(self, bus_stop_id):
        """Checks available points to stop."""
        try:
            postoj = self.c.execute("SELECT ID From Points WHERE StopId=?", bus_stop_id)
            point_id = [rows[0] for rows in postoj]
            if not point_id:
                raise NoBusStopException("Bus stop does not exists.")
            return point_id
        except (UnboundLocalError, ValueError, sqlite3.ProgrammingError):
            raise ValueIsNotTupleException("Not a valid bus stop id")

    def point_id_to_stop_name(self, bus_stop_id):
        """Swaps point id to stop name"""
        try:
            point_id = (bus_stop_id,)
            stop = self.c.execute("SELECT StopName From Points WHERE Id=?", point_id)
            stop_name = [rows[0] for rows in stop]
            if not stop_name:
                raise NoBusStopException("Not a valid bus stop id")
            return stop_name
        except (UnboundLocalError, ValueError, sqlite3.ProgrammingError, sqlite3.InterfaceError):
            raise ValueIsNotTupleException("Not a valid bus stop id")

    def check_variant_id(self, point_id):
        """Checks the possible ways for a bus to pass through a given stop."""
        try:
            variant_id = []
            for i in point_id:
                stop = self.c.execute("SELECT VariantID FROM StopDepartures WHERE PointID=?",
                                        (i,))
                for row in stop:
                    variant_id.append(row[0])
            variant_id = list(set(variant_id))
            if not variant_id:
                raise NoBusStopException("Not a valid bus stop point id - empty list")
            return variant_id
        except (TypeError, ValueError, sqlite3.ProgrammingError, sqlite3.InterfaceError):
            raise ValueIsNotTupleException("Not a valid bus stop point id")

    @staticmethod
    def check_both_variant_id(start_variant_id, end_variant_id):
        """Returns connection combinations."""
        try:
            both_variant_id = [i for i in start_variant_id
                               for j in end_variant_id
                               if i == j]
            return both_variant_id
        except (TypeError, ValueError, sqlite3.ProgrammingError, sqlite3.InterfaceError):
            raise ValueIsNotTupleException("Not a valid start or end variant id")

    def id_to_bus_line(self, variant_id):
        """Swaps id to line number."""
        try:
            both_variant_line = []
            both_variant_id = variant_id[0]
            for i in both_variant_id:
                variant_id = (i,)
                route = self.c.execute("SELECT * FROM Variants Where ID=?", variant_id)
                for row in route:
                    both_variant_line.append(row[1])
            both_variant_line = list(set(both_variant_line))
            return both_variant_line
        except TypeError:
            raise ValueIsNotTupleException("Not a valid variant id")

    @staticmethod
    def int_to_str(int_list):
        """Converts elements of type int to string."""
        str_list = [str(i) for i in int_list]
        return str_list

    def which_bus_stop(self, point_id, both_variant_id):
        """Checks which line stop is bus stop."""
        try:
            stop_no = []
            for j in both_variant_id:
                variant_id = j
                for i in point_id:
                    route = self.c.execute("SELECT No FROM Routes WHERE PointID=? and VariantID=?",
                                           (i, variant_id))
                    for row in route:
                        stop_no.append(row[0])
            return stop_no
        except (TypeError, ValueError, sqlite3.ProgrammingError, sqlite3.InterfaceError):
            raise ValueIsNotTupleException("Not a valid start or end variant id")

    @staticmethod
    def how_many_bus_stops(bus_stops_start, bus_stops_end):
        """Retrurns number of line stops between two bus stops."""
        try:
            bus_stops_amount = [bus_stops_end[i] - bus_stops_start[i]
                                for i in range(len(bus_stops_start))]
            return bus_stops_amount
        except TypeError:
            raise ValueIsNotTupleException("Not a valid bus stop number")

    @staticmethod
    def choose_appropriate_bus_stops(stop_no, stop_no2):
        """Celects correct options for buses going in the right direction."""
        bus_stops_start = [stop_no[i] for i in range(len(stop_no)) if stop_no2[i] > stop_no[i]]
        bus_stops_end = [stop_no2[i] for i in range(len(stop_no2)) if stop_no2[i] > stop_no[i]]
        przystanki = [bus_stops_start, bus_stops_end]
        return przystanki

    @staticmethod
    def change_to_int(list_elements):
        """Convert all list elements to int."""
        try:
            convert = [int(i) for i in list_elements]
            return convert
        except ValueError:
            raise ValueError("One of element can not be convert to int")
        except TypeError:
            raise ValueIsNotTupleException("Not valid argument")

    def search_all_routes(self, start_point_id, end_point_id):
        """Searches whole routes."""
        bus_stop_b = []
        all_routes = []
        try:
            self.change_to_int(start_point_id)
            self.change_to_int(end_point_id)

            for i in start_point_id:
                edge = connection_graph.bfs2(i, bus_stop_b)
                if len(edge) != 1:
                    test = int(edge[0][0])
                    for j in end_point_id:
                        test2 = int(j)
                        naj = shortest(edge, test, test2)
                        if len(naj) != 2:
                            all_routes.append(naj)
                        # print(naj,len(naj))
            return all_routes
        except (TypeError, ValueError):
            raise ValueIsNotTupleException("Not a valid arguments")

    @staticmethod
    def choose_unique(all_routes):
        """Selects unique stops."""
        try:
            for i in all_routes:
                i[0].reverse()
            next_bus_stops = []
            for i in all_routes:
                next_bus_stops.append(i[0])
            return next_bus_stops
        except (TypeError, ValueError, AttributeError):
            raise ValueIsNotTupleException("Not a valid arguments")

    def choose_unique_routes(self, next_bus_stops):
        """Selects unique routes. """
        length_next_bus_stops = len(next_bus_stops)
        for i in range(length_next_bus_stops):
            for j in range(len(next_bus_stops[i])):
                next_bus_stops[i][j] = self.point_id_to_stop_name(next_bus_stops[i][j])

        unique_route = []
        for i in next_bus_stops:
            tmp = 0
            first = i[0]
            last = i[len(i) - 1]
            for j in range(1, len(i) - 1):
                if i[j] == first or i[j] == last:
                    tmp = 1
                    break
            if tmp == 1:
                continue
            unique_route.append(i)

        next_bus_stops = []
        length_unique_route = len(unique_route)
        for i in range(length_unique_route):
            repeated = unique_route[i]
            tmp = 0
            for j in range(i + 1, length_unique_route):
                if unique_route[j] == repeated:
                    tmp = 1
                    break
            if tmp == 1:
                continue
            next_bus_stops.append(unique_route[i])
        return next_bus_stops

    @staticmethod
    def choose_shortest(bus_stops):
        """Returns the shortest route."""
        try:
            tmp = bus_stops[0]
            for i in bus_stops:
                if len(i) < len(tmp):
                    tmp = i
            return tmp
        except TypeError:
            Exception("Not a valid arguments")

    def search_connections(self, start, end):
        """Returns list of lines number available between start and end stops."""
        start = (start,)
        end = (end,)
        start_id = (self.check_id(start),)
        end_id = (self.check_id(end),)
        start_point_id = self.check_point_id(start_id)
        end_point_id = self.check_point_id(end_id)
        start_variant_id = self.check_variant_id(start_point_id)
        end_variant_id = self.check_variant_id(end_point_id)
        both_variant_id = self.check_both_variant_id(start_variant_id, end_variant_id)
        stop_id = (both_variant_id,)
        both_variant_line = self.id_to_bus_line(stop_id)
        return both_variant_line

    def which_bus_lines_on_route(self, first_bus_stops, bus_stops_name, choose_lines, length):
        """Returns the list of whole available travel combinations."""
        for i in first_bus_stops:
            choose_lines.append([i])

        for i in range(1, len(bus_stops_name) - 1):
            second_bus_stops = self.search_connections(bus_stops_name[i], bus_stops_name[i + 1])
            for j in choose_lines:
                if j[-1] in second_bus_stops:
                    j.append(j[-1])
                else:
                    for k in second_bus_stops:
                        tmp = copy.deepcopy(j)
                        tmp.append(k)
                        choose_lines.append(tmp)
        ready = []
        for i in choose_lines:
            if len(i) == length:
                ready.append(i)
        return ready

    @staticmethod
    def count(bus_lines, penalty):
        """Calculates the total score of the given lines."""
        score = []
        bus_lines_length = len(bus_lines)
        for i in range(bus_lines_length):
            sum = 1
            for j in range(len(bus_lines[i]) - 1):
                if bus_lines[i][j] == bus_lines[i][j + 1]:
                    sum += 1
                else:
                    sum = sum + penalty + 1
            score.append(sum)
        return score

    def close_database(self):
        """Closes database."""
        self.c.close()
        self.conn.close()


class DirectConnections(SearchRoutes):
    """Searches for direct routes between two bus stop."""

    def __init__(self):
        super().__init__()
        self.bus_stops_amount = 0
        self.both_variant_line = "Brak"

    def show(self):
        """Prints direct routes."""
        if self.both_variant_line == [] or self.bus_stops_amount == []:
            print("Brak połączeń bezpośrednich")
        else:
            my_string = "Trasy bezposrednie na trasie {} - {}:"
            print(my_string.format(self.start[0], self.end[0]))
            for i in range(len(self.bus_stops_amount)):
                print("\nTrasa nr ", i + 1)
                my_string = "Linia {0}"
                print(my_string.format(self.both_variant_line[i]))

    def enter_data(self):
        """Enters data."""
        self.start = SearchRoutes.enter_bus_stop(self)
        self.end = SearchRoutes.enter_bus_stop(self)

    def search_direct_connection(self):
        """Searches for direct routes."""
        # self.wprowadz_dane()
        start_id = (self.check_id(self.start),)
        end_id = (self.check_id(self.end),)

        start_point_id = self.check_point_id(start_id)
        end_point_id = self.check_point_id(end_id)

        start_variant_id = self.check_variant_id(start_point_id)
        end_variant_id = self.check_variant_id(end_point_id)
        both_variant_id = self.check_both_variant_id(start_variant_id, end_variant_id)

        stop_id = (both_variant_id,)
        self.both_variant_line = self.id_to_bus_line(stop_id)

        self.int_to_str(start_point_id)
        self.int_to_str(both_variant_id)
        self.int_to_str(end_point_id)

        stop_no = self.which_bus_stop(start_point_id, both_variant_id)
        stop_no2 = self.which_bus_stop(end_point_id, both_variant_id)

        bus_stops = self.choose_appropriate_bus_stops(stop_no, stop_no2)
        bus_stops_start = bus_stops[0]
        bus_stops_end = bus_stops[1]

        self.bus_stops_amount = self.how_many_bus_stops(bus_stops_start, bus_stops_end)
        return self.both_variant_line, self.bus_stops_amount


class AllRoutes(SearchRoutes):
    """Searches for shortest routes between two bus stop."""

    def __init__(self):
        super().__init__()
        graph = Graph()
        graph.generate()
        self.score = 0
        self.ready = 0

        self.route = 0
        self.bus_stops = 0

    def search(self):
        """Searches for shortest routes with total score."""
        # self.wprowadz_dane()
        # Search bus stop ID
        start_id = (self.check_id(self.start),)
        end_id = (self.check_id(self.end_station),)

        # Possible stopping points for buses at the stop
        start_point_id = self.check_point_id(start_id)
        end_point_id = self.check_point_id(end_id)

        # Possible ways of running the line through a given stop
        start_variant_id = self.check_variant_id(start_point_id)
        end_variant_id = self.check_variant_id(end_point_id)

        # Common combinations of connections
        both_variant_id = self.check_both_variant_id(start_variant_id, end_variant_id)

        # Convert List elements from int to str
        self.int_to_str(start_point_id)
        self.int_to_str(both_variant_id)
        self.int_to_str(end_point_id)

        all_routes = self.search_all_routes(start_point_id, end_point_id)
        next_bus_stops = self.choose_unique(all_routes)
        self.route = copy.deepcopy(next_bus_stops)
        next_bus_stops = self.choose_unique_routes(next_bus_stops)
        self.bus_stops = self.choose_shortest(next_bus_stops)
        self.bus_stops = [i for k in self.bus_stops for i in k]
        bus_stops_length = len(self.bus_stops) - 1
        choose_line = []
        first_bus_stops = self.search_connections(self.bus_stops[0], self.bus_stops[1])

        self.ready = self.which_bus_lines_on_route(first_bus_stops, self.bus_stops, choose_line, bus_stops_length)
        self.score = self.count(self.ready, self.penalty)

        i = 0
        routes = []
        if self.score != []:
            while self.score[i] == self.score[0]:
                routes.append(set(self.ready[i]))
                if i == (len(self.score) - 1):
                    break
                i += 1
            return routes
        return 0

    def show(self):
        """Prints final results."""
        ready_set = copy.deepcopy(self.ready)
        tmp = self.score[0]
        i = 0
        length_ready_set = len(ready_set)
        for i in range(length_ready_set):
            ready_set[i] = set(ready_set[i])
        my_string = "Łączne wyniki z karą za przesiadkę= {} na trasie {} - {}:"
        print(my_string.format(self.penalty, self.start[0], self.end_station[0]))

        amount = 0
        while self.score[amount] <= tmp:
            amount += 1


        for i in range(amount):
            first = self.start[0]
            print("\nTrasa nr ", i + 1)
            print("Linią ", self.ready[i][0], " na trasie", end=": ")
            for j in range(len(self.ready[i]) - 1):
                if self.ready[i][j] != self.ready[i][j + 1]:
                    print(first, "-", self.bus_stops[j + 1])
                    print("Linią ", self.ready[i][j + 1], " na trasie", end=": ")
                    first = self.bus_stops[j + 1]
            else:
                print(first, "-", self.end_station[0])

        return i

    def show_v2(self):
        """Prints final results."""
        amount = self.show()
        for i in range(amount):
            first = self.start[0]
            print("\nTrasa nr ", i + 1)
            print("Linią ", self.ready[i][0], " na trasie", end=": ")
            for j in range(len(self.ready[i]) - 1):
                if self.ready[i][j] != self.ready[i][j + 1]:
                    print(first, "-", self.route[j + 1])
                    print("Linią ", self.ready[i][j + 1], " na trasie", end=": ")
                    first = self.route[j + 1]
            else:
                print(first, "-", self.end_station[0])
                break


class Route:
    """Searches for all stops on a given bus line. """

    def __init__(self):
        self.conn = sqlite3.connect("rozklady.sqlite3")
        self.c = self.conn.cursor()

        self.route = []
        self.bus_line = ()

    def bus_line_route(self, bus_line_number):
        """Returns tuple of stop number and stop name"""
        self.bus_line = (bus_line_number,)
        variant_id = []
        stop = self.c.execute("SELECT Id FROM Variants WHERE LineName=?", self.bus_line)
        for row in stop:
            variant_id.append(row[0])
        variant_id = list(set(variant_id))
        # print(VariantID)

        for i in enumerate(variant_id):
            stop = self.c.execute("SELECT No, StopName FROM Routes  WHERE VariantID=?",
                                    (variant_id[i[0]],))
            for row in stop:
                self.route.append([row[0], row[1]])
        return self.route

    def show(self):
        """Prints route of the line"""
        for i in self.route:
            if i[0] == 0:
                print("")
            print(i[0], i[1])

    def close_database(self):
        """Closes database."""
        self.c.close()
        self.conn.close()


connection_graph = Graph()
connection_graph.generate()


def main():
    while True:
        print("\nWybierz opcje:")
        print("1.Polaczenia bezposrednie:")
        print("2.Najkrótsze połączenia:")
        print("3.Trasa danej linii:")
        print("4.Koniec")

        choose = input()
        if choose == '1':
            direct_connections = DirectConnections()
            direct_connections.enter_data()
            direct_connections.search_direct_connection()
            direct_connections.show()
            direct_connections.close_database()

        if choose == '2':
            all_routes = AllRoutes()
            all_routes.enter_data()
            all_routes.search()
            all_routes.show()
            all_routes.close_database()

        if choose == '3':
            bus_line = input("Podaj numer linii: ")
            bus_line_timetable = Route()
            bus_line_timetable.bus_line_route(bus_line)
            bus_line_timetable.show()
            bus_line_timetable.close_database()

        if choose == '4':
            break

if __name__ == '__main__':
    main()
