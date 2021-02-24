""" The module contains the functions needed for creating GUI

    Typical usage example:
    root = tk.Tk()
    root.geometry("1000x1000")
    root.resizable(width=False, height=False)

    canvas = tk.Canvas(root, height=1000, width=1000, bg=BG_COLOR)
    canvas.pack()

    gui = GUI()
    gui.ekran_poczatkowy()

    root.mainloop()
    gui.zamknij_baze()
"""
import tkinter as tk
from tkinter import messagebox
import sqlite3
import copy
import szukaj

FILE = "Logo.png"
BG_COLOR = "#aaaaaa"
FONT = "Times New Roman"


class Logo:
    """Creates logo on main screen."""

    def __init__(self):
        self.photo = tk.PhotoImage(file=FILE, )
        self.logo = tk.Label(root, image=self.photo, bd=0)

    def show(self):
        """Creates logo."""
        self.logo.place(relx=0, rely=0)

    def destroy(self):
        """Destroys logo"""
        self.logo.destroy()


class Description:
    """Creates description for entries"""

    def __init__(self, position_x, position_y, text, font_size):
        self.position_x = position_x
        self.position_y = position_y
        self.text = text
        self.font = font_size
        self.description = tk.Label(root, text=self.text, bg=BG_COLOR, font=(FONT, self.font))

    def show(self):
        """Creates string."""
        self.description.place(relx=self.position_x, rely=self.position_y)

    def destroy(self):
        """Destroys string."""
        self.description.destroy()


class Error(Description):
    """Creates string for errors."""

    def __init__(self, position_x, position_y, text, font_size):
        self.position_x = position_x
        self.position_y = position_y
        self.text = text
        self.font = font_size
        super().__init__(self.position_x, self.position_y, self.text, self.font)

    def show(self):
        """Creates label."""
        self.description = tk.Label(root, text=" ", bg=BG_COLOR, font=(FONT, self.font), foreground='red')
        self.description.place(relx=self.position_x, rely=self.position_y)

    def config(self):
        """Change label text."""
        self.description.config(text=self.text)


class TextInput:
    """Creates entry space."""

    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.pole = tk.Entry(root)

    def show(self):
        """Creates entry."""
        self.pole.place(relwidth=0.4, relheight=0.05, relx=self.position_x, rely=self.position_y)

    def get(self):
        """Gets entry value."""
        return self.pole.get()

    def destroy(self):
        """Destroy entry."""
        self.pole.destroy()


class Button:
    """Creates button for given arguments."""

    def __init__(self, width, height, position_x, position_y, text, function):
        self.width = width
        self.height = height
        self.position_x = position_x
        self.position_y = position_y
        self.text = text
        self.function = function
        self.button = tk.Button(root, text=self.text, command=self.function)

    def show(self):
        """Creates button."""
        self.button.place(relwidth=self.width, relheight=self.height,
                          relx=self.position_x, rely=self.position_y)

    def destroy(self):
        """Destroy button."""
        self.button.destroy()


class Route:
    """Searches for all bus stops for given line."""

    def __init__(self, choose, bus_line_route):
        self.choose = choose
        self.bus_line_route = bus_line_route

    def bus_lines(self):
        """Prints all bus stops for given line."""
        j = 0
        first = []
        second = []
        first.append([self.bus_line_route[0][0], self.bus_line_route[0][1]])
        for bus_stop in self.bus_line_route[1:]:
            if j == 0:
                if bus_stop[0] == 0:
                    j += 1
                    second.append([bus_stop[0], bus_stop[1]])
                    continue
                first.append([bus_stop[0], bus_stop[1]])
            if j == 1:
                if bus_stop[0] == 0:
                    j += 1
                else:
                    second.append([bus_stop[0], bus_stop[1]])

        label1 = " "
        label2 = " "
        label3 = " "
        label4 = " "

        length_1 = len(first)
        length_2 = len(second)
        if self.choose == 1:
            for i in range(length_1):
                if i <= int(length_1 / 2):
                    label1 += "{} {} \n".format(str(first[i][0]), first[i][1])
                else:
                    label2 += "{} {} \n".format(str(first[i][0]), first[i][1])
                i += 1
        if self.choose == 2:
            for i in range(length_2):
                if i <= int(length_2 / 2):
                    label3 += "{} {} \n".format(str(second[i][0]), second[i][1])
                else:
                    label4 += "{} {} \n".format(str(second[i][0]), second[i][1])

        # Labels
        if self.choose == 1:
            self.show_bus_route_str_1 = Description(0.15, 0.1, label1, 14)
            self.show_bus_route_str_1.show()

            self.show_bus_route_str_2 = Description(0.55, 0.1, label2, 14)
            self.show_bus_route_str_2.show()
        if self.choose == 2:
            self.show_bus_route_str_3 = Description(0.15, 0.1, label3, 14)
            self.show_bus_route_str_3.show()

            self.show_bus_route_str_4 = Description(0.55, 0.1, label4, 14)
            self.show_bus_route_str_4.show()

    def destroy(self):
        """Destroys strings."""
        try:
            self.show_bus_route_str_1.destroy()
            self.show_bus_route_str_2.destroy()
        except AttributeError:
            pass
        try:
            self.show_bus_route_str_3.destroy()
            self.show_bus_route_str_4.destroy()
        except AttributeError:
            pass


