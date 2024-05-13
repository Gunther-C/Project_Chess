from tkinter import *
from tkinter import ttk
from tkinter import font
from core import extend_view


class TournamentsViews(extend_view.ExtendViews):
    def __init__(self, new_self):

        self.se = new_self

        self.frame = Frame(self.se, bg="#FEF9E7", padx=15, pady=10)
        self.frame.grid()
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.new_window = None
        self.new_frame = None
        super().__init__(self.frame)

    def new_menu(self):
        self.se.menu_tour = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_choice())
        self.se.menu.add_cascade(label="Tournois", menu=self.se.menu_tour)
        self.se.menu.add_command(label="Quitter", command=self.se.destroy)
        self.se.config(menu=self.se.menu)

    def menu_choice(self):
        if not self.se.widjets_menu1:
            self.se.menu_listing = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_list())
            self.se.menu_tour.add_command(label="Ajouter un tournoi", command=lambda: self.se.result_menu('create'))
            self.se.menu_tour.add_command(label="Chercher un tournoi", command=lambda: self.se.result_menu('search'))
            self.se.menu_tour.add_cascade(label="Liste des tournois par:", menu=self.se.menu_listing)
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

        def choice(event):
            return result
        self.se.clear_frame(self.frame)
        self.se.master_window(50, 60)
        self.se.minsize(width=420, height=450)
        self.frame.place(relx=0.5, rely=0.4, anchor='center')

        title = self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True, mst=self.frame,
                   bg="#FEF9E7", justify=None, text="Nouveau Tournoi : ", width=None, row=0, cols=None, colspan=7,
                   sticky=None, padx=None, pady=None)

        name = self.input_text(mst=self.frame, lb_row=2, ip_row=3, cols=1, colspan=6, bg="#FEF9E7", text="Nom : ",
                               ip_wh=20)
        address = self.input_text(mst=self.frame, lb_row=5, ip_row=6, cols=1, colspan=6, bg="#FEF9E7",
                                  text="Adresse : ", ip_wh=60)
        birth_start = self.input_date(mst=self.frame, lb_row=8, ip_row=9, bg="#FEF9E7", text="Date de début : ")

        round_type = self.input_text(mst=self.frame, lb_row=11, ip_row=12, cols=1, colspan=6, bg="#FEF9E7",
                                     text="Choisissez un nombre de tour", ip_wh=10)

        # if not self.se.new_player:
        self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=None,
                   justify=None, text="Sélection des joueurs", row=14, cols=1, colspan=6, sticky='w')

        plr_create = ttk.Button(self.frame, text="Créer",
                                command=lambda: self.se.tournament_ctrl(self.frame, data_tour))
        plr_create.grid(row=15, column=1, columnspan=3, pady=5)

        plr_list = ttk.Button(self.frame, text="Rechercher",
                              command=lambda: self.se.tournament_ctrl(self.frame, {'listing': 'listing'}))
        plr_list.grid(row=15, column=4, columnspan=3, pady=5)

        data_tour = {'name': name, 'address': address, 'birth_start': birth_start, 'tour_type': round_type}
        submit = ttk.Button(self.frame, text="Valider", command=lambda: self.se.tournament_ctrl(self.frame, data_tour))
        submit.grid(columnspan=7, pady=20, ipadx=5)

        title.update()
        address.update()
        name.update()
        space_x_date: list = self.adjust_x(address, name)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=(space_x_date[2]), ipady=None,
                   justify=None, text="", row=9, cols=6, colspan=None, sticky=None)
        space_xx: list = self.adjust_x(address, title)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=(space_xx[2]), ipady=None,
                   justify=None, text="", row=0, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=None, ipady=None,
                   justify=None, text="", row=4, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=None, ipady=None,
                   justify=None, text="", row=7, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=None, ipady=None,
                   justify=None, text="", row=10, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=None, ipady=None,
                   justify=None, text="", row=13, cols=0, colspan=None, sticky=None)


    def list_player(self, title: str, data_player: list):

        self.new_window = self.se.listing_window()

        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0, anchor='n')

        master_geometrie = self.new_window[1], self.new_window[2]
        list_system = self.se.listing_canvas(self.new_frame, '#ffffff', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        scroll_mouse = list_system[2]
        view_x = list_system[3]
        view_y = list_system[4]


        self.title(family=None, size=15, weight="bold", slant="roman", underline=True, mst=frame, bg="#ffffff",
                   justify="center", text=title, width=None, child_w=0, row=0, cols=None, colspan=8, sticky="n",
                   padx=None, pady=20)

        for player in data_player:
            title_cols = 0
            for keys, values in player.items():
                if not keys == 'id':
                    self.title(family=None, size=10, weight="bold", slant="roman", underline=False, mst=frame,
                               bg="#ffffff", justify="center", text=keys, width=None, child_w=300, row=1,
                               cols=title_cols, colspan=None, sticky=None, padx=15, pady=5)
                    title_cols += 1
            break

        next_line = 2
        for player in data_player:
            value_cols = 0
            for keys, values in player.items():
                if not keys == 'id':
                    self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                               justify="center", text=values, row=next_line, cols=value_cols, colspan=None, sticky=None)
                    value_cols += 1
            next_line += 1

        frame.update()
        frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox("all"), width=(view_x - 100), height=(view_y - 25)))
        canvas.bind_all("<MouseWheel>", scroll_mouse)

    def message(self, **kwargs: any) -> any:
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(self.frame, bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        self.frame.after(10000, label.destroy)
