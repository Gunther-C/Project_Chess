from tkinter import ttk, font, Menu, Frame, Entry, Label, DISABLED, END

from core import extend_view


class PlayersViews(extend_view.ExtendViews):
    def __init__(self, new_self: any):

        self.se = new_self

        self.frame = Frame(self.se, bg="#FEF9E7", padx=15, pady=10)
        self.frame.grid()
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        super().__init__(self.frame)

    def new_menu(self):
        """
        :return: Menu principale
        """
        self.se.menu_players = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_choice())
        self.se.menu.add_cascade(label="Joueurs", menu=self.se.menu_players)
        self.se.menu.add_command(label="Debug", command=lambda: self.se.debug())
        self.se.menu.add_command(label="Quitter", command=self.se.destroy)
        self.se.config(menu=self.se.menu)

    def menu_choice(self):
        """
        :return: Menu secondaire
        """
        if not self.se.widjets_menu1:
            self.se.menu_searching = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_search())
            self.se.menu_listing = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_list())
            self.se.menu_players.add_command(label="Ajouter un joueur", command=lambda: self.create_player())
            self.se.menu_players.add_cascade(label="Chercher un joueur par :", menu=self.se.menu_searching)
            self.se.menu_players.add_cascade(label="Liste des joueurs par :", menu=self.se.menu_listing)
            self.se.widjets_menu1 = True

    def menu_list(self):
        """
        :return: Menu du style de listes de joueurs
        """
        if not self.se.widjets_menu2:
            self.se.menu_listing.add_command(label="Ordre alphabétique", command=lambda: self.se.recover_list('name'))
            self.se.menu_listing.add_command(label="Odre d'inscription",
                                             command=lambda: self.se.recover_list('registration'))
            self.se.menu_listing.add_command(label="Point(s) gagné(s)", command=lambda: self.se.recover_list('score'))
            self.se.widjets_menu2 = True

    def menu_search(self):
        """
        :return: Menu du style de recherche
        """
        if not self.se.widjets_menu3:
            self.se.menu_searching.add_command(label="Nom", command=lambda: self.search_player('last_name'))
            self.se.menu_searching.add_command(label="Identifiant", command=lambda: self.search_player('identity'))
            self.se.widjets_menu3 = True

    def create_player(self):
        """
        :return: Création d'un joueur
        """
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(50, 60)
        self.se.minsize(width=int(master_geometrie[0] * 0.60), height=int(master_geometrie[1] * 0.90))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        title = self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True,
                           mst=self.frame, bg="#FEF9E7", justify=None, text="Nouveau joueur : ", width=None,
                           row=0, cols=None, colspan=7, sticky=None, padx=None, pady=None)

        identity = self.input_text(mst=self.frame, lb_row=2, ip_row=3, cols=1, colspan=5, bg="#FEF9E7",
                                   text="Identifiant : ", ip_wh=20)

        last_name = self.input_text(mst=self.frame, lb_row=5, ip_row=6, cols=1, colspan=5, bg="#FEF9E7",
                                    text="Nom : ", ip_wh=20)

        first_name = self.input_text(mst=self.frame, lb_row=8, ip_row=9, cols=1, colspan=5, bg="#FEF9E7",
                                     text="Prénom : ", ip_wh=20)

        birth = self.input_date(mst=self.frame, lb_row=11, ip_row=12, bg="#FEF9E7", text="Date de naissance : ")

        point = self.input_text(mst=self.frame, lb_row=14, ip_row=15, cols=1, colspan=5, bg="#FEF9E7",
                                text="Point(s) : ", ip_wh=10)
        point.insert(0, "0")
        data_player = {'identity': identity, 'last_name': last_name, 'first_name': first_name, 'birth': birth,
                       'point': point}

        submit = ttk.Button(self.frame, text="  Valider  ",
                            command=lambda: self.se.player_ctrl(self.frame, data_player))
        submit.grid(columnspan=7, pady=20)

        space_x: list = self.adjust_x(title, last_name)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=1, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=4, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=7, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=10, cols=6, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=13, cols=6, colspan=None, sticky=None)

    def insert_player(self, dt_player: object):
        """
        :param dt_player:
        :return: Résultat de l'ajout d'un joueur
        """
        def click(type_choice):
            if type_choice == 'save':
                self.se.save_or_tournament('save', dt_player)
                insert.config(state=DISABLED)
            else:
                self.se.save_or_tournament('tournament', dt_player)

        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(50, 60)
        self.se.minsize(width=int(master_geometrie[0] * 0.60), height=int(master_geometrie[1] * 0.90))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        title = self.title(family=None, size=15, weight="bold", slant="roman", underline=True,  mst=self.frame,
                           bg="#FEF9E7", justify=None, text="Que voulez-vous faire : ", width=None, row=0, cols=None,
                           colspan=5, sticky=None, padx=None, pady=None)

        header = ['Identité', 'Nom', 'Prénom', 'Date de naissance', 'Point(s)']
        players = [dt_player.identity, dt_player.last_name, dt_player.first_name, dt_player.birth, dt_player.point]
        next_line = 2

        for head, player_val in zip(header, players):
            self.title(family=None, size=10, weight="bold", slant="roman", underline=False, mst=self.frame,
                       bg="#FEF9E7", justify="right", text=head, width=None, row=next_line, cols=1,
                       colspan=None, sticky="e", padx=None, pady=None)
            self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=None,
                       justify="left", text=player_val, row=next_line, cols=3, colspan=None, sticky="w")
            next_line += 1

        insert = ttk.Button(self.frame, text=" Ajouter à la liste des joueurs ", command=lambda: click('save'))
        insert.grid(row=(next_line + 2), columnspan=5)

        create = ttk.Button(self.frame, text=" Créer un tournoi avec ce joueur ", command=lambda: click('tournament'))
        create.grid(row=(next_line + 1), columnspan=5, pady=20)

        annule = ttk.Button(self.frame, text=" Annuler ", command=lambda: self.se.clear_frame(self.frame))
        annule.grid(row=(next_line + 3), columnspan=5, pady=20)

        insert.update()
        space_x: list = self.adjust_x(title, insert)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=1, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=9, ipady=None,
                   justify=None, text="", row=1, cols=2, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=1, cols=4, colspan=None, sticky=None)

    def search_player(self, choice_type):
        """
        :param choice_type:
        :return: Recherche par nom ou numéro d'identité national
        """
        self.se.background['image'] = ""
        self.se.clear_frame(self.frame)
        view_master = self.se.master_window(50, 60)
        self.se.minsize(width=int(view_master[0] * 0.60), height=int(view_master[1] * 0.90))
        self.frame.place(relx=0.5, rely=0.3, anchor='center')

        (Label(self.frame, bg="#FEF9E7", font=self.lc_cal, text="Rechercher un joueur : ")
         .grid(row=0, columnspan=3, pady=20))

        result_text = "Par Nom : "
        if choice_type == "identity":
            result_text = "Par numéro d'Identité"

        Label(self.frame, bg="#FEF9E7", text=result_text).grid(row=2, column=1, columnspan=3, sticky='w')

        result = Entry(self.frame, width=20)
        result.grid(row=3, column=1, columnspan=3, sticky='w')

        data_player = {choice_type: result}

        (ttk.Button(self.frame, text="  Valider  ", command=lambda: self.se.search_menu(self.frame, data_player))
         .grid(row=4, columnspan=3, pady=20))

    def matching_multi_players(self, multi_players: list):
        """
        :param multi_players:
        :return: Plusieurs résultats trouvés lors d'une recherche par nom
        """
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(50, 60)
        self.se.minsize(width=int(master_geometrie[0] * 0.60), height=int(master_geometrie[1] * 0.90))
        self.frame.place(relx=0.5, rely=0, anchor='n')

        list_system = self.se.listing_canvas(self.frame, 0, '#FEF9E7', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        view_x = list_system[2]
        view_y = list_system[3]

        self.title(family=None, size=15, weight="bold", slant="roman", underline=True,  mst=frame, bg="#FEF9E7",
                   justify=None, text="Plusieurs résultats : ", width=None, row=0, cols=1, colspan=2,  sticky=None,
                   padx=10, pady=None)

        def player_button(data_player, next_row):
            button = ttk.Button(frame, text=f" {data_player.last_name} {data_player.first_name} ",
                                command=lambda: self.matching_player(data_player))
            button.grid(row=next_row, column=1, columnspan=2, pady=10, ipadx=20)

        next_line = 2
        for player in multi_players:
            player_button(player, next_line)
            next_line += 1

        annule = ttk.Button(frame, text=" Annuler ", command=lambda: self.se.clear_frame(self.frame))
        annule.grid(row=next_line, column=1, columnspan=2, pady=30)

        self.se.canvas_roll(canvas, frame, view_x, view_y)

        frame.update()
        col0_x = self.adjust_x(canvas, frame)
        Label(frame, bg="#FEF9E7").grid(row=0, column=0, ipadx=col0_x[2] // 2)

    def matching_player(self, dt_player: object):
        """
        :param dt_player:
        :return: Résultat de la recherche d'un joueur
        """
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(50, 60)
        self.se.minsize(width=int(master_geometrie[0] * 0.60), height=int(master_geometrie[1] * 0.90))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        title = self.title(family=None, size=15, weight="bold", slant="roman", underline=True, mst=self.frame,
                           bg="#FEF9E7", justify=None, text="Résultat de la recherche : ", width=None, row=0,
                           cols=None, colspan=5, sticky=None, padx=None, pady=None)

        header = ['Identité', 'Nom', 'Prénom', 'Date de naissance', 'Point(s)']
        players = [dt_player.identity, dt_player.last_name, dt_player.first_name, dt_player.birth, dt_player.point]
        next_line = 2
        for head, player_val in zip(header, players):
            self.title(family=None, size=10, weight="bold", slant="roman", underline=False, mst=self.frame,
                       bg="#FEF9E7", justify="right", text=head, width=None, row=next_line, cols=1,
                       colspan=None, sticky="e", padx=None, pady=None)
            self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=None,
                       justify="left", text=player_val, row=next_line, cols=3, colspan=None, sticky="w")
            next_line += 1

        create_trt = ttk.Button(self.frame, text=" Créer un tournoi avec ce joueur ",
                                command=lambda: self.se.save_or_tournament('tournament', dt_player))
        create_trt.grid(row=(next_line + 1), columnspan=5, pady=20)

        annule = ttk.Button(self.frame, text=" Annuler ", command=lambda: self.se.clear_frame(self.frame))
        annule.grid(row=(next_line + 2), columnspan=5, pady=20)

        create_trt.update()
        space_x: list = self.adjust_x(title, create_trt)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=1, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=9, ipady=None,
                   justify=None, text="", row=1, cols=2, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7", ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=1, cols=4, colspan=None, sticky=None)

    def list_players(self, title: str, data_players: list):
        """
        :param title:
        :param data_players:
        :return: Liste des joueurs en bdd
        """
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(60, 70)
        self.se.minsize(width=master_geometrie[0], height=master_geometrie[1])
        self.frame.place(relx=0.5, rely=0.1, anchor='n')

        self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True, mst=self.frame,
                   bg="#FEF9E7", justify=None, text=title, width=None, row=0, cols=None, colspan=2, sticky=None,
                   padx=None, pady=15)

        cols_x = int(master_geometrie[0] - 200) // 6
        content_y = int(master_geometrie[1] / 3) // 12
        columns: tuple = (1, 2, 3, 4, 5, 6)
        header: tuple = ('Ordre d\'inscription', ' Identité', 'Nom', 'Prénom', 'Date de naissance', 'Point(s)')

        content = ttk.Treeview(self.frame, columns=columns, show='headings', padding=20, height=content_y)
        content.tag_configure('highlight', background='lightblue')

        for x, head in enumerate(header):
            content.column(columns[x], width=cols_x, anchor="center")
            content.heading(columns[x], text=head)

        for player in data_players:
            list_players = [player.id_player, player.identity, player.last_name, player.first_name, player.birth,
                            player.point]
            content.insert('', END, values=list_players)

        def item_selected(event):
            result = None
            for selected_item in content.selection():
                result = content.item(selected_item)['values']

            if result:
                data_player = None
                for dt_player in data_players:
                    if dt_player.identity == result[1]:
                        data_player = dt_player
                if data_player:
                    self.matching_player(data_player)

        def hover(event):
            tree = event.widget
            item = tree.identify_row(event.y)
            tree.tk.call(tree, "tag", "remove", "highlight")
            tree.tk.call(tree, "tag", "add", "highlight", item)

        content.bind("<Motion>", hover, add=True)
        content.bind('<<TreeviewSelect>>', item_selected, add=True)
        content.grid(row=1, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=content.yview)
        content.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

    def message(self, **kwargs: any) -> any:
        """
        :param kwargs:
        :return: Message d'alerte
        """
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(self.frame, bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        self.frame.after(10000, label.destroy)
