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

        # self.schema_round()

        """font_families = font.families()
        for family in font_families:
            print(family)"""
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
            self.se.menu_listing.add_command(label="Dates croissantes",
                                             command=lambda: self.se.tournament_lists('first'))
            self.se.menu_listing.add_command(label="Dates décroissantes",
                                             command=lambda: self.se.tournament_lists('last'))
            self.se.widjets_menu2 = True

    def new_tournament(self):
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(55, 70)
        self.se.minsize(width=int(master_geometrie[0] * 0.70), height=int(master_geometrie[1]))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

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

        select_players = [BooleanVar() for _ in data_player]

        def tournament_submit(dt_tournament):
            if len(self.se.new_all_players) > 0:
                for nw_player in self.se.new_all_players:
                    data_tournament['players'].insert(0, nw_player)

            self.new_window[0].destroy()
            self.se.tournament_ctrl(self.frame, dt_tournament)

        def unity_player_submit(plr_data):
            ctrl_result = self.se.tournament_ctrl_player(self.new_frame, plr_data)
            if ctrl_result:
                infos_plr = {'Identité': ctrl_result[0], 'Nom': ctrl_result[1], 'Prénom': ctrl_result[2]}
                self.se.new_all_players.append(infos_plr)
                all_player_submit('player')

        def all_player_submit(submit_type):
            if submit_type == 'list':
                data_tournament['players'] = [data_player[x] for x, select in enumerate(select_players) if select.get()]

            self.new_window[0].destroy()
            ctrl_name = self.se.search_name_widget(self.frame, 'selectPlayers')

            if not ctrl_name:
                if len(self.se.new_all_players) > 0 or len(data_tournament['players']) > 0:
                    submit = ttk.Button(self.frame, text="Valider", name='selectPlayers',
                                        command=lambda: tournament_submit(data_tournament))
                    submit.grid(columnspan=7, pady=30, ipadx=5)

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

        plr_list = ttk.Button(self.frame, text="Rechercher", command=lambda: new_list())
        plr_list.grid(row=15, column=4, columnspan=3, pady=5)

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

        data_tournament['name'] = name
        data_tournament['address'] = address
        data_tournament['birth_start'] = birth_start
        data_tournament['numberRound'] = number_turns
        data_tournament['players'] = []

        def new_list():
            view_list = self.list_players(data_player, select_players, 'Sélection des joueurs')
            self.new_window = view_list[0]

            submit_list = ttk.Button(view_list[1], text="Valider", command=lambda: all_player_submit('list'))
            submit_list.grid(column=1, columnspan=7, pady=20, ipadx=5)

        def new_player():
            if self.new_window:
                self.new_window[0].destroy()
            self.new_window = self.se.listing_window(30, 50, 40, 40, 'Ajouter un joueur', '#FEF9E7')

            self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
            self.new_frame.grid()
            self.new_frame.place(relx=0.5, rely=0.4, anchor='center')

            plr_title = self.title(family="Lucida Calligraphy", size=30, weight="bold", slant="italic", underline=True,
                                   mst=self.new_frame, bg="#FEF9E7", justify=None, text="Nouveau joueur : ", width=None,
                                   row=0, cols=None, colspan=7, sticky=None, padx=None, pady=None)

            identity = self.input_text(mst=self.new_frame, lb_row=2, ip_row=3, cols=1, colspan=5, bg="#FEF9E7",
                                       text="Identifiant : ", ip_wh=20)
            last_name = self.input_text(mst=self.new_frame, lb_row=5, ip_row=6, cols=1, colspan=5, bg="#FEF9E7",
                                        text="Nom : ", ip_wh=20)
            first_name = self.input_text(mst=self.new_frame, lb_row=8, ip_row=9, cols=1, colspan=5, bg="#FEF9E7",
                                         text="Prénom : ", ip_wh=20)

            plr_data = {'identity': identity, 'last_name': last_name, 'first_name': first_name}

            submit_players = ttk.Button(self.new_frame, text="  Valider  ",
                                        command=lambda: unity_player_submit(plr_data))
            submit_players.grid(columnspan=7, pady=20)

            space_x: list = self.adjust_x(plr_title, last_name)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=1, cols=0, colspan=None, sticky=None)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=4, cols=0, colspan=None, sticky=None)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=7, cols=0, colspan=None, sticky=None)
            self.label(mst=self.new_frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                       justify=None, text="", row=10, cols=6, colspan=None, sticky=None)

    def list_tournament(self, title: str, data_tournament: list):

        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(70, 70)
        self.se.minsize(width=master_geometrie[0], height=master_geometrie[1])
        self.frame.place(relx=0.5, rely=0.1, anchor='n')

        self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True, mst=self.frame,
                   bg="#FEF9E7", justify=None, text=title, width=None, row=0, cols=None, colspan=2, sticky=None,
                   padx=None, pady=15)

        cols_x = int(master_geometrie[0] - 100) // 7
        content_y = int(master_geometrie[1] / 3) // 12

        """data_tournament = []
        for x in range(10):
            for tournament in data_tour:
                data_tournament.append(tournament)"""

        columns: tuple = ()
        for keys in data_tournament[0]:
            columns = columns + (keys,)

        content = ttk.Treeview(self.frame, columns=columns, show='headings', padding=20, height=content_y)
        content.tag_configure('highlight', background='lightblue')

        for keys in data_tournament[0]:
            content.column(keys, width=cols_x, anchor="center")
            content.heading(keys, text=keys)

        for tournament in data_tournament:
            list_tour = []
            for keys, values in tournament.items():
                if keys == 'Joueurs':
                    values = len(values)
                if keys == 'Rounds':
                    values = len(values)
                list_tour.append(values)
            content.insert('', END, values=list_tour)

        def selected(event):
            result = None
            for selected_item in content.selection():
                result = content.item(selected_item)['values']

            if result:
                rst_rounds = None
                rst_players = None
                for tour in data_tournament:
                    for kys in tour:
                        if kys == 'id' and tour[kys] == result[0]:
                            rst_rounds = tour['Rounds']
                            rst_players = tour['Joueurs']
                if rst_rounds and rst_players:
                    self.se.tournament_treatment('data', self.frame, result[0], result[1], result[2], result[3],
                                                 result[4], rst_rounds, rst_players)

        def hover(event):
            tree = event.widget
            item = tree.identify_row(event.y)
            tree.tk.call(tree, "tag", "remove", "highlight")
            tree.tk.call(tree, "tag", "add", "highlight", item)

        content.bind("<Motion>", hover)
        content.bind('<<TreeviewSelect>>', selected)
        content.grid(row=1, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=content.yview)
        content.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

    def detail_tournament(self, tournament: object):

        if len(self.se.new_all_players) > 0:
            self.se.new_all_players.clear()

        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(50, 60)
        self.se.minsize(width=(master_geometrie[0] - 100), height=(master_geometrie[1] - 100))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True, mst=self.frame,
                   bg="#FEF9E7", justify="center", text=tournament.name, width=None, row=0, cols=1, colspan=3,
                   sticky=None, padx=None, pady=30)

        self.title(family="Times New Roman", size=14, weight="bold", slant="roman", underline=False, mst=self.frame,
                   bg="#FEF9E7", justify=None, text=f"Le : {tournament.date}", width=None, row=1, cols=1,
                   colspan=3, sticky="w", padx=None, pady=10)

        self.title(family="Times New Roman", size=14, weight="bold", slant="roman", underline=False, mst=self.frame,
                   bg="#FEF9E7", justify=None, text=f"A : {tournament.address}", width=None, row=2, cols=1,
                   colspan=3, sticky="w", padx=None, pady=10)

        self.title(family="Times New Roman", size=14, weight="bold", slant="roman", underline=False, mst=self.frame,
                   bg="#FEF9E7", justify=None, text=f"En : {tournament.number_turns} manche(s)", width=None, row=3,
                   cols=1, colspan=3, sticky="w", padx=None, pady=10)

        self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=10, justify=None, text="",
                   row=4, cols=0, colspan=None, sticky=None)

        plr_create = ttk.Button(self.frame, text="Liste des joueurs", command=lambda: players_list())
        plr_create.grid(row=5, column=1,  ipadx=20, ipady=5)

        self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=20, ipady=None, justify=None, text="",
                   row=5, cols=2, colspan=None, sticky=None)

        plr_list = ttk.Button(self.frame, text="Liste des tours",
                              command=lambda: round_list())
        plr_list.grid(row=5, column=3, ipadx=20, ipady=5)

        plr_list = ttk.Button(self.frame, text="<= Lancer le tour =>", command=lambda: round_start())
        plr_list.grid(row=6, columnspan=4, pady=40, ipadx=30, ipady=10)

        def players_list():
            view_list = self.list_players(tournament.players, None, 'Liste des joueurs')
            self.new_window = view_list[0]

            submit_list = ttk.Button(view_list[1], text="Fermer", command=lambda: self.new_window[0].destroy())
            submit_list.grid(column=1, columnspan=7, pady=20, ipadx=5)

        def round_start():
            last_round = tournament.rounds[-1]
            if len(last_round['start']) < 1:
                last_round['start'] = self.se.update_date(('start', tournament.id_tour))

            new_round = self.se.round_instance(last_round)
            self.schema_round(tournament.id_tour, new_round)

        def round_list():
            rounds = self.se.round_instance(tournament.rounds)
            self.list_rounds(tournament.id_tour, rounds)


    def schema_round(self, tournament_id: object, new_round: object):

        """modif_round = False
        last_round_id = tournament.rounds[-1]
        last_round_id = last_round_id['round']
        if last_round_id == new_round['round']:
            modif_round = True"""

        # tournament_id = tournament.id_tour

        if self.new_window:
            self.new_window[0].destroy()

        self.new_window = self.se.listing_window(60, 90, 300, 30, f'Tour n° {new_round.id_round}', '#FEF9E7')

        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0, anchor='n')

        if not new_round.finish:
            new_round.finish = 'En cours'

        name = self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True,
                          mst=self.new_frame, bg="#FEF9E7", justify=None, text=f"Tour n° {new_round.id_round}",
                          width=None, row=0, cols=0, colspan=2, sticky="w", padx=20, pady=15)

        start = self.title(family="Times New Roman", size=14, weight="bold", slant="roman", underline=False,
                           mst=self.new_frame, bg="#FEF9E7", justify=None,
                           text=f"Ouverture du tournoi le : {new_round.start}", width=None, row=1, cols=0, colspan=2,
                           sticky="w", padx=20, pady=5)

        finish = self.title(family="Times New Roman", size=14, weight="bold", slant="roman", underline=False,
                            mst=self.new_frame, bg="#FEF9E7", justify=None, text=f"Tournoi terminé le : {new_round.finish}",
                            width=None, row=2, cols=0, colspan=2, sticky="w", padx=20, pady=5)

        name.update()
        start.update()
        finish.update()
        head_y = int(name.winfo_height() + start.winfo_height() + finish.winfo_height()) * 2
        master_geometrie = self.new_window[1], int(self.new_window[2] - head_y)

        list_system = self.se.listing_canvas(self.new_frame, 3, '#ffffff', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        scroll_mouse = list_system[2]
        view_x = list_system[3]
        view_y = list_system[4]

        lb_font = font.Font(family='Times New Roman', size=15)
        next_line = 0
        number_key = 0

        def action(winner, loser, parent):
            if new_round.start and not new_round.finish:
                match_key = parent.winfo_name()

                if not loser:
                    extract = winner.find('-')
                    id_player1 = winner[:extract]
                    id_player2 = winner[extract + 1:]
                    results = [(id_player1, 0.5), (id_player2, 0.5)]
                else:
                    id_player1 = winner[0]
                    id_player2 = loser[0]
                    results = [(id_player1, 1), (id_player2, 0)]

                for child in parent.winfo_children():
                    id_name = child.winfo_name()
                    id_n = id_name.find('id-')
                    identity = id_name[id_n + 3:]
                    if identity == id_player1:
                        child.configure(foreground='green')
                    if identity == id_player2:
                        child.configure(foreground='red')
                    if id_name == 'score':
                        child['text'] = winner[1]
                        if not loser:
                            child['text'] = 'Match null'
                            if identity == id_player1 or identity == id_player2:
                                child.configure(foreground='red')

                if winner:
                    data_match = (tournament_id, match_key, results)
                    self.se.update_score(data_match)
            else:
                pass

        def player_1(player1, player2, parent, color):
            plr1_widget = Label(match_frame, width=15, bg="#ffffff", highlightbackground="black", highlightthickness=1,
                                font=lb_font, foreground=color, text=player1.name_plr1,
                                name=f"id-{player1.identity_plr1}")
            plr1_widget.bind("<Button-1>", lambda e: action(player1, player2, parent))
            plr1_widget.grid(row=0, padx=10)

        def player_2(player2, player1, parent,color):
            plr2_widget = Label(match_frame, width=15, bg="#ffffff", highlightbackground="black", highlightthickness=1,
                                font=lb_font, foreground=color, text=player2.name_plr2,
                                name=f"id-{player2.identity_plr2}")
            plr2_widget.bind("<Button-1>", lambda e: action(player2, player1, parent))
            plr2_widget.grid(row=2, padx=10)




###############################################################






        for player in new_round['matchs']:

            result_match = 'En cours'
            foreground1 = 'black'
            foreground2 = 'black'

            if len(player[0]) > 2:

                if float(player[0][2]) > float(player[1][2]):
                    result_match = player[0][1]
                    foreground1 = 'green'
                    foreground2 = 'red'

                elif float(player[0][2]) < float(player[1][2]):
                    result_match = player[1][1]
                    foreground1 = 'red'
                    foreground2 = 'green'

                elif float(player[0][2]) == 0.5 and float(player[1][2]) == 0.5:
                    result_match = 'Match null'
                    foreground1 = 'blue'
                    foreground2 = 'blue'

                else:
                    result_match = 'Annulé'

            elif not new_round.start:
                result_match = 'non lancé'

            match_frame = Frame(frame, name=str(number_key), highlightbackground="black", highlightthickness=1,
                                bg="#f5cb8e", pady=30)
            match_frame.grid(row=next_line, column=1)

            player_1(player[0], player[1], match_frame, foreground1)

            espace = Label(match_frame, width=5, bg="#f5cb8e")
            espace.grid(row=1, column=1)

            result = Label(match_frame, width=15, bg="#ffffff", highlightbackground="black", highlightthickness=1,
                           font=lb_font, text=result_match, name="score")
            result.grid(row=1, column=2, padx=10)

            player_2(player[1], player[0], match_frame, foreground2)

            next_line += 1

            espace_ext = Label(frame)
            espace_ext.grid(row=next_line, column=1)

            next_line += 1
            number_key += 1

        canvas.update()
        canvas.create_window((0, 0), window=frame)
        frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox("all"), width=(view_x - 80), height=view_y))
        canvas.bind_all("<MouseWheel>", scroll_mouse)

        frame.update()
        col0_x = self.adjust_x(canvas, frame)
        col0 = Label(frame, bg="#ffffff")
        col0.grid(row=0, column=0, ipadx=col0_x[2])

        submit_list = ttk.Button(self.new_frame, text=f"Valider le tour n° {new_round['round']}",
                                 command=lambda: self.new_window[0].destroy())
        submit_list.grid(column=0, columnspan=2, pady=20, ipadx=5)

    def list_players(self, data_player, select_players, title):
        if self.new_window:
            self.new_window[0].destroy()
        self.new_window = self.se.listing_window(40, 60, 30, 30, 'Liste des joueurs', '#FEF9E7')
        master_geometrie = self.new_window[1], self.new_window[2]

        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0, anchor='n')

        list_system = self.se.listing_canvas(self.new_frame, 0, '#ffffff', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        scroll_mouse = list_system[2]
        view_x = list_system[3]
        view_y = list_system[4]

        self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True, mst=frame,
                   bg="#ffffff", justify="center", text=title, width=None, row=0, cols=1, colspan=7, sticky="n",
                   padx=None, pady=20)

        # En tète listing
        title_cols = 1
        if not select_players:
            label = Label(frame, bg="#ffffff", height=1, underline=1)
            label.grid(row=1, column=title_cols, padx=40)
            title_cols += 1

        for title_list in data_player[0]:
            self.title(family="Times New Roman", size=12, weight="bold", slant="roman", underline=False, mst=frame,
                       bg="#ffffff", justify="center", text=title_list, width=None, row=1,
                       cols=title_cols, colspan=None, sticky=None, padx=None, pady=5)
            title_cols += 1

            label = Label(frame, bg="#ffffff", height=1, underline=1)
            label.grid(row=1, column=title_cols, padx=40)
            title_cols += 1

        next_line = 2
        if len(self.se.new_all_players) > 0:
            for nw_player in self.se.new_all_players:
                value_cols = 1

                for key in nw_player:
                    self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                               justify="center", text=nw_player[key], row=next_line, cols=value_cols, colspan=None,
                               sticky=None)
                    value_cols += 1

                    label = Label(frame, bg="#ffffff", height=1, underline=1)
                    label.grid(row=next_line, column=value_cols, padx=40)
                    value_cols += 1

                if select_players:
                    check = self.check_button(mst=frame, variable=None, onvalue=1, offvalue=0,
                                              bg="#ffffff", justify=None, indicatoron=True, selectcolor=None,
                                              state="disabled", cols=value_cols, row=next_line, sticky=None)
                    check.select()
                next_line += 1

            label = Label(frame, bg="#ffffff", height=1, underline=1)
            label.grid(row=next_line, columnspan=6, sticky="w")
            next_line += 1

        for i, infos_player in enumerate(data_player):
            value_cols = 1

            if not select_players:
                label = Label(frame, bg="#ffffff", height=1, underline=1)
                label.grid(row=next_line, column=value_cols, padx=40)
                value_cols += 1

            for ks in infos_player:
                self.label(mst=frame, width=None, height=None, bg="#ffffff", ipadx=None, ipady=None,
                           justify="center", text=infos_player[ks], row=next_line, cols=value_cols, colspan=None,
                           sticky=None)
                value_cols += 1

                label = Label(frame, bg="#ffffff", height=1, underline=1)
                label.grid(row=next_line, column=value_cols, padx=40)
                value_cols += 1

            if select_players:
                self.check_button(mst=frame, variable=select_players[i], onvalue=1, offvalue=0,
                                  bg="#ffffff", justify=None, indicatoron=True, selectcolor=None,
                                  state="normal", cols=value_cols, row=next_line, sticky=None)
            next_line += 1

        canvas.update()
        canvas.create_window((0, 0), window=frame)
        frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox("all"), width=view_x, height=view_y))
        canvas.bind_all("<MouseWheel>", scroll_mouse)

        frame.update()
        col0_x = self.adjust_x(canvas, frame)
        col0 = Label(frame, bg="#ffffff")
        col0.grid(row=0, column=0, ipadx=col0_x[2])

        return self.new_window, frame

    def list_rounds(self, tournament_id: object,  data_rounds: list):
        if self.new_window:
            self.new_window[0].destroy()
        self.new_window = self.se.listing_window(50, 50, 30, 40, 'Liste des tours', '#FEF9E7')
        master_geometrie = self.new_window[1], self.new_window[2]

        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0, anchor='n')

        self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True,
                   mst=self.new_frame, bg="#FEF9E7", justify=None, text="Liste des tours", width=None, row=0,
                   cols=None, colspan=2, sticky=None, padx=None, pady=15)

        cols_x = int(master_geometrie[0] - 100) // 4
        content_y = int(master_geometrie[1] / 3) // 12

        for rd in data_rounds:
            if rd.start and not rd.finish:
                rd.finish = 'En cours'

            elif not rd.finish:
                rd.finish = 'En attente de lancement'

            if not rd.start:
                rd.start = 'En attente de lancement'
            count_matchs = len(rd.matchs_list)
            rd.matchs_list = str(count_matchs)

        columns: tuple = (1, 2, 3, 4)
        header: tuple = ("Numéro", "Date d'ouverture", "Date de fin", "Nombre de match")

        content = ttk.Treeview(self.new_frame, columns=columns, show='headings', padding=20, height=content_y)
        content.tag_configure('highlight', background='lightblue')

        for x, head in enumerate(header):
            content.column(columns[x], width=cols_x, anchor="center")
            content.heading(columns[x], text=head)

        for rd in data_rounds:
            list_matchs = [rd.id_round, rd.start, rd.finish, rd.matchs_list]
            content.insert('', END, values=list_matchs)

        def selected(event):
            result = None
            for selected_item in content.selection():
                result = content.item(selected_item)['values']

            if result:
                found = False
                number = 0
                for _round in data_rounds:
                    if _round.id_round == result[0]:
                        found = True
                        break

                    number += 1

                if found:
                    new_round = self.se.round_instance(data_rounds[number])
                    self.schema_round(tournament_id, new_round)

        def hover(event):
            tree = event.widget
            item = tree.identify_row(event.y)
            tree.tk.call(tree, "tag", "remove", "highlight")
            tree.tk.call(tree, "tag", "add", "highlight", item)

        content.bind("<Motion>", hover)
        content.bind('<<TreeviewSelect>>', selected)
        content.grid(row=1, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self.new_frame, orient="vertical", command=content.yview)
        content.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

    def message(self, **kwargs: any) -> any:
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(kwargs['mst'], bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        kwargs['mst'].after(10000, label.destroy)