class RouteWithBusStops:
    """Searches for shortest routes between two bus stops with total score."""

    def __init__(self, start, end, ready, penalty, route, amount, score, tmp):
        self.start = start
        self.end = end
        self.ready = ready
        self.penalty = penalty
        self.route = route
        self.amount = amount
        self.score = score
        self.tmp = tmp

    def show_description(self):
        """Prints routes between two bus stops."""
        ready_description = " "
        for i in range(self.tmp, self.amount):
            first = self.start[0]
            which_route = i + 1
            tmp = str(which_route)
            ready_description += "\nTrasa nr {} \t\tWynik: {}".format(tmp,
                                                                  str(self.score[which_route - 1]))
            ready_description += "\nLinią {} na trasie: ".format(str(self.ready[i][0]))
            for j in range(len(self.ready[i]) - 1):
                if self.ready[i][j] != self.ready[i][j + 1]:
                    ready_description += "{}-{}\n".format(str(first), self.route[j + 1])
                    ready_description += "Linią {} na trasie".format(str(self.ready[i][j + 1]))
                    first = self.route[j + 1]
                    # print(koncowy_napis)
            else:
                ready_description += "{}-{}\n".format(str(first), str(self.end[0]))
                # print(koncowy_napis)

        self.showed_bus_stops = Description(0.36, 0.18, ready_description, 12)
        self.showed_bus_stops.show()

    def destroy(self):
        """Destroy routes string."""
        self.showed_bus_stops.destroy()


class DirectRouteWithBusStops:
    """Searches for direct routes between two bus stops."""

    def __init__(self, start, end, penalty, both_variant_line, amount, score, tmp):
        self.start = start
        self.end = end
        self.both_variant_line = both_variant_line
        self.penalty = penalty
        self.amount = amount
        self.score = score
        self.tmp = tmp

    def show_description(self):
        """Prints routes between two bus stops."""
        ready_description = " "
        for i in range(self.tmp, self.amount):
            which_route = i + 1
            ready_description += "\n\nTrasa nr {} \t\tWynik: {}".format(str(which_route),
                                                                    str(self.score[i]))
            ready_description += "\nLinią {} na trasie: {}-{} \n".format(str(self.both_variant_line[i]),
                                                                     str(self.start[0]),
                                                                     str(self.end[0]))
        if self.amount == 0:
            ready_description += "\n\nBrak bezposrednich polaczen na danej trasie "
        self.showed_bus_stops = Description(0.36, 0.18, ready_description, 12)
        self.showed_bus_stops.show()

    def destroy(self):
        """Destroy route string."""
        self.showed_bus_stops.destroy()


def close():
    """Closes the programm."""
    response = messagebox.askokcancel("Potwierdzenie", "Czy na pewno chcesz zamknąć program?")
    if response:
        root.quit()


