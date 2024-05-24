from tkinter import *
from tkinter import ttk
from tkinter import font
from core import extend_view


class PlayersViews(extend_view.ExtendViews):
    def __init__(self, new_self: any):

        self.se = new_self

        self.frame = Frame(self.se, bg="#FEF9E7", padx=15, pady=10)
        self.frame.grid()
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        super().__init__(self.frame)

    def new_menu(self):
        self.se.menu_players = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_choice())
        self.se.menu.add_cascade(label="Joueurs", menu=self.se.menu_players)
        self.se.menu.add_command(label="Quitter", command=self.se.destroy)
        self.se.config(menu=self.se.menu)

    def menu_choice(self):
        if not self.se.widjets_menu1:
            self.se.menu_searching = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_search())
            self.se.menu_listing = Menu(self.se.menu, tearoff=0, postcommand=lambda: self.menu_list())
            self.se.menu_players.add_command(label="Ajouter un joueur", command=lambda: self.create_player())
            self.se.menu_players.add_cascade(label="Chercher un joueur par :", menu=self.se.menu_searching)
            self.se.menu_players.add_cascade(label="Liste des joueurs par :", menu=self.se.menu_listing)
            self.se.widjets_menu1 = True

    def menu_list(self):
        if not self.se.widjets_menu2:
            self.se.menu_listing.add_command(label="Ordre alphabétique", command=lambda: self.se.recover_list('names'))
            self.se.menu_listing.add_command(label="Tournoi(s) gagné(s)",
                                             command=lambda: self.se.recover_list('tournaments'))
            self.se.menu_listing.add_command(label="Partie(s) gagnée(s)", command=lambda: self.se.recover_list('games'))
            self.se.widjets_menu2 = True

    def menu_search(self):
        if not self.se.widjets_menu3:
            self.se.menu_searching.add_command(label="Nom", command=lambda: self.search_player('Nom'))
            self.se.menu_searching.add_command(label="Identifiant", command=lambda: self.search_player('Identité'))
            self.se.widjets_menu3 = True

    def create_player(self):
        self.se.clear_frame(self.frame)
        view_master = self.se.master_window(50, 60)
        self.se.minsize(width=int(view_master[0] * 0.60), height=int(view_master[1] * 0.90))
        self.frame.place(relx=0.5, rely=0.4, anchor='center')

        title = self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True,
                           mst=self.frame, bg="#FEF9E7", justify=None, text="Nouveau joueur : ", width=None,
                           row=0, cols=None, colspan=7, sticky=None, padx=None, pady=None)

        last_name = self.input_text(mst=self.frame, lb_row=2, ip_row=3, cols=1, colspan=5, bg="#FEF9E7",
                                    text="Nom : ", ip_wh=20)
        first_name = self.input_text(mst=self.frame, lb_row=5, ip_row=6, cols=1, colspan=5, bg="#FEF9E7",
                                     text="Prénom : ", ip_wh=20)
        birth = self.input_date(mst=self.frame, lb_row=8, ip_row=9, bg="#FEF9E7", text="Date de naissance : ")

        identity = self.input_text(mst=self.frame, lb_row=11, ip_row=12, cols=1, colspan=5, bg="#FEF9E7",
                                   text="Identifiant : ", ip_wh=20)

        data_player = {'identity': identity, 'last_name': last_name, 'first_name': first_name, 'birth': birth}

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

    def insert_player(self, data_pl: object):
        data_player = {
            'Identité': data_pl.identity,
            'Nom': data_pl.last_name,
            'Prénom': data_pl.first_name,
            'Date de naissance': data_pl.birth
        }

        def click(type_choice):
            if type_choice == 'save':
                self.se.save_or_tournament('save', data_player)
                insert.config(state=DISABLED)
            else:
                self.se.save_or_tournament('tournament', data_player)

        self.se.clear_frame(self.frame)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        title = self.title(family=None, size=15, weight="bold", slant="roman", underline=True,  mst=self.frame,
                           bg="#FEF9E7", justify=None, text="Que voulez-vous faire : ", width=None, row=0, cols=None,
                           colspan=5, sticky=None, padx=None, pady=None)
        next_line = 2
        for keys, values in data_player.items():
            self.title(family=None, size=10, weight="bold", slant="roman", underline=False, mst=self.frame,
                       bg="#FEF9E7", justify="right", text=keys, width=None, row=next_line, cols=1,
                       colspan=None, sticky="e", padx=None, pady=None)
            self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=None,
                       justify="left", text=values, row=next_line, cols=3, colspan=None, sticky="w")
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
        # Recherche par nom
        self.se.clear_frame(self.frame)
        view_master = self.se.master_window(50, 60)
        self.se.minsize(width=int(view_master[0] * 0.60), height=int(view_master[1] * 0.90))
        self.frame.place(relx=0.5, rely=0.3, anchor='center')

        title = self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True,
                           mst=self.frame, bg="#FEF9E7", justify=None, text="Rechercher un joueur : ", width=None,
                           row=0, cols=None, colspan=3, sticky=None, padx=None, pady=None)

        result = self.input_text(mst=self.frame, lb_row=2, ip_row=3, cols=1, colspan=None, bg="#FEF9E7",
                                 text=choice_type + " : ", ip_wh=20)

        data_player = {choice_type: result}

        submit = ttk.Button(self.frame, text="  Valider  ",
                            command=lambda: self.se.search_menu(self.frame, data_player))
        submit.grid(columnspan=7, pady=20)

        space_x: list = self.adjust_x(title, result)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7",  ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=1, cols=0, colspan=None, sticky=None)
        self.label(mst=self.frame, width=None, height=-1, bg="#FEF9E7",  ipadx=space_x[2] // 2, ipady=None,
                   justify=None, text="", row=4, cols=2, colspan=None, sticky=None)

    def matching_multi_players(self, multi_players: list):
        self.se.clear_frame(self.frame)

        master_geometrie = self.se.master_window(50, 60)
        self.se.minsize(width=master_geometrie[0], height=master_geometrie[1])

        list_system = self.se.listing_canvas(self.frame, '#FEF9E7', master_geometrie)
        frame = list_system[0]
        canvas = list_system[1]
        scroll_mouse = list_system[2]
        view_x = list_system[3]
        view_y = list_system[4]

        self.frame.place(relx=0.5, rely=0, anchor='n')

        self.title(family=None, size=15, weight="bold", slant="roman", underline=True,  mst=frame, bg="#FEF9E7",
                   justify=None, text="Plusieurs résultats : ", width=None, row=0, cols=1, colspan=2,  sticky=None,
                   padx=10, pady=None)

        def player_button(lst_name, fst_name, dt_player, next_row):
            button = ttk.Button(frame, text=f" {lst_name} {fst_name} ", command=lambda: self.matching_player(dt_player))
            button.grid(row=next_row, column=1, columnspan=2, pady=10)

        next_line = 2
        for player in multi_players:
            last_name = None
            first_name = None
            for keys in player:
                if keys == 'Nom':
                    last_name = player[keys]
                if keys == 'Prénom':
                    first_name = player[keys]

            player_button(last_name, first_name, player, next_line)
            next_line += 1

        annule = ttk.Button(frame, text=" Annuler ", command=lambda: self.se.clear_frame(self.frame))
        annule.grid(row=next_line, column=1, columnspan=2)

        canvas.update()
        canvas.create_window((0, 0), window=frame)
        frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox("all"), width=view_x, height=view_y))
        canvas.bind_all("<MouseWheel>", scroll_mouse)

        frame.update()
        col0_x = self.adjust_x(canvas, frame)
        col0 = Label(frame, bg="#FEF9E7")
        col0.grid(row=0, column=0, ipadx=col0_x[2])

    def matching_player(self, data_player: dict):
        self.se.clear_frame(self.frame)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        title = self.title(family=None, size=15, weight="bold", slant="roman", underline=True, mst=self.frame,
                           bg="#FEF9E7", justify=None, text="Résultat de la recherche : ", width=None, row=0, cols=None,
                           colspan=5, sticky=None, padx=None, pady=None)
        next_line = 2
        instance_player = {}
        for keys, values in data_player.items():
            self.title(family=None, size=10, weight="bold", slant="roman", underline=False, mst=self.frame,
                       bg="#FEF9E7", justify="right", text=keys, width=None, row=next_line, cols=1, colspan=None,
                       sticky="e", padx=None, pady=None)
            self.label(mst=self.frame, width=None, height=None, bg="#FEF9E7", ipadx=None, ipady=None, justify="left",
                       text=values, row=next_line, cols=3, colspan=None, sticky="w")

            instance_player = self.se.instance_player(instance_player, keys, values)
            next_line += 1

        create_trt = ttk.Button(self.frame, text=" Créer un tournoi avec ce joueur ",
                                command=lambda: self.se.save_or_tournament('tournament', instance_player))
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

    def list_player(self, title: str, data_players: list):
        self.se.clear_frame(self.frame)
        master_geometrie = self.se.master_window(70, 70)
        self.se.minsize(width=master_geometrie[0], height=master_geometrie[1])
        self.frame.place(relx=0.5, rely=0.1, anchor='n')

        self.title(family="Lucida Handwriting", size=20, weight="bold", slant="italic", underline=True, mst=self.frame,
                   bg="#FEF9E7", justify=None, text=title, width=None, row=0, cols=None, colspan=2, sticky=None,
                   padx=None, pady=15)

        cols_x = int(master_geometrie[0] - 200) // 9
        content_y = int(master_geometrie[1] / 3) // 12

        """data_tournament = []
        for x in range(10):
            for tournament in data_tour:
                data_tournament.append(tournament)"""

        columns: tuple = ()
        for col_name in data_players[0]:
            columns = columns + (col_name,)

        content = ttk.Treeview(self.frame, columns=columns, show='headings', padding=20, height=content_y)
        content.tag_configure('highlight', background='lightblue')

        for head_name in data_players[0]:
            content.column(head_name, width=cols_x, anchor="center")
            content.heading(head_name, text=head_name)

        for player in data_players:
            list_players = []
            for keys, values in player.items():
                list_players.append(values)
            content.insert('', END, values=list_players)

        def item_selected(event):
            result = None
            for selected_item in content.selection():
                result = content.item(selected_item)['values']

            if result:
                data_player = None
                for plr in data_players:
                    for kys in plr:
                        if kys == 'id' and plr[kys] == result[0]:
                            data_player = plr

                if data_player:
                    self.matching_player(data_player)

        def hover(event):
            tree = event.widget
            item = tree.identify_row(event.y)
            tree.tk.call(tree, "tag", "remove", "highlight")
            tree.tk.call(tree, "tag", "add", "highlight", item)

        content.bind("<Motion>", hover)
        content.bind('<<TreeviewSelect>>', item_selected)
        content.grid(row=1, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=content.yview)
        content.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')


    def message(self, **kwargs: any) -> any:
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])
        label = Label(self.frame, bg=kwargs['bg'], font=lb_font, name=kwargs['name'], fg=kwargs['fg'],
                      pady=kwargs['pady'], text=kwargs['text'])
        label.grid(columnspan=10)
        self.frame.after(10000, label.destroy)
