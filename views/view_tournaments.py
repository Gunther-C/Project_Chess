from tkinter import *
from tkinter import ttk
from tkinter import font
from core import extend_view


class TournamentsViews(extend_view.ExtendViews):
    def __init__(self, new_self: any):

        self.se = new_self

        self.frame = Frame(self.se, bg="#FEF9E7", padx=15, pady=10)
        self.frame.grid()
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        super().__init__(self.frame)


    def new_menu(self):
        self.se.menu_players = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_choice())
        self.se.menu.add_cascade(label="Tournois", menu=self.se.menu_players)
        self.se.menu.add_command(label="Quitter", command=self.se.quit)
        self.se.config(menu=self.se.menu)

    def menu_choice(self):
        if not self.se.widjets_menu1:
            self.se.menu_listing = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_list())
            self.se.menu_players.add_command(label="Ajouter un tournoi", command=lambda: self.se.result_menu('create'))
            self.se.menu_players.add_command(label="Chercher un tournoi", command=lambda: self.se.result_menu('search'))
            self.se.menu_players.add_cascade(label="Liste des tournois par:", menu=self.se.menu_listing)
            self.se.widjets_menu1 = True

    def menu_list(self):
        if not self.se.widjets_menu2:
            self.se.menu_listing.add_command(label="Ordre alphabétique", command=lambda: self.se.recover_list('names'))
            self.se.menu_listing.add_command(label="Dates croissantes",
                                             command=lambda: self.se.recover_list('cr_date'))
            self.se.menu_listing.add_command(label="Dates décroissantes",
                                             command=lambda: self.se.recover_list('de_date'))
            self.se.widjets_menu2 = True



    def new_tournament(self):

        pass






    def message(self, **kwargs: any) -> any:
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(self.frame, bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        self.frame.after(10000, label.destroy)
