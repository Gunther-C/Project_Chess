from tkinter import *
from tkinter import font, Entry
from tkinter import ttk
import re


class Core(Tk):

    def __init__(self):
        super().__init__()

        self.master_id = self.winfo_id()
        print(self.master_id)
        self.data_transfer = None

        self.new_player = None
        self.new_player2 = None

        self.new_tournament = None

        self.menu_listing = None
        self.widjets_menu1 = False
        self.widjets_menu2 = False

        self.frame = None
        self.frame_list = None

        self.view_x: list = self.window_x(self.winfo_screenwidth(), 50)
        self.view_y: list = self.window_y(self.winfo_screenheight(), 60)

        self.geometry('{}x{}+{}+{}'.format(self.view_x[0], self.view_y[0], self.view_x[1], self.view_y[1]))
        self.minsize(width=420, height=450)
        self.title(" Echec")
        self.config(bg="#FEF9E7")
        self.iconbitmap("views/pictures/horse.ico")
        self.menu = Menu(self)

        """
        self.new_self = Toplevel(self)
        self.withdraw()
        self.new_self.geometry('{}x{}+{}+{}'.format(view_x[0], view_y[0], view_x[1], view_y[1]))
        self.new_self.minsize(width=350, height=400)
        self.new_self.title(" Echec")
        self.new_self.config(bg="#FEF9E7")
        self.new_self.iconbitmap("views/pictures/horse.ico")
        self.menu = Menu(self.new_self)
        """

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

    @staticmethod
    def string_verif(arg_type, text) -> False:
        new_text = re.search(r"[0-9]+", text)
        if new_text:
            return f"{arg_type} doit comporter uniquement du texte"

    @staticmethod
    def long_string_verif(arg_type, min_txt, max_txt, text) -> False:
        if len(text) < min_txt or len(text) > max_txt:
            return f"{arg_type} doit comporter entre {min_txt} et {max_txt} caractères"

    @staticmethod
    def clear_frame(frame: any) -> None:
        if frame:
            for widget in frame.winfo_children():
                widget.destroy()

    @staticmethod
    def create_error(errors_dict):
        ctrl_errors = []
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

    def listing_canvas(self, curent_frame):

        self.minsize(width=(self.view_x[0] + 100), height=(self.view_y[0] + 25))
        self.maxsize(width=(self.view_x[0] + 200), height=(self.view_y[0] + 25))

        canvas = Canvas(curent_frame)
        self.frame_list = Frame(canvas, bg="#ffffff", padx=10, pady=15)
        scrollbar = Scrollbar(curent_frame, orient="vertical", command=canvas.yview)

        canvas.configure(yscrollcommand=scrollbar.set, bg="#ffffff", width=self.view_x[0], height=self.view_y[0])
        canvas.create_window((0, 0), window=self.frame_list, anchor='nw')

        canvas.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky='ns')

        def mouse_move(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        return self.frame_list, canvas, mouse_move

