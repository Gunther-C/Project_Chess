from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from core import extend_view


class TournamentsViews(extend_view.ExtendViews):
    def __init__(self, new_self):

        self.se = new_self

        self.frame = Frame(self.se, bg="#FEF9E7", padx=15, pady=10)
        self.frame.grid()
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.new_window = None
        self.new_frame = None

        self.tournament_players: list = []

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

        data_tournament: dict = {}
        data_player: list = []

        file_players = self.se.players_list()
        dt_player = sorted(file_players, key=lambda x: x['Nom'])

        # Récupérer uniquement identité, nom et prénom avec self.se.instance_player
        for plr in dt_player:
            instance_player: dict = {}
            for keys, values in plr.items():
                instance_player = self.se.instance_player(instance_player, keys, values)
            data_player.append(instance_player)

        self.se.clear_frame(self.frame)
        view_master = self.se.master_window(55, 70)
        self.se.minsize(width=int(view_master[0] * 0.70), height=int(view_master[1]))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        title = self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True,
                           mst=self.frame, bg="#FEF9E7", justify=None, text="Nouveau Tournoi : ", width=None, row=0,
                           cols=None, colspan=7, sticky=None, padx=None, pady=None)
        name = self.input_text(mst=self.frame, lb_row=2, ip_row=3, cols=1, colspan=6, bg="#FEF9E7", text="Nom : ",
                               ip_wh=20)
        address = self.input_text(mst=self.frame, lb_row=5, ip_row=6, cols=1, colspan=6, bg="#FEF9E7",
                                  text="Adresse : ", ip_wh=60)
        birth_start = self.input_date(mst=self.frame, lb_row=8, ip_row=9, bg="#FEF9E7", text="Date de début : ")

        number_turns = self.input_text(mst=self.frame, lb_row=11, ip_row=12, cols=1, colspan=6, bg="#FEF9E7",
                                       text="Choisissez un nombre de tour", ip_wh=10)
        number_turns.insert(0, '4')

        self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=None,
                   justify=None, text="Sélection des joueurs", row=14, cols=1, colspan=6, sticky='w')

        plr_create = ttk.Button(self.frame, text="Créer", command=lambda: new_player())
        plr_create.grid(row=15, column=1, columnspan=3, pady=5)

        plr_list = ttk.Button(self.frame, text="Rechercher", command=lambda: list_player())
        plr_list.grid(row=15, column=4, columnspan=3, pady=5)

        data_tournament['name'] = name
        data_tournament['address'] = address
        data_tournament['birth_start'] = birth_start
        data_tournament['numberRound'] = number_turns
        data_tournament['players'] = []

        def on_click(submit_type):
            if submit_type == 'list':
                data_tournament['players'] = [data_player[x] for x, select in enumerate(select_players) if select.get()]

            if len(self.se.new_all_players) > 0:
                for nw_player in self.se.new_all_players:
                    data_tournament['players'].insert(0, nw_player)

            print(data_tournament['players'])

            self.new_window[0].destroy()

            ctrl_name = self.se.search_name_widget(self.frame, 'selectPlayers')
            if not ctrl_name and len(data_tournament['players']) > 0:
                submit = ttk.Button(self.frame, text="Valider", name='selectPlayers',
                                    command=lambda: self.se.tournament_ctrl(self.frame, data_tournament))
                submit.grid(columnspan=7, pady=30, ipadx=5)

        select_players = [BooleanVar() for _ in data_player]

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

        def list_player():
            self.new_window = self.se.listing_window(45, 70, 'Liste des joueurs', '#FEF9E7')
            master_geometrie = self.new_window[1], self.new_window[2]

            self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
            self.new_frame.grid()
            self.new_frame.place(relx=0.5, rely=0, anchor='n')

            list_system = self.se.listing_canvas(self.new_frame, '#ffffff', master_geometrie)
            frame = list_system[0]
            canvas = list_system[1]
            scroll_mouse = list_system[2]
            view_x = list_system[3]
            view_y = list_system[4]

            # Titre
            self.title(family=None, size=15, weight="bold", slant="roman", underline=True, mst=frame, bg="#ffffff",
                       justify="center", text="Sélection des joueurs", width=None, child_w=0, row=0, cols=None,
                       colspan=8, sticky="n", padx=None, pady=20)

            # En tète listing
            for infos_type in data_player:
                title_cols = 0
                for title_list in infos_type:
                    self.title(family=None, size=10, weight="bold", slant="roman", underline=False, mst=frame,
                               bg="#ffffff", justify="center", text=title_list, width=None, child_w=300, row=1,
                               cols=title_cols, colspan=None, sticky=None, padx=15, pady=5)
                    title_cols += 1
                break

            next_line = 2
            if len(self.se.new_all_players) > 0:
                for nw_player in self.se.new_all_players:
                    value_cols = 0
                    for key in nw_player:
                        self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                                   justify="center", text=nw_player[key], row=next_line, cols=value_cols, colspan=None,
                                   sticky=None)
                        value_cols += 1

                    check = self.check_button(mst=frame, variable=None, onvalue=1, offvalue=0,
                                              bg="#ffffff", justify=None, indicatoron=True, selectcolor=None,
                                              state="disabled", cols=value_cols, row=next_line, sticky=None)
                    check.select()
                    next_line += 1

                label = Label(frame, bg="#ffffff", height=1, underline=1)
                label.grid(row=next_line, columnspan=8, sticky="w")
                next_line += 1

            for i, infos_player in enumerate(data_player):
                value_cols = 0
                for ks in infos_player:
                    self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                               justify="center", text=infos_player[ks], row=next_line, cols=value_cols, colspan=None,
                               sticky=None)
                    value_cols += 1

                self.check_button(mst=frame, variable=select_players[i], onvalue=1, offvalue=0,
                                  bg="#ffffff", justify=None, indicatoron=True, selectcolor=None,
                                  state="normal", cols=value_cols, row=next_line, sticky=None)
                next_line += 1

            submit_list = ttk.Button(frame, text="Valider", command=lambda: on_click('list'))
            submit_list.grid(columnspan=7, pady=20, ipadx=5)

            frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox("all"), width=(view_x - 100),
                                                       height=(view_y - 55)))
            canvas.bind_all("<MouseWheel>", scroll_mouse)
            frame.place(relx=0.5, rely=0.1, anchor='n')

        def new_player():
            self.new_window = self.se.listing_window(30, 50, 'Ajouter un joueur', '#FEF9E7')
            master_geometrie = self.new_window[1], self.new_window[2]

            self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
            self.new_frame.grid()
            self.new_frame.place(relx=0.5, rely=0.4, anchor='center')

            plr_title = self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True,
                                   mst=self.new_frame, bg="#FEF9E7", justify=None, text="Nouveau joueur : ", width=None,
                                   row=0, cols=None, colspan=7, sticky=None, padx=None, pady=None)

            identity = self.input_text(mst=self.new_frame, lb_row=2, ip_row=3, cols=1, colspan=5, bg="#FEF9E7",
                                       text="Identifiant : ", ip_wh=20)
            last_name = self.input_text(mst=self.new_frame, lb_row=5, ip_row=6, cols=1, colspan=5, bg="#FEF9E7",
                                        text="Nom : ", ip_wh=20)
            first_name = self.input_text(mst=self.new_frame, lb_row=8, ip_row=9, cols=1, colspan=5, bg="#FEF9E7",
                                         text="Prénom : ", ip_wh=20)

            plr_data = {'identity': identity, 'last_name': last_name, 'first_name': first_name}

            submit_players = ttk.Button(self.new_frame, text="  Valider  ", command=lambda: lbd())
            submit_players.grid(columnspan=7, pady=20)

            def lbd():
                ctrl_result = self.se.tournament_ctrl_player(self.new_frame, plr_data)
                if ctrl_result:
                    infos_plr = {'Identité': ctrl_result[0], 'Nom': ctrl_result[1], 'Prénom': ctrl_result[2]}
                    self.se.new_all_players.append(infos_plr)
                    on_click('player')

            space_x: list = self.adjust_x(plr_title, last_name)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=1, cols=0, colspan=None, sticky=None)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=4, cols=0, colspan=None, sticky=None)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=7, cols=0, colspan=None, sticky=None)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=10, cols=6, colspan=None, sticky=None)

    def detail_tournament(self, data_player: dict):

        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(70, 70)
        list_system = self.se.listing_canvas(self.frame, '#ffffff', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        scroll_mouse = list_system[2]
        view_x = list_system[3]
        view_y = list_system[4]
        self.se.minsize(width=view_x, height=view_y)
        self.frame.place(relx=0.5, rely=0, anchor='n')

        self.title(family=None, size=15, weight="bold", slant="roman", underline=True, mst=frame, bg="#ffffff",
                   justify="center", text=data_player['Nom'], width=None, row=0, cols=None, colspan=8, sticky="n",
                   padx=None, pady=20)

        self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                   justify="center", text=data_player['Adresse'], row=1, cols=1, colspan=7,
                   sticky=None)

        self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                   justify="center", text=data_player['Date'], row=2, cols=1, colspan=7,
                   sticky=None)

        self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                   justify="center", text=f"Nombre(s) de tour(s){data_player['number_turns']}", row=3, cols=1, colspan=7,
                   sticky=None)

        for player in data_player['Joueurs']:
            title_cols = 0
            for keys, values in player.items():
                if not keys == 'id':
                    self.title(family=None, size=10, weight="bold", slant="roman", underline=False, mst=frame,
                               bg="#ffffff", justify="center", text=keys, width=None, child_w=300, row=4,
                               cols=title_cols, colspan=None, sticky=None, padx=15, pady=5)
                    title_cols += 1
            break

        next_line = 5
        for player in data_player['Joueurs']:
            value_cols = 0
            for keys, values in player.items():
                if not keys == 'id':
                    self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                               justify="center", text=values, row=next_line, cols=value_cols, colspan=None,
                               sticky=None)
                    value_cols += 1
            next_line += 1

        frame.update()
        frame.bind("<Configure>",
                   canvas.configure(scrollregion=canvas.bbox("all"), width=(view_x - 100), height=(view_y - 25)))
        canvas.bind_all("<MouseWheel>", scroll_mouse)





    def message(self, **kwargs: any) -> any:
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(kwargs['mst'], bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        kwargs['mst'].after(10000, label.destroy)
