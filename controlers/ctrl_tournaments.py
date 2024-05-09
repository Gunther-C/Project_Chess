from tkinter import *
from tkinter import font, Entry
from tkinter import ttk
import time

from core import core
from database import data_tournament as data
from models import mdl_tournament as model
from views import view_tournaments as view


class TournamentsCtrl(core.Core):
    def __init__(self, data_transfer=None):
        super().__init__()

        self.vue = view.TournamentsViews(self)

        self.vue.new_menu()
        self.vue.menu_choice()


    def result_menu(self, result: str | None = None):
        match result:
            case 'create':
                self.vue.new_torunament()

            case 'search':
                self.vue.search_player()

            case _:
                pass







    def tournaments(self):

        if not self.widjets_menu2:
            self.menu_tournaments.add_command(label="Ajouter un tournoi", command=lambda: self.create())
            self.menu_tournaments.add_command(label="Chercher un tournoi",
                                              command=lambda: self.event_choice('search_player'))
            self.menu_tournaments.add_command(label="Liste de tous les tournois",
                                              command=lambda: self.event_choice('list_player'))
            self.widjets_menu2 = True

    def create(self):
        # vue création
        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self, bg="#FEF9E7")
        self.frame.grid()
        self.frame.place(relx=0.5, rely=0.4, anchor='center')

        data_player: dict = view.TournamentsViews(self.frame).new_player()

        submit = ttk.Button(self.frame, text="  Valider  ", command=lambda: create_control_result(data_player))
        submit.grid(columnspan=7)


window = TournamentsCtrl(None)
window.mainloop()