class GUI(Route, szukaj.AllRoutes, szukaj.DirectConnections, RouteWithBusStops):
    """Creates GUI"""

    def __init__(self):
        self.conn = sqlite3.connect("rozklady.sqlite3")
        self.c = self.conn.cursor()

        self.bus_line_route_2 = szukaj.Route()
        self.exist = 0
        self.tmp = 0
        self.temporary = 1

        self.error = Error(0.73, 0.79, "Taka linia nie isnieje", 14)
        self.error.show()

        self.error_start = Error(0.73, 0.36, "Taki przystanek nie isnieje", 14)
        self.error_start.show()

        self.error_end = Error(0.73, 0.46, "Taka przystanek nie isnieje", 14)
        self.error_end.show()

        self.error_penalty = Error(0.73, 0.56, "Wprowadzono zle dane", 14)
        self.error_penalty.show()

        self.first = []
        self.second = []

    def main_screen(self):
        """Creates main screen."""
        self.logo()
        self.search_strings()
        self.data_inputs()
        self.search_buttons()

    def logo(self):
        """Shows logo."""
        self.image = Logo()
        self.image.show()

    def search_strings(self):
        """Creates strings."""
        self.first_bus_stop_text = Description(0.3, 0.32, "Przystanek początkowy:", 12)
        self.first_bus_stop_text.show()

        self.last_bus_stop_text = Description(0.3, 0.42, "Przystanek końcowy", 12)
        self.last_bus_stop_text.show()

        self.penalty_text = Description(0.3, 0.52, "Kara za przesiadkę:", 12)
        self.penalty_text.show()

        self.bus_line_text = Description(0.3, 0.75, "Wybierz linie", 12)
        self.bus_line_text.show()

    def data_inputs(self):
        """Creates entry spaces."""
        self.first = TextInput(0.3, 0.35)
        self.first.show()

        self.last = TextInput(0.3, 0.45)
        self.last.show()

        self.change_line = TextInput(0.3, 0.55)
        self.change_line.show()

        self.bus_line = TextInput(0.3, 0.78)
        self.bus_line.show()

    def search_buttons(self):
        """Creates search buttons"""
        self.search_button = Button(0.19, 0.05, 0.3, 0.65, "Szukaj najkrótszych polaczen",
                                    self.get_values_bus_stops)
        self.search_button.show()

        self.search_direct_button = Button(0.19, 0.05, 0.51, 0.65,
                                                   "Szukaj bezpośrednich polaczen",
                                           self.get_values_direct_routes)
        self.search_direct_button.show()

        self.route_button = Button(0.2, 0.05, 0.4, 0.88,
                                     'Pokaż trasę linii', self.get_line_names)
        self.route_button.show()

    def check_penalty(self):
        """Returns penalty for change line."""
        self.penalty = self.change_line.get()
        try:
            self.penalty = float(self.penalty)
            if 0 <= self.penalty <= 100:
                return self.penalty
            return -1
        except ValueError:
            return -1

    def zniszcz_początkowy(self):
        """Destroy all start elements on screen"""
        self.first.destroy()
        self.last.destroy()
        self.change_line.destroy()
        self.first_bus_stop_text.destroy()
        self.last_bus_stop_text.destroy()
        self.penalty_text.destroy()
        self.search_button.destroy()
        self.search_direct_button.destroy()
        self.bus_line_text.destroy()
        self.bus_line.destroy()
        self.route_button.destroy()
        self.image.destroy()

    def get_value(self, pole):
        """Returns bus names."""
        start = pole.get()
        stop = self.c.execute("SELECT Name FROM Stops")
        for rows in stop:
            if start == rows[0]:
                return start
        return 0

    def get_values_bus_stops(self):
        """Gets bus stops name"""
        self.start = self.get_value(self.first)
        self.end = self.get_value(self.last)
        self.penalty = self.check_penalty()

        if self.start == 0:
            self.error_start.config()

        if self.end == 0:
            self.error_end.config()

        if self.penalty == -1:
            self.error_penalty.config()

        if self.start != 0:
            self.error_start.destroy()
            self.error_start = Error(0.73, 0.36, "Taki przystanek nie isnieje", 14)
            self.error_start.show()

        if self.end != 0:
            self.error_end.destroy()
            self.error_end = Error(0.73, 0.46, "Taka przystanek nie isnieje", 14)
            self.error_end.show()

        if self.penalty != -1:
            self.error_penalty.destroy()
            self.error_penalty = Error(0.73, 0.56, "Wprowadzono zle dane", 14)
            self.error_penalty.show()

        if self.start != 0 and self.end != 0 and self.penalty != -1:
            self.zniszcz_początkowy()
            self.search_routes()

    def get_values_direct_routes(self):
        """Gets bus stops name."""
        self.start = self.get_value(self.first)
        self.end = self.get_value(self.last)
        self.penalty = self.check_penalty()

        if self.start == 0:
            self.error_start.config()

        if self.end == 0:
            self.error_end.config()

        if self.penalty == -1:
            self.error_penalty.config()

        if self.start != 0:
            self.error_start.destroy()
            self.error_start = Error(0.73, 0.36, "Taki przystanek nie isnieje", 14)
            self.error_start.show()

        if self.end != 0:
            self.error_end.destroy()
            self.error_end = Error(0.73, 0.46, "Taka przystanek nie isnieje", 14)
            self.error_end.show()

        if self.penalty != -1:
            self.error_penalty.destroy()
            self.error_penalty = Error(0.73, 0.56, "Wprowadzono zle dane", 14)
            self.error_penalty.show()

        if self.start != 0 and self.end != 0 and self.penalty != -1:
            # Zniszczenie pól
            self.zniszcz_początkowy()
            self.search_direct_routes()

    def show(self):
        """Returns how many results are."""
        ready_set = copy.deepcopy(self.ready)
        tmp = self.score[0]
        amount = 0
        ready_set_length = len(ready_set)
        for i in range(ready_set_length):
            ready_set[i] = set(ready_set[i])

        while self.score[amount] <= tmp:
            amount += 1

        return amount - 1

    def search_routes(self):
        """Searches for routes with total score."""
        # Show results
        description = "Trasa {} - {} z karąza przesiadkę równą {}".format(self.start, self.end, self.penalty)
        self.route_search = Description(0.27, 0.1, description, 16)
        self.route_search.show()

        self.start = (self.start,)
        self.end = (self.end,)
        # Search route
        all_routes = szukaj.AllRoutes()
        start_id = (all_routes.check_id(self.start),)
        end_id = (all_routes.check_id(self.end),)

        # Possible stopping points for buses at the stop
        start_point_id = all_routes.check_point_id(start_id)
        end_point_id = all_routes.check_point_id(end_id)

        # Possible ways of running the line through a given stop
        start_variant_id = all_routes.check_variant_id(start_point_id)
        end_variant_id = all_routes.check_variant_id(end_point_id)

        # Common combinations of connections
        both_variant_id = all_routes.check_both_variant_id(start_variant_id, end_variant_id)

        # Convert int to str
        all_routes.int_to_str(start_point_id)
        all_routes.int_to_str(both_variant_id)
        all_routes.int_to_str(end_point_id)

        all_possible_routes = all_routes.search_all_routes(start_point_id, end_point_id)
        next_bus_stops = all_routes.choose_unique(all_possible_routes)
        self.bus_route = copy.deepcopy(next_bus_stops)
        next_bus_stops = all_routes.choose_unique_routes(next_bus_stops)
        self.bus_stops = all_routes.choose_shortest(next_bus_stops)
        self.bus_stops = [i for k in self.bus_stops for i in k]
        self.bus_stops_length = len(self.bus_stops) - 1
        bus_line = []
        first = all_routes.search_connections(self.bus_stops[0], self.bus_stops[1])

        self.ready = all_routes.which_bus_lines_on_route(first, self.bus_stops,
                                                         bus_line, self.bus_stops_length)
        self.score = all_routes.count(self.ready, self.penalty)

        self.amount = self.show() + 1

        if self.amount < 8:
            self.route_with_bus_stops = RouteWithBusStops(self.start, self.end, self.ready,
                                                          self.penalty, self.bus_stops,
                                                          self.amount, self.score, self.tmp)
            self.route_with_bus_stops.show_description()

        else:
            self.route_with_bus_stops = RouteWithBusStops(self.start, self.end, self.ready, self.penalty,
                                                          self.bus_stops, 7, self.score, self.tmp)
            self.route_with_bus_stops.show_description()
            self.tmp += 7

            self.show_more_button = Button(0.3, 0.05, 0.35, 0.78, "Pokaż więcej", self.show_more)
            self.show_more_button.show()
            self.exist = 1

        self.exit_button = Button(0.3, 0.05, 0.15, 0.85, "Zamknij", close)
        self.exit_button.show()

        self.go_back_button = Button(0.3, 0.05, 0.55, 0.85, "Wróć", self.go_back_route)
        self.go_back_button.show()

    def show_more(self):
        """Shows more routes."""
        self.route_with_bus_stops.destroy()
        if self.tmp > self.amount:
            self.tmp = 0
            self.temporary = 0
        self.temporary += 1
        max_deep = 7 * self.temporary
        if max_deep > self.amount:
            max_deep = self.amount
        self.route_with_bus_stops = RouteWithBusStops(self.start, self.end, self.ready,
                                                      self.penalty, self.bus_stops,
                                                      max_deep, self.score, self.tmp)
        self.route_with_bus_stops.show_description()
        self.tmp += 7

    def search_direct_routes(self):
        """Searches for direct routes between two bus stops."""
        # Show results
        str1 = "Trasa {} - {} z karą za przesiadkę równą {}".format(self.start, self.end, self.penalty)
        self.route_search = Description(0.27, 0.1, str1, 16)
        self.route_search.show()

        self.start = (self.start,)
        self.end = (self.end,)
        # Search route
        direct_connections = szukaj.DirectConnections()
        start_id = (direct_connections.check_id(self.start),)
        end_id = (direct_connections.check_id(self.end),)

        # Possible stopping points for buses at the stop
        start_point_id = direct_connections.check_point_id(start_id)
        end_point_id = direct_connections.check_point_id(end_id)

        # Possible ways of running the line through a given stop
        start_variant_id = direct_connections.check_variant_id(start_point_id)
        end_variant_id = direct_connections.check_variant_id(end_point_id)

        # Common combinations of connections
        both_variant_id = direct_connections.check_both_variant_id(start_variant_id, end_variant_id)

        variant_id = (both_variant_id,)
        self.both_variant_line = direct_connections.id_to_bus_line(variant_id)

        direct_connections.int_to_str(start_point_id)
        direct_connections.int_to_str(both_variant_id)
        direct_connections.int_to_str(end_point_id)

        self.stop_no = direct_connections.which_bus_stop(start_point_id, both_variant_id)
        self.stop_no2 = direct_connections.which_bus_stop(end_point_id, both_variant_id)

        bus_stops = direct_connections.choose_appropriate_bus_stops(self.stop_no, self.stop_no2)
        bus_stops_start = bus_stops[0]
        bus_stops_end = bus_stops[1]

        self.bus_stops_amount = self.how_many_bus_stops(bus_stops_start, bus_stops_end)
        self.routes_amount = len(self.both_variant_line)

        if self.routes_amount < 8:
            self.route_with_bus_stops = DirectRouteWithBusStops(self.start, self.end, self.penalty,
                                                                self.both_variant_line, self.routes_amount,
                                                                self.bus_stops_amount, self.tmp)
            self.route_with_bus_stops.show_description()
        else:
            self.route_with_bus_stops = DirectRouteWithBusStops(self.start, self.end, self.penalty,
                                                                self.both_variant_line, 7,
                                                                self.bus_stops_amount, self.tmp)
            self.route_with_bus_stops.show_description()
            self.tmp += 7

            self.show_more_button = Button(0.3, 0.05, 0.35, 0.78, "Pokaż więcej",
                                           self.show_more_direct_connections)
            self.show_more_button.show()
            self.exist = 1

        self.exit_button = Button(0.3, 0.05, 0.15, 0.85, "Zamknij", close)
        self.exit_button.show()

        self.go_back_button = Button(0.3, 0.05, 0.55, 0.85, "Wróć", self.go_back_route)
        self.go_back_button.show()

    def show_more_direct_connections(self):
        """Shows more connections."""
        self.route_with_bus_stops.destroy()
        if self.tmp > self.routes_amount:
            self.tmp = 0
            self.temporary = 0
        self.temporary += 1
        max_deep = 7 * self.temporary
        if max_deep > self.routes_amount:
            max_deep = self.routes_amount
        self.route_with_bus_stops = DirectRouteWithBusStops(self.start, self.end, self.penalty,
                                                            self.both_variant_line, max_deep,
                                                            self.bus_stops_amount, self.tmp)
        self.route_with_bus_stops.show_description()
        self.tmp += 7

    def go_back_bus_lines(self):
        """Backs to previous screen."""
        self.error = Error(0.73, 0.79, "Taka linia nie isnieje", 14)
        self.error.show()
        self.route_description.destroy()
        self.exit.destroy()
        self.again.destroy()
        self.reverse.destroy()
        self.which_route.destroy()

        self.logo()
        self.search_strings()
        self.data_inputs()
        self.search_buttons()

    def go_back_route(self):
        """Backs to previous screen."""
        self.temporary = 1
        self.tmp = 0
        self.route_with_bus_stops.destroy()
        self.route_search.destroy()
        self.exit_button.destroy()
        self.go_back_button.destroy()
        if self.exist == 1:
            self.show_more_button.destroy()
        self.logo()
        self.search_strings()
        self.data_inputs()
        self.search_buttons()

    def reverse_route(self):
        """Revesres route."""
        self.choose = self.which_route.choose
        self.which_route.destroy()
        if self.choose == 1:
            self.which_route.choose = 2
            self.which_route.bus_lines()
            # print(self.trasa_linii)
            # self.jakaDroga = Trasa(2,self.trasa_linii)
        elif self.choose == 2:
            self.which_route.choose = 1
            self.which_route.bus_lines()
            # print(self.trasa_linii)
            # self.jakaDroga = Trasa(1,self.trasa_linii)

    def destroy_main_screen(self):
        """Destroys all elements on start menu."""
        self.error.destroy()
        self.image.destroy()
        self.first.destroy()
        self.last.destroy()
        self.change_line.destroy()
        self.first_bus_stop_text.destroy()
        self.last_bus_stop_text.destroy()
        self.penalty_text.destroy()
        self.search_button.destroy()
        self.search_direct_button.destroy()
        self.bus_line_text.destroy()
        self.bus_line.destroy()
        self.route_button.destroy()

    def get_line_names(self):
        """Gets line name."""
        self.route = self.bus_line.get()
        try:
            self.bus_route = int(self.route)
            stop = self.c.execute("SELECT Name FROM Lines")
            for rows in stop:
                if self.route == rows[0]:
                    self.route = rows[0]
                    break
            else:
                self.route = -1
                self.error.config()
        except ValueError:
            self.route = -1
            self.error.config()

        if self.route != -1:
            self.destroy_main_screen()

            self.bus_line_route = self.bus_line_route_2.bus_line_route(self.route)

            self.route_description = Description(0.43, 0.05, "Trasa linii:" + str(self.route), 16)
            self.route_description.show()

            j = 0
            self.first = []
            self.second = []
            self.first.append([self.bus_line_route[0][0], self.bus_line_route[0][1]])
            for stop in self.bus_line_route[1:]:
                if j == 0:
                    if stop[0] == 0:
                        j += 1
                        self.second.append([stop[0], stop[1]])
                        continue
                    self.first.append([stop[0], stop[1]])
                if j == 1:
                    if stop[0] == 0:
                        j += 1
                    self.second.append([stop[0], stop[1]])
            i = 0

            self.choose = 2
            self.which_route = Route(self.choose, self.bus_line_route)
            self.which_route.bus_lines()

            self.exit = Button(0.2, 0.05, 0.7, 0.85, "Zamknij", close)

            self.again = Button(0.2, 0.05, 0.4, 0.85, "Wróć", self.go_back_bus_lines)

            self.reverse = Button(0.2, 0.05, 0.1, 0.85, "Odwróc", self.reverse_route)

            self.exit.show()
            self.again.show()
            self.reverse.show()

    def close_database(self):
        """Closes database."""
        self.c.close()
        self.conn.close()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1000x1000")
    root.resizable(width=False, height=False)

    canvas = tk.Canvas(root, height=1000, width=1000, bg=BG_COLOR)
    canvas.pack()

    gui = GUI()
    gui.main_screen()

    root.mainloop()
    gui.close_database()
