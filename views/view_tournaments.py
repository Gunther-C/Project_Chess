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

        self.se.maxsize(width=0, height=0)
        self.se.minsize(width=420, height=450)
        self.se.clear_frame(self.frame)
        self.frame.place(relx=0.5, rely=0.4, anchor='center')

        self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True, mst=self.frame,
                   bg="#FEF9E7", justify=None, text="Nouveau Tournoi : ", width=None, row=0, cols=None, colspan=7,
                   sticky=None, padx=None, pady=None)

        name = self.input_text(mst=self.frame, lb_row=2, ip_row=3, cols=1, colspan=6, bg="#FEF9E7", text="Nom : ",
                               ip_wh=20)
        address = self.input_text(mst=self.frame, lb_row=5, ip_row=6, cols=1, colspan=6, bg="#FEF9E7",
                                  text="Adresse : ", ip_wh=60)
        birth_start = self.input_date(mst=self.frame, lb_row=8, ip_row=9, bg="#FEF9E7", text="Date de début : ")

        self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=None,
                   justify=None, text="Type de tournoi", row=10, cols=1, colspan=6, sticky='w')

        number_round: tuple = ('Partie unique', 'Partie 3 manches', 'Tournoi 4 rounds', 'Tournoi 8 rounds')

        list_choice_round = ttk.Combobox(self.frame, values=number_round, state='readonly', background='#ffffff')
        list_choice_round.current(2)
        list_choice_round.grid(row=12, column=1, columnspan=6, sticky='w')


        def result(event):
            select_t = list_choice_round.get()
            print(select_t)

        list_choice_round.bind("<<ComboboxSelected>>", result)

        select_type = list_choice_round.get()
        match select_type:
            case 'Partie unique':
                select_type = 2
            case 'Partie 3 manches':
                select_type = 2
            case 'Tournoi 4 rounds':
                select_type = 16
            case 'Tournoi 8 rounds':
                select_type = 32
            case _:
                pass

        data_tour = {'name': name, 'address': address, 'birth_start': birth_start, 'tour_type': select_type}

        submit = ttk.Button(self.frame, text="Valider", command=lambda: self.se.tournament_ctrl(self.frame, data_tour))
        submit.grid(columnspan=7, pady=20, ipadx=5)

        space_x: list = self.adjust_x(address, name)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=(space_x[2] - 30), ipady=None,
                   justify=None, text="", row=9, cols=6, colspan=None, sticky=None)

        """self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=7, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=10, cols=6, colspan=None, sticky=None)"""

    def message(self, **kwargs: any) -> any:
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(self.frame, bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        self.frame.after(10000, label.destroy)
