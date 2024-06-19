from tkinter import ttk, font, Menu, Frame, Label, Checkbutton, BooleanVar, messagebox, END, INSERT
from tkinter.scrolledtext import ScrolledText

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

        """font_families = font.families()
        for family in font_families:
            print(family)"""

    def new_menu(self):
        """
        :return: Menu Tournoi
        """
        self.se.menu_param = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_parameter())
        self.se.menu_tour = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_choice())
        self.se.menu.add_cascade(label="Menu Tournois", menu=self.se.menu_tour)
        self.se.menu.add_cascade(label="Options", menu=self.se.menu_param)
        self.se.config(menu=self.se.menu)

    def menu_parameter(self):
        """
        :return: Menu principale, fermer l'application
        """
        if not self.se.widjets_menu4:
            def w_master():
                self.se.destroy()
                self.se.windows_master()

            self.se.menu_param.add_command(label="Menu principal", command=lambda: w_master())
            self.se.menu_param.add_command(label="Quitter", command=self.se.destroy)
            self.se.widjets_menu4 = True

    def menu_choice(self):
        """
        :return: Menu secondaire
        """
        if not self.se.widjets_menu1:
            self.se.menu_listing = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_list())
            self.se.menu_tour.add_command(label="Ajouter un tournoi", command=lambda: self.new_tournament())
            self.se.menu_tour.add_cascade(label="Liste des tournois par:", menu=self.se.menu_listing)
            self.se.widjets_menu1 = True

    def menu_list(self):
        """
        :return: Menu du style de listes des tournois
        """
        if not self.se.widjets_menu2:
            self.se.menu_listing.add_command(label="Dates croissantes",
                                             command=lambda: self.se.tournament_lists('first', self.frame))
            self.se.menu_listing.add_command(label="Dates décroissantes",
                                             command=lambda: self.se.tournament_lists('last', self.frame))
            self.se.widjets_menu2 = True

    def new_tournament(self):
        """
        :return: Vue création nouveau tournoi
        """
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(55, 70)
        self.se.minsize(width=int(master_geometrie[0] * 0.70), height=int(master_geometrie[1]))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        data_tournament: dict = {}
        data_player = []
        new_list_players = self.se.instance_player()

        if new_list_players:
            data_player = new_list_players

        select_players = [BooleanVar() for _ in data_player]

        def tournament_submit(dt_tournament):

            if len(self.se.new_all_players) > 0:
                for nw_player in self.se.new_all_players:
                    if nw_player not in dt_tournament['players']:
                        dt_tournament['players'].insert(0, nw_player)

            self.new_window[0].destroy()
            self.se.tournament_ctrl(self.frame, dt_tournament)

        def all_player_submit(submit_type):
            if submit_type == 'list':
                data_tournament['players'] = \
                    [data_player[x] for x, select in enumerate(select_players) if select.get()]

            self.new_window[0].destroy()
            ctrl_name = self.se.search_name_widget(self.frame, 'selectPlayers')

            if not ctrl_name:
                if len(self.se.new_all_players) > 0 or len(data_tournament['players']) > 0:
                    submit = ttk.Button(self.frame, text="Valider", name='selectPlayers',
                                        command=lambda: tournament_submit(data_tournament))
                    submit.grid(columnspan=7, pady=30, ipadx=5)

        Label(self.frame, bg="#FEF9E7", font=self.lc_cal, text="Nouveau Tournoi : ").grid(row=0, columnspan=7, pady=18)

        name = self.input_text(mst=self.frame, lb_row=2, ip_row=3, cols=1, colspan=6, bg="#FEF9E7", text="Nom : ",
                               ip_wh=20)
        address = self.input_text(mst=self.frame, lb_row=5, ip_row=6, cols=1, colspan=6, bg="#FEF9E7",
                                  text="Adresse : ", ip_wh=60)
        birth_start = self.input_date(mst=self.frame, lb_row=8, ip_row=9, bg="#FEF9E7", text="Date de début : ")

        number_turns = self.input_text(mst=self.frame, lb_row=11, ip_row=12, cols=1, colspan=6, bg="#FEF9E7",
                                       text="Choisissez un nombre de tour", ip_wh=10)
        number_turns.insert(0, '4')

        Label(self.frame, bg="#FEF9E7", font=self.new_r,
              text="Sélection des joueurs").grid(row=14, column=3, columnspan=4, sticky="w", pady=9)

        ttk.Button(self.frame, text="Créer", command=lambda: new_player()).grid(row=15, column=1, columnspan=3, pady=5)
        ttk.Button(self.frame, text="Rechercher", command=lambda: new_list()).grid(row=15, column=4, columnspan=3,
                                                                                   pady=5)
        address.update(), name.update()
        col0_x: list = self.adjust_x(address, name)
        Label(self.frame, bg="#FEF9E7").grid(row=0, column=0, ipadx=int(col0_x[2] / 2) - 20)
        Label(self.frame, bg="#FEF9E7").grid(row=9, column=6, ipadx=col0_x[2])
        Label(self.frame, bg="#FEF9E7").grid(row=4, column=1, columnspan=5)
        Label(self.frame, bg="#FEF9E7").grid(row=7, column=1, columnspan=5)
        Label(self.frame, bg="#FEF9E7").grid(row=10, column=1, columnspan=5)
        Label(self.frame, bg="#FEF9E7").grid(row=13, column=1, columnspan=5)

        data_tournament['name'] = name
        data_tournament['address'] = address
        data_tournament['birth_start'] = birth_start
        data_tournament['numberRound'] = number_turns
        data_tournament['players'] = []

        def new_list():

            view_list = self.list_players(data_player, select_players, 'Sélection des joueurs')
            self.new_window = view_list[0]

            submit_list = ttk.Button(view_list[1], text="Valider", command=lambda: all_player_submit('list'))
            submit_list.grid(column=0, columnspan=2, pady=20, ipadx=20)

        def new_player():
            _data = self.create_player()

            def cr_player(plr_data):
                ctrl_result = self.se.tournament_ctrl_player(self.new_frame, plr_data)
                if ctrl_result:
                    infos_plr = [{'identity': ctrl_result[0], 'last_name': ctrl_result[1],
                                  'first_name': ctrl_result[2], 'point': ctrl_result[3]}]
                    _data_player = self.se.instance_player(infos_plr)
                    if _data_player:
                        self.se.new_all_players.append(_data_player[0])
                        all_player_submit('player')

                self.new_window[0].destroy()

            ttk.Button(self.new_frame, text="  Valider  ",
                       command=lambda: cr_player(_data)).grid(row=13, columnspan=3, pady=15)

    # fonction attachée a la fonction new_tournament
    def create_player(self):
        """
        :return: Sous fonction de la fonction new_tournament()
         Valeur de saisie création d'un joueur tournoi
        """
        if self.new_window:
            self.new_window[0].destroy()
        self.new_window = self.se.listing_window(40, 50, 40, 40, 'Ajouter un joueur', '#FEF9E7')

        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0.4, anchor='center')

        plr_title = Label(self.new_frame, bg="#FEF9E7", font=self.lc_cal, text="Nouveau joueur tournoi : ")
        plr_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=3)

        identity = self.input_text(mst=self.new_frame, lb_row=2, ip_row=3, cols=1, colspan=None, bg="#FEF9E7",
                                   text="Identifiant : ", ip_wh=20)
        last_name = self.input_text(mst=self.new_frame, lb_row=5, ip_row=6, cols=1, colspan=None, bg="#FEF9E7",
                                    text="Nom : ", ip_wh=20)
        first_name = self.input_text(mst=self.new_frame, lb_row=8, ip_row=9, cols=1, colspan=None, bg="#FEF9E7",
                                     text="Prénom : ", ip_wh=20)
        point = self.input_text(mst=self.new_frame, lb_row=11, ip_row=12, cols=1, colspan=None, bg="#FEF9E7",
                                text="Point(s) : ", ip_wh=10)
        point.insert(0, "0.0")

        _data = {'identity': identity, 'last_name': last_name, 'first_name': first_name, 'point': point}

        """ttk.Button(self.new_frame, text="  Valider  ",
                   command=lambda: cr_player(_data)).grid(row=13, columnspan=3, pady=15)"""

        plr_title.update(), last_name.update()
        col_x: list = self.adjust_x(plr_title, last_name)
        Label(self.new_frame, bg="#FEF9E7").grid(row=1, column=0, ipadx=int(col_x[2] / 4))

        Label(self.new_frame, bg="#FEF9E7").grid(row=4, column=1)
        Label(self.new_frame, bg="#FEF9E7").grid(row=7, column=1)
        Label(self.new_frame, bg="#FEF9E7").grid(row=10, column=1)

        """def cr_player(plr_data):
            ctrl_result = self.se.tournament_ctrl_player(self.new_frame, plr_data)
            if ctrl_result:
                infos_plr = [{'identity': ctrl_result[0], 'last_name': ctrl_result[1], 'first_name': ctrl_result[2],
                              'point': ctrl_result[3]}]
                _data_player = self.se.instance_player(infos_plr)
                if _data_player:
                    self.se.new_all_players.append(_data_player[0])"""

        return _data

    def detail_tournament(self, tournament: object, result_round=None):
        """
        :param tournament:
        :param result_round:
        :return: Vue en détaille d'un tournoi
        """
        last_rd = tournament.rounds[-1]
        last_finish = last_rd.finish

        def comment():
            new_comment = _comment.get("1.0", "end-1c")
            new_comment.strip()
            self.se.tournament_comment(new_comment)

        if len(self.se.new_all_players) > 0:
            self.se.new_all_players.clear()

        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(60, 85)
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

        self.title(family="Times New Roman", size=14, weight="bold", slant="roman", underline=False, mst=self.frame,
                   bg="#FEF9E7", justify=None, text="Commentaire :", width=None, row=4, cols=1, colspan=3, sticky="w",
                   padx=None, pady=10)

        lb_font = font.Font(family='Times New Roman', size=12)
        _comment = ScrolledText(self.frame, height=10, highlightbackground="black", highlightthickness=1, font=lb_font)
        _comment.grid(column=1, columnspan=3, row=5, sticky="w")
        _comment.insert(INSERT, tournament.comment)
        _comment.bind("<KeyRelease>", lambda e: comment(), add=True)
        if last_finish:
            _comment.config(state="disabled")

        Label(self.frame, bg="#FEF9E7").grid(row=10, column=0, ipady=10)

        plr_create = ttk.Button(self.frame, text="Liste des joueurs", command=lambda: players_list())
        plr_create.grid(row=11, column=1, ipadx=20, ipady=5)

        Label(self.frame, bg="#FEF9E7").grid(row=11, column=2, ipadx=20)

        plr_list = ttk.Button(self.frame, text="Liste des tours", command=lambda: round_list())
        plr_list.grid(row=11, column=3, ipadx=20, ipady=5)

        if not last_finish:
            plr_list = ttk.Button(self.frame, text="<= Lancer le tour =>", command=lambda: round_start())
            plr_list.grid(row=12, columnspan=4, pady=40, ipadx=30, ipady=10)

        if result_round:
            self.message(mst=self.frame, family=None, size=12, weight="normal", slant="roman", underline=False,
                         bg="#FEF9E7", name="error", fg=result_round[1], pady=10,
                         text=result_round[0])

        def players_list():
            view_list = self.list_players(tournament.players, None, 'Liste des joueurs')
            self.new_window = view_list[0]

            submit_list = ttk.Button(view_list[1], text="Fermer", command=lambda: self.new_window[0].destroy())
            submit_list.grid(column=0, columnspan=2, pady=20, ipadx=20)

        def round_start():
            last_round = tournament.rounds[-1]
            self.schema_round('round_start', tournament, last_round)

        def round_list():
            self.list_rounds(tournament, tournament.rounds)

    def list_players(self, data_player, select_players, title):
        """
        :param data_player:
        :param select_players:
        :param title:
        :return: Vue liste des joueurs
        """
        if len(data_player) > 0:
            data_player.sort(key=lambda x: x.point, reverse=True)

        if self.new_window:
            self.new_window[0].destroy()
        self.new_window = self.se.listing_window(50, 60, 30, 30, 'Liste des joueurs', '#FEF9E7')
        master_geometrie = self.new_window[1], int(self.new_window[2] - 150)

        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0, anchor='n')

        list_system = self.se.listing_canvas(self.new_frame, 1, '#ffffff', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        view_x = list_system[2]
        view_y = list_system[3]

        self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True,
                   mst=self.new_frame, bg="#FEF9E7", justify="center", text=title, width=None, row=0, cols=0,
                   colspan=2, sticky="n", padx=None, pady=20)
        # En tète listing
        header = ("N° Identité", "Nom", "Prénom", "Score")
        cols = 1
        for title_list in header:
            self.title(family="Times New Roman", size=12, weight="bold", slant="roman", underline=False, mst=frame,
                       bg="#ffffff", justify="center", text=title_list, width=None, row=1,
                       cols=cols, colspan=None, sticky=None, padx=30, pady=30)
            cols += 1

        player_supp = []
        next_line = 2
        if len(self.se.new_all_players) > 0:

            for nw_player in self.se.new_all_players:
                player_supp.append(nw_player.identity)

                identity = Label(frame, bg="#ffffff", justify="center", text=nw_player.identity)
                identity.grid(row=next_line, column=1, padx=30)
                last_name = Label(frame, bg="#ffffff", justify="center", text=nw_player.last_name)
                last_name.grid(row=next_line, column=2, padx=30)
                first_name = Label(frame, bg="#ffffff", justify="center", text=nw_player.first_name)
                first_name.grid(row=next_line, column=3, padx=30)
                score = Label(frame, bg="#ffffff", justify="center", text=nw_player.point)
                score.grid(row=next_line, column=4, padx=30)
                check = Checkbutton(frame, onvalue=1, offvalue=0, bg="#ffffff", offrelief="flat", overrelief="ridge",
                                    indicatoron=True, state="disabled")
                check.grid(row=next_line, column=5, padx=15)
                check.select()
                next_line += 1

            Label(frame, bg="#ffffff", height=1, underline=1).grid(row=next_line, columnspan=6, sticky="w", pady=20)
            next_line += 1

        if len(data_player) > 0:
            for i, dt_player in enumerate(data_player):
                # "equal = None" évite le doublon quand le tournoi est créé avec un joueur dans la fenêtre joueur
                equal = None
                if select_players:
                    for sup_id in player_supp:
                        if sup_id == dt_player.identity:
                            equal = True

                if not equal:
                    identity = Label(frame, bg="#ffffff", justify="center", text=dt_player.identity)
                    identity.grid(row=next_line, column=1, padx=30)
                    last_name = Label(frame, bg="#ffffff", justify="center", text=dt_player.last_name)
                    last_name.grid(row=next_line, column=2, padx=30)
                    first_name = Label(frame, bg="#ffffff", justify="center", text=dt_player.first_name)
                    first_name.grid(row=next_line, column=3, padx=30)
                    score = Label(frame, bg="#ffffff", justify="center", text=dt_player.point)
                    score.grid(row=next_line, column=4, padx=30)
                    if select_players:
                        check = Checkbutton(frame, variable=select_players[i], onvalue=1, offvalue=0, bg="#ffffff",
                                            offrelief="flat", overrelief="ridge", indicatoron=True)
                        check.grid(row=next_line, column=5, padx=15)
                    next_line += 1

        self.se.canvas_roll(canvas, frame, view_x, view_y)

        frame.update()
        col0_x = self.adjust_x(canvas, frame)
        Label(frame, bg="#ffffff").grid(row=0, column=0, ipadx=col0_x[2] // 2)

        return self.new_window, self.new_frame

    def list_rounds(self, tournament: object, data_rounds: list):
        """
        :param tournament:
        :param data_rounds:
        :return: Vue liste des rounds
        """
        if self.new_window:
            self.new_window[0].destroy()
        self.new_window = self.se.listing_window(50, 60, 30, 40, 'Liste des rounds', '#FEF9E7')
        master_geometrie = self.new_window[1], self.new_window[2]

        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", padx=15, pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0, anchor='n')

        self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True,
                   mst=self.new_frame, bg="#FEF9E7", justify=None, text="Liste des Rounds", width=None, row=0,
                   cols=None, colspan=2, sticky=None, padx=None, pady=15)

        cols_x = int(master_geometrie[0] - 100) // 4
        content_y = int(master_geometrie[1] / 3) // 12

        views_rounds = []
        for rd in data_rounds:
            rd_view = [rd.id_round, rd.start, rd.finish, rd.matchs_list]

            if rd_view[1] and not rd_view[2]:
                rd_view[2] = 'En cours'

            elif not rd_view[2]:
                rd_view[2] = 'En attente de lancement'

            if not rd_view[1]:
                rd_view[1] = 'En attente de lancement'

            rd_view[3] = len(rd_view[3])

            views_rounds.append(rd_view)

        columns: tuple = (1, 2, 3, 4)
        header: tuple = ("Numéro", "Date d'ouverture", "Date de fin", "Nombre de matchs")

        content = ttk.Treeview(self.new_frame, columns=columns, show='headings', padding=20, height=content_y)
        content.tag_configure('highlight', background='lightblue')

        for x, head in enumerate(header):
            content.column(columns[x], width=cols_x, anchor="center")
            content.heading(columns[x], text=head)

        for rd in views_rounds:
            list_matchs = [rd[0], rd[1], rd[2], rd[3]]
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
                    self.schema_round('list_rounds', tournament, data_rounds[number])

        def hover(event):
            tree = event.widget
            item = tree.identify_row(event.y)
            tree.tk.call(tree, "tag", "remove", "highlight")
            tree.tk.call(tree, "tag", "add", "highlight", item)

        content.bind("<Motion>", hover, add=True)
        content.bind('<<TreeviewSelect>>', selected, add=True)
        content.grid(row=1, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self.new_frame, orient="vertical", command=content.yview)
        content.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        close_list = ttk.Button(self.new_frame, text="Fermer", command=lambda: self.new_window[0].destroy())
        close_list.grid(row=2, column=0, columnspan=2, pady=20, ipadx=20)

    def list_tournament(self, title: str, data_tournament: list):
        """
        :param title:
        :param data_tournament:
        :return: Vue liste des tournois
        """
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(70, 70)
        self.se.minsize(width=master_geometrie[0], height=master_geometrie[1])
        self.frame.place(relx=0.5, rely=0.1, anchor='n')

        self.title(family="Lucida Calligraphy", size=20, weight="bold", slant="roman", underline=True, mst=self.frame,
                   bg="#FEF9E7", justify=None, text=title, width=None, row=0, cols=None, colspan=2, sticky=None,
                   padx=None, pady=15)

        cols_x_long = int(master_geometrie[0] - 100) // 4
        cols_x_medium = int(master_geometrie[0] - 100) // 8
        cols_x_small = int(master_geometrie[0] - 100) // 12
        cols_x = cols_x_small, cols_x_long, cols_x_long, cols_x_medium, cols_x_small, cols_x_small, cols_x_small
        content_y = int(master_geometrie[1] / 3) // 12

        columns: tuple = ()
        for keys in data_tournament[0]:
            if not keys == 'Commentaires':
                columns = columns + (keys,)

        content = ttk.Treeview(self.frame, columns=columns, show='headings', padding=20, height=content_y)
        content.tag_configure('highlight', background='lightblue')

        for y, keys in enumerate(data_tournament[0]):
            if not keys == 'Commentaires':
                content.column(keys, width=cols_x[y], anchor="center")
                content.heading(keys, text=keys)

        for tournament in data_tournament:
            list_tour = []
            for keys, values in tournament.items():
                if keys == 'Joueurs':
                    values = len(values)
                if keys == 'Rounds':
                    values = len(values)
                if not keys == 'Commentaires':
                    list_tour.append(values)
            content.insert('', END, values=list_tour)

        def selected(event):
            result = None
            for selected_item in content.selection():
                result = content.item(selected_item)['values']

            if result:
                rst_rounds = None
                rst_players = None
                rst_comment = None
                for tour in data_tournament:
                    for kys in tour:
                        if kys == 'id' and tour[kys] == result[0]:
                            rst_rounds = tour['Rounds']
                            rst_players = tour['Joueurs']
                            rst_comment = tour['Commentaires']
                if rst_rounds and rst_players:
                    self.se.tournament_treatment('data', self.frame, result[0], result[1], result[2], result[3],
                                                 result[4], rst_rounds, rst_players, rst_comment)

        def hover(event):
            tree = event.widget
            item = tree.identify_row(event.y)
            tree.tk.call(tree, "tag", "remove", "highlight")
            tree.tk.call(tree, "tag", "add", "highlight", item)

        content.bind("<Motion>", hover, add=True)
        content.bind('<<TreeviewSelect>>', selected, add=True)
        content.grid(row=1, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=content.yview)
        content.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

    def schema_round(self, type_round, tournament: object, new_round: object):
        """
        :param type_round:
        :param tournament:
        :param new_round:
        :return: Vu déroulement des matchs d'un round
        """
        text_start = "Ce round n'est pas encore lancé"
        text_finish = 'En attente'
        if new_round.start:
            text_start = new_round.start
        if new_round.finish:
            text_finish = new_round.finish
        elif new_round.start and not new_round.finish:
            text_finish = 'En cours'

        if self.new_window:
            self.new_window[0].destroy()
        self.new_window = self.se.listing_window(60, 90, 100, 30, f'Round n° {new_round.id_round}', '#FEF9E7')
        self.new_frame = Frame(self.new_window[0], bg="#FEF9E7", pady=10)
        self.new_frame.grid()
        self.new_frame.place(relx=0.5, rely=0, anchor='n')

        name = Label(self.new_frame, bg="#FEF9E7", font=self.new_r, text=f"Round n° {new_round.id_round}")
        name.grid(row=0, columnspan=2, sticky="w", padx=20, pady=15)

        start = Label(self.new_frame, bg="#FEF9E7", font=self.new_r, text=f"Ouverture du round le : {text_start}")
        start.grid(row=1, columnspan=2, sticky="w", padx=20)

        finish = Label(self.new_frame, bg="#FEF9E7", font=self.new_r, text=f"Round terminé le : {text_finish}")
        finish.grid(row=2, columnspan=2, sticky="w", padx=20, pady=5)

        name.update(), start.update(), finish.update()
        head_y = int(name.winfo_height() + start.winfo_height() + finish.winfo_height() + 15) * 2
        master_geometrie = self.new_window[1], int(self.new_window[2] - head_y)
        list_system = self.se.listing_canvas(self.new_frame, 3, '#ffffff', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        view_x = list_system[2]
        view_y = list_system[3]
        next_line = 0
        number_key = 0

        def view_player1(_match, parent, frames_list, color):
            plr1_ = Label(parent, width=15, bg="#ffffff", highlightbackground="black", highlightthickness=1,
                          font=self.new_r, foreground=color, text=_match.name_plr1, name=f"id-{_match.identity_plr1}")
            plr1_.bind("<Button-1>", lambda e: self.schema_round_action('player1', type_round, tournament,
                                                                        new_round, start, _match, parent,
                                                                        frames_list,), add=True)
            plr1_.grid(row=0, padx=10)

        def view_player2(_match, parent, frames_list, color):
            plr2_ = Label(parent, width=15, bg="#ffffff", highlightbackground="black", highlightthickness=1,
                          font=self.new_r, foreground=color, text=_match.name_plr2, name=f"id-{_match.identity_plr2}")
            plr2_.bind("<Button-1>", lambda e: self.schema_round_action('player2', type_round, tournament,
                                                                        new_round, start, _match, parent, frames_list),
                       add=True)
            plr2_.grid(row=2, padx=10)

        def result_null(_match, parent, frames_list):
            null = Label(parent, width=10, bg="#ffffff", highlightbackground="black", highlightthickness=1,
                         font=self.new_r_mini, foreground='blue', text="Match null")
            null.bind("<Button-1>", lambda e: self.schema_round_action('equal', type_round, tournament,
                                                                       new_round, start, _match, parent, frames_list),
                      add=True)
            null.grid(row=1, column=0, pady=15)

        frame_list = []
        for _matchs in new_round.matchs_list:
            foreground1 = 'black'
            foreground2 = 'black'
            result_match = 'Non lancé'

            if new_round.start:
                if _matchs.score_plr1 == 0.0 and _matchs.score_plr2 == 0.0:
                    result_match = 'En cours'

                elif _matchs.score_plr1 > _matchs.score_plr2:
                    result_match = _matchs.name_plr1
                    foreground1 = 'green'
                    foreground2 = 'red'

                elif _matchs.score_plr2 > _matchs.score_plr1:
                    result_match = _matchs.name_plr2
                    foreground1 = 'red'
                    foreground2 = 'green'

                elif _matchs.score_plr1 == _matchs.score_plr2:
                    result_match = 'Match null'
                    foreground1 = 'blue'
                    foreground2 = 'blue'

            match_frame = Frame(frame, name=str(number_key), highlightbackground="black", highlightthickness=1,
                                bg="#f5cb8e", pady=30)
            match_frame.grid(row=next_line, column=1)

            view_player1(_matchs, match_frame, frame_list, foreground1)

            result_null(_matchs, match_frame, frame_list)

            result = Label(match_frame, width=15, bg="#ffffff", highlightbackground="black", highlightthickness=1,
                           font=self.new_r, text=result_match, name="score")
            result.grid(row=1, column=2, padx=10)

            view_player2(_matchs, match_frame, frame_list, foreground2)

            next_line += 1
            Label(frame).grid(row=next_line, column=1)
            next_line += 1
            number_key += 1
            frame_list.append(match_frame)

        self.se.canvas_roll(canvas, frame, view_x, view_y)

        frame.update()
        col0_x = self.adjust_x(canvas, frame)
        Label(frame, bg="#ffffff").grid(row=0, column=0, ipadx=col0_x[2] // 2)

        sub = ttk.Button(self.new_frame, text=f"Valider le tour n° {new_round.id_round}",
                         command=lambda: self.submit_l(new_round, frame_list, type_round, tournament))
        sub.grid(column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

    # fonction attachée a la fonction schema_round
    def schema_round_action(self, action_type, type_round, tournament, new_round, start, match, parent, frames_lists):
        """
        :param action_type:
        :param type_round:
        :param tournament:
        :param new_round:
        :param start:
        :param match:
        :param parent:
        :param frames_lists:
        :return: Sous fonction de la fonction schema_round()
        """
        if not new_round.finish and type_round == 'round_start':
            match_key = parent.winfo_name()
            widget_player1 = None
            widget_player2 = None
            widget_score = None

            # Lancement du round
            if not new_round.start:
                new_round.start = self.se.update_date(('start', tournament.id_tour), self.new_frame)
                start.config(text=f"Ouverture du round le : {new_round.start}")
                for _frame in frames_lists:
                    key_frames = _frame.winfo_name()
                    if not match_key == key_frames:
                        for child in _frame.winfo_children():
                            child_name = child.winfo_name()
                            if child_name == 'score':
                                child['text'] = 'En cours'

            # Récupération des vues
            for child in parent.winfo_children():
                widget_name = child.winfo_name()
                id_n = widget_name.find('id-')
                widget_id_player = widget_name[id_n + 3:]

                if widget_id_player == match.identity_plr1:
                    widget_player1 = child

                if widget_id_player == match.identity_plr2:
                    widget_player2 = child

                if widget_name == 'score':
                    widget_score = child

            # traitement
            match action_type:

                case 'equal':
                    match.score_plr1 = 0.5
                    match.score_plr2 = 0.5
                    results = [(match.identity_plr1, 0.5), (match.identity_plr2, 0.5)]
                    widget_player1.configure(foreground='blue')
                    widget_player2.configure(foreground='blue')
                    widget_score['text'] = 'Match null'

                case 'player1':
                    match.score_plr1 = 1.0
                    match.score_plr2 = 0.0
                    results = [(match.identity_plr1, match.score_plr1), (match.identity_plr2, match.score_plr2)]
                    widget_player1.configure(foreground='green')
                    widget_player2.configure(foreground='red')
                    widget_score['text'] = match.name_plr1

                case 'player2':
                    match.score_plr1 = 0.0
                    match.score_plr2 = 1.0
                    results = [(match.identity_plr2, match.score_plr2), (match.identity_plr1, match.score_plr1)]
                    widget_player1.configure(foreground='red')
                    widget_player2.configure(foreground='green')
                    widget_score['text'] = match.name_plr2
                case _:
                    results = None

            if results:
                data_match = (tournament.id_tour, match_key, results)
                self.se.update_score(data_match, self.new_frame)
        else:
            pass

    # fonction attachée a la fonction schema_round
    def submit_l(self, new_round, frame_list, type_round, tournament):
        """
        :param new_round:
        :param frame_list:
        :param type_round:
        :param tournament:
        :return: Sous fonction de la fonction schema_round()
        """
        not_submit = False
        text_list = ['En cours', 'Non lancé']

        if not new_round.finish:
            for _frame in frame_list:
                for child in _frame.winfo_children():
                    child_name = child.winfo_name()
                    child_text = child['text']
                    if child_text in text_list and child_name == 'score':
                        not_submit = child_text

            if not not_submit and type_round == 'round_start':
                self.se.round_treatment(tournament)
                self.new_window[0].destroy()

            if not_submit == 'En cours':
                messagebox.showwarning(title='Avertissement', message='Un ou plusieurs match(s) sont en cours')

            elif not_submit == 'Non lancé':
                messagebox.showwarning(title='Avertissement', message='Lancer le round dans la fenêtre tournoi et '
                                                                      'cliqué sur un joueur ou match null pour '
                                                                      'lancer le tour')
        else:
            self.new_window[0].destroy()

    @staticmethod
    def message(**kwargs: any) -> any:
        """
        :param kwargs:
        :return: Message d'alerte
        """
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(kwargs['mst'], bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        kwargs['mst'].after(12000, label.destroy)
