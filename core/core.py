from tkinter import *
from tkinter import font, Entry
from tkinter import ttk
import re

from database import data_players as dt_players

class Core(Tk):

    def __init__(self):
        super().__init__()

        self.master_id = self.winfo_id()
        print(self.master_id)
        self.data_transfer = None

        self.menu_listing = None
        self.frame = None
        self.frame_list = None
        self.widjets_menu1 = False
        self.widjets_menu2 = False
        self.widjets_menu3 = False

        self.master_window(50, 60)
        self.minsize(width=420, height=450)
        self.title(" Echec")
        self.config(bg="#FEF9E7")
        self.iconbitmap("views/pictures/horse.ico")
        self.menu = Menu(self)

        self.new_player = None
        # self.new_player2 = None

        self.new_tournoi = None

        # self.new_w = None
        # self.new_fr = None

    def master_window(self, child_width, child_height):
        """
        Placement / dimension fenêtre principale
        """
        view_x: list = self.window_x(self.winfo_screenwidth(), child_width)
        view_y: list = self.window_y(self.winfo_screenheight(), child_height)
        self.geometry('{}x{}+{}+{}'.format(view_x[0], view_y[0], view_x[1], view_y[1]))

        return [view_x[0], view_y[0]]

    def listing_window(self, percent_width, percent_height):
        new_window = Toplevel(self)
        view_x: list = self.window_x(self.winfo_screenwidth(), percent_width)
        view_y: list = self.window_y(self.winfo_screenheight(), percent_height)
        new_window.geometry('{}x{}+{}+{}'.format(view_x[0], view_y[0], 30, 30))
        new_window.minsize(width=view_x[0], height=view_y[0])
        new_window.title(" Liste des joueurs")
        new_window.config(bg="#FEF9E7")
        new_window.iconbitmap("views/pictures/horse.ico")
        return new_window, view_x[0], view_y[0]

    def listing_canvas(self, curent_frame, bg_color, dimension):

        canvas = Canvas(curent_frame)
        self.frame_list = Frame(canvas, bg=bg_color, padx=10, pady=15)

        scrollbar = Scrollbar(curent_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        canvas.configure(yscrollcommand=scrollbar.set, bg=bg_color, width=dimension[0], height=dimension[1])
        canvas.create_window((0, 0), window=self.frame_list, anchor='nw')
        canvas.grid(row=0, column=0)

        def mouse_move(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        return self.frame_list, canvas, mouse_move, dimension[0], dimension[1]

    @staticmethod
    def players_list():
        # fichier json des joueurs
        file_players = dt_players.PlayersData().load_players_file()
        if file_players:
            return file_players

    @staticmethod
    def window_x(parent, child_width) -> list:
        screen_width = parent
        unity = int(screen_width / 100)
        window_width = unity * int(child_width)
        modulo_width = (screen_width - window_width) // 2
        return [window_width, modulo_width]

    @staticmethod
    def window_y(parent, child_height) -> list:
        screen_height = parent
        unity = int(screen_height / 100)
        window_height = unity * int(child_height)
        modulo_height = (screen_height - window_height) // 2
        return [window_height, modulo_height]

    @staticmethod
    def number_verif(arg_type, number) -> False:
        if number:
            number = number.replace(" ", "").strip()
            new_nbr = re.search(r"[a-zA-Z]+", number)
            if new_nbr:
                return f"{arg_type} doit comporter uniquement des chiffres"
            else:
                match arg_type:
                    case "Le jour":
                        if int(number) < 1 or int(number) > 31 or not len(number) == 2:
                            return f"{arg_type} doit comporter un nombre entre 01 et 31"
                    case "Le mois":
                        if int(number) < 1 or int(number) > 12 or not len(number) == 2:
                            return f"{arg_type} doit comporter un nombre entre 01 et 12"
                    case "L'année joueur":
                        if int(number) < 1900 or int(number) > 2016 or not len(number) == 4:
                            return f"{arg_type} doit comporter un nombre entre 1900 et 2016"
                    case "L'année tournoi":
                        if int(number) < 2024 or int(number) > 2100 or not len(number) == 4:
                            return f"{arg_type} doit comporter un nombre entre 2024 et 2100"
                    case "numberRound":
                        if int(number) < 1 or int(number) > 99:
                            return f"{arg_type} doit comporter un nombre entre 1 et 99"

    @staticmethod
    def string_verif(arg_type, text) -> False:
        if text:
            text = text.replace(" ", "").strip()
            new_text = re.search(r"[0-9]+", text)
            if new_text:
                return f"{arg_type} doit comporter uniquement du texte"

    @staticmethod
    def long_string_verif(arg_type, min_txt, max_txt, text) -> False:
        if text:
            text = text.replace(" ", "").strip()
            if len(text) < min_txt or len(text) > max_txt:
                return f"{arg_type} doit comporter entre {min_txt} et {max_txt} caractères"

    @staticmethod
    def identity_verif(text) -> False:
        if text:
            text = text.replace(" ", "").strip()
            if not len(text) == 7 or not text[:2].isalpha() or not text[2:].isdigit():
                return f"Le numéro national d'identité '{text}' n'est pas valide"

    @staticmethod
    def clear_frame(frame: any) -> None:
        if frame:
            for widget in frame.winfo_children():
                widget.destroy()

    @staticmethod
    def create_error(errors_dict):
        ctrl_errors = []
        if len(errors_dict) > 0:
            number_error = 0
            for txt in errors_dict.values():
                if txt is not None:
                    number_error += 1
                    name = f"error{number_error}"
                    ctrl_errors.append([name, txt])

        return ctrl_errors

    @staticmethod
    def destroy_error(frame, ctrl_number_error: int):
        if frame:
            for child in frame.winfo_children():
                name = f"error{ctrl_number_error}"
                if child.winfo_name() == name:
                    ctrl_number_error += 1
                    child.destroy()

    @staticmethod
    def search_name_widget(frame, name: str) -> False:
        if frame:
            for child in frame.winfo_children():
                if child.winfo_name() == name:
                    return True




    @staticmethod
    def instance_player(data_player, key=None, value=None):
        if key and value:
            match key:
                case 'Identité':
                    data_player[key] = value
                case 'Nom':
                    data_player[key] = value
                case 'Prénom':
                    data_player[key] = value
                case 'Date de naissance':
                    data_player[key] = value
                case _:
                    pass
        return data_player
