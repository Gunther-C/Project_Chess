from tkinter import Tk, Menu, Toplevel, Frame, Label, Canvas, messagebox, Scrollbar, PhotoImage, UNITS
from datetime import date
import subprocess
import webbrowser
import os
import re

from database.data_players import PlayersData
from database.data_tournaments import TournamentData


class Core(Tk):
    def __init__(self):
        super().__init__()

        self.master_id = self.winfo_id()

        self.data_transfer = None

        self.menu_options = None
        self.menu_players = None
        self.menu_tour = None

        self.new_player = None
        self.new_tournament = None

        self.menu_listing = None
        self.frame = None
        self.frame_list = None

        self.widjets_menu = False
        self.widjets_menu1 = False
        self.widjets_menu2 = False
        self.widjets_menu3 = False
        self.widjets_menu4 = False

        self.view_master = self.master_window(50, 60)
        self.minsize(width=int(self.view_master[0] * 0.60), height=int(self.view_master[1] * 0.90))
        self.title(" Echec")
        self.config(bg="#FEF9E7")
        # self.iconphoto(False, PhotoImage(file='views/pictures/horse.png'))

        self.background = Label(self, bg="#FEF9E7", width=int(self.view_master[0] * 0.40),
                                height=int(self.view_master[1] * 0.50))
        self.background.image = PhotoImage(file="views/pictures/Chess_mini.png")
        self.background['image'] = self.background.image
        self.background.grid()
        self.background.place(relx=0.5, rely=0.5, anchor='center')

        self.menu = Menu(self)

    def master_window(self, child_width, child_height):
        """
        :param child_width:
        :param child_height:
        :return: Placement / dimension fenêtre principale
        """
        view_x: list = self.window_x(self.winfo_screenwidth(), child_width)
        view_y: list = self.window_y(self.winfo_screenheight(), child_height)
        self.geometry('{}x{}+{}+{}'.format(view_x[0], view_y[0], view_x[1], view_y[1]))

        return [view_x[0], view_y[0]]

    def listing_window(self, percent_width, percent_height, place_x, place_y, title, bg):
        """
        :param percent_width:
        :param percent_height:
        :param place_x:
        :param place_y:
        :param title:
        :param bg:
        :return: Fenêtre supplémentaire
        """
        new_window = Toplevel(self)
        view_x: list = self.window_x(self.winfo_screenwidth(), percent_width)
        view_y: list = self.window_y(self.winfo_screenheight(), percent_height)
        new_window.geometry('{}x{}+{}+{}'.format(view_x[0], view_y[0], place_x, place_y))
        new_window.minsize(width=view_x[0], height=view_y[0])
        new_window.title(title)
        new_window.config(bg=bg)
        return new_window, view_x[0], view_y[0]

    def searching(self, **kwargs: any) -> False:
        """
        :param kwargs:
        :return: Recherchée correspondance
            si le joueur est déja dans la bdd à l'inscription
            recherche si un joueur éxiste retourne ses infos en cas de success
            Si plusieurs joueurs ont le mème nom retourne une list des joueurs
        """
        file_players = self.players_list()
        multi_player = []

        if file_players:
            type_search = 1
            last_name = None
            first_name = None
            birth = None
            identity = None
            if 'last_name' in kwargs:
                last_name = kwargs['last_name'].strip().replace(' ', '').lower()
            if 'first_name' in kwargs:
                first_name = kwargs['first_name'].strip().replace(' ', '').lower()
            if 'birth' in kwargs:
                birth = kwargs['birth']
            if 'identity' in kwargs:
                identity = kwargs['identity']
                id_last = identity[:2]
                if not id_last.isupper():
                    id_last = id_last.upper()
                    id_first = identity[2:]
                    identity = id_last + id_first

            for player in file_players:

                data_user = []
                for keys, values in player.items():
                    if keys == 'last_name':
                        values = values.strip().replace(' ', '').lower()
                        if last_name == values:
                            data_user.append(values)

                    if keys == 'first_name':
                        values = values.strip().replace(' ', '').lower()
                        if first_name == values:
                            data_user.append(values)

                    if keys == 'birth':
                        if birth == values:
                            data_user.append(values)

                    if keys == 'identity':
                        if identity == values:
                            data_user.append(values)

                if kwargs['search_type'] == 'compare':
                    type_search = 3

                if len(data_user) == type_search:
                    multi_player.append(player)

        return multi_player

    def clear_frame(self, clear_type: str, frame: any) -> None:
        """
        :param clear_type:
        :param frame:
        :return: Néttoyage de la frame tkinter en cours
        """
        if frame:
            for widget in frame.winfo_children():
                widget.destroy()

        if clear_type == 'continu':
            self.background.destroy()
        else:
            self.background = Label(self, bg="#FEF9E7", width=int(self.view_master[0] * 0.40),
                                    height=int(self.view_master[1] * 0.50))
            self.background.image = PhotoImage(file="views/pictures/Chess_mini.png")
            self.background['image'] = self.background.image
            self.background.grid()
            self.background.place(relx=0.5, rely=0.5, anchor='center')

    @staticmethod
    def debug():
        """
        :return: Traitement flake8
        """
        try:
            subprocess.run(["flake8", "--format=html", "--htmldir=flake8_rapport"])

            try:
                chemin = os.getcwd()
                fichier_html = f"{chemin}/flake8_rapport/index.html"
                webbrowser.open(fichier_html)

            except ValueError as er:
                print("Erreur lors de l'ouverture du fichier :", er)

        except subprocess.CalledProcessError as e:
            messagebox.showwarning(title='Avertissement', message=f"Erreur : {e}")

    @staticmethod
    def listing_canvas(curent_frame, rw, bg_color, dimension):
        """
        :param curent_frame:
        :param rw:
        :param bg_color:
        :param dimension:
        :return: Canvas avec scrollbar
        """
        dimension_x = int(dimension[0] - 60)
        dimension_y = int((dimension[1] - 30))

        canvas = Canvas(curent_frame)
        frame_list = Frame(canvas, bg=bg_color, pady=40)

        scrollbar = Scrollbar(curent_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=rw, column=1, sticky='ns')

        canvas.configure(yscrollcommand=scrollbar.set, bg=bg_color, width=dimension_x, height=dimension_y,
                         highlightthickness=0)
        canvas.grid(row=rw, column=0)

        canvas.update()
        frame_list.update()
        return frame_list, canvas, dimension_x, dimension_y

    @staticmethod
    def canvas_roll(canvas, frame, view_x, view_y):
        """
        :param canvas:
        :param frame:
        :param view_x:
        :param view_y:
        :return: Traitement scrollbar du canvas
        """
        def roll_wheel(event):
            direction = 0
            if event.num == 5 or event.delta == -120:
                direction = 1
            if event.num == 4 or event.delta == 120:
                direction = -1
            event.widget.yview_scroll(direction, UNITS)

        def new_scroll(vw_x, vw_y):
            canvas.configure(scrollregion=canvas.bbox("all"), width=vw_x, height=vw_y)

        canvas.update()
        canvas.create_window((0, 0), window=frame)
        frame.bind("<Configure>", lambda event: new_scroll(view_x, view_y), add=True)
        canvas.bind('<MouseWheel>', lambda event: roll_wheel(event), add=True)
        canvas.bind('<Button-4>', lambda event: roll_wheel(event), add=True)
        canvas.bind('<Button-5>', lambda event: roll_wheel(event), add=True)

    @staticmethod
    def players_list() -> False:
        """
        :return: fichier json des joueurs
        """
        file_players = PlayersData().load_players_file()
        if file_players:
            return file_players

    @staticmethod
    def tournaments_list() -> False:
        """
        :return: fichier json des tournois
        """
        tournament = TournamentData().load_tournament_file()
        if tournament:
            return tournament

    @staticmethod
    def window_x(parent, child_width) -> list:
        """
        :param parent:
        :param child_width:
        :return: Ajuster la largeur de la fenêtre en pourcentage, centrer sur l'écran
        valeur1 = Largeur de la fenêtre
        valeur2 = Différence entre la largeur de la fenêtre et celle de l'écran
                  (diviser par deux pour les marges gauche et droite de la fenêtre)
        """
        screen_width = parent
        unity = int(screen_width / 100)
        window_width = unity * int(child_width)
        modulo_width = (screen_width - window_width) // 2
        return [window_width, modulo_width]

    @staticmethod
    def window_y(parent, child_height) -> list:
        """
        :param parent:
        :param child_height:
        :return: Ajuster la hauteur de la fenêtre en pourcentage, centrer sur l'écran
        valeur1 = hauteur de la fenêtre
        valeur2 = Différence entre la hauteur de la fenêtre et celle de l'écran
                  (diviser par deux pour les marges haut et bas de la fenêtre)
        """
        screen_height = parent
        unity = int(screen_height / 100)
        window_height = unity * int(child_height)
        modulo_height = (screen_height - window_height) // 2
        return [window_height, modulo_height]

    @staticmethod
    def number_verif(arg_type, number) -> False:
        """
        :param arg_type:
        :param number:
        :return: erreur ciblée si la saisie n'est pas un nombre entier
        """
        number = number.replace(" ", "").strip()
        new_nbr = number.isdigit()
        if not new_nbr:
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
                    elif number[0] == '0':
                        return f"{arg_type} ne doit pas commencer par un ( 0 )"
                case "L'année tournoi":
                    if not len(number) == 4:
                        return f"{arg_type} doit comporter un nombre à 4 chiffres"
                    elif number[0] == '0':
                        return f"{arg_type} ne doit pas commencer par un ( 0 )"
                case "numberRound":
                    if int(number) < 1 or int(number) > 99:
                        return "Le nombre de rounds doit comporter un nombre entre 1 et 99"

    @staticmethod
    def number_float_verif(arg_type, number) -> False:
        """
        :param arg_type:
        :param number:
        :return: erreur ciblée si la saisie n'est pas zero ou cinq après la virgule
        """
        result = False
        text = f"{arg_type} Uniquement des chiffres (seul un 5 est accepté après le point, exemple :0.5 ou 10 ou 10.5"
        number = number.replace(" ", "").strip()
        point = re.search(r"[.]+", number)

        if point:
            new_number = number.find('.')
            first_number = number[:new_number]
            last_number = number[new_number + 1:]

            verif_first = first_number.isdigit()
            verif_last = last_number.isdigit()
            if not verif_first or not verif_last or last_number != '5' and last_number != '0':
                result = True

        if not point:
            verif_number = number.isdigit()
            if not verif_number:
                return text
        elif result:
            return text
        else:
            pass

    @staticmethod
    def date_verif(*args) -> False:
        """
        :param args:
        :return: La date de départ ne peut être antérieure à la date du jour !
        """
        now = date.today()
        date_verif = date(int(args[0]), int(args[1]), int(args[2]))
        if date_verif < now:
            return "La date de départ ne peut être antérieure à la date du jour !"

    @staticmethod
    def string_verif(arg_type, text) -> False:
        """
        :param arg_type:
        :param text:
        :return: la saisie doit comporter du texte et Certains caractères spéciaux
        """
        if text:
            text = text.replace(" ", "").strip()
            verif_text = re.search("[^a-zA-Z0-9-'_]+", text)
            if verif_text:
                return f"{arg_type} doit comporter du texte, \n Certains caractères spéciaux ne sont pas autorisés"

    @staticmethod
    def long_string_verif(arg_type, min_txt, max_txt, text) -> False:
        """
        :param arg_type:
        :param min_txt:
        :param max_txt:
        :param text:
        :return: Longueur du texte saisie
        """
        if text:
            text = text.replace(" ", "").strip()
            if len(text) < min_txt or len(text) > max_txt:
                return f"{arg_type} doit comporter entre {min_txt} et {max_txt} caractères"

    @staticmethod
    def identity_verif(text) -> False:
        """
        :param text:
        :return: erreur Le numéro national d'identité n'est pas valide
        """
        if text:
            text = text.replace(" ", "").strip()
            if not len(text) == 7 or not text[:2].isalpha() or not text[2:].isdigit():
                return f"Le numéro national d'identité '{text}' n'est pas valide"

    @staticmethod
    def create_error(errors_dict):
        """
        :param errors_dict:
        :return: Mise en liste des erreurs principalement de saisie
        """
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
        """
        :param frame:
        :param ctrl_number_error:
        :return: suppréssion de la liste des erreurs principalement de saisie
        """
        if frame:
            for child in frame.winfo_children():
                name = f"error{ctrl_number_error}"
                if child.winfo_name() == name:
                    ctrl_number_error += 1
                    child.destroy()

    @staticmethod
    def search_name_widget(frame, name: str) -> False:
        """
        :param frame:
        :param name:
        :return: Recherche d'un widget par son nom dans une frame
        """
        if frame:
            for child in frame.winfo_children():
                if child.winfo_name() == name:
                    return True
