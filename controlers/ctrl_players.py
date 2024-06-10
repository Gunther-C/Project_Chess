from tkinter import *
from tkinter import font, Entry
from tkinter import ttk

from core import core
from core import french_date as date_fr
from rotate import rotation

from database.data_players import PlayersData

from models.mdl_player import PlayersMdl
from views import view_players as view


class PlayersCtrl(core.Core):

    def __init__(self, data_transfer=None):
        super().__init__()

        self.vue = view.PlayersViews(self)
        self.vue.new_menu()
        self.vue.menu_choice()

        """if data_transfer:
            self.new_player = data_transfer
            self.vue.new_player()"""

    def player_ctrl(self, new_frame, data_player):
        errors_dict = {}
        identity = data_player['identity'].get()
        last_name = data_player['last_name'].get()
        first_name = data_player['first_name'].get()
        day = data_player['birth']['day'].get()
        month = data_player['birth']['month'].get()
        year = data_player['birth']['year'].get()
        point = data_player['point'].get()

        if identity:
            errors_dict['identity'] = self.identity_verif(identity)

        if last_name:
            errors_dict['ctrl_lst_1'] = self.long_string_verif("Le Nom", 2, 40, last_name)
            errors_dict['ctrl_lst_2'] = self.string_verif("Le Nom", last_name)

        if first_name:
            errors_dict['ctrl_fst_1'] = self.long_string_verif("Le Prénom", 2, 40, first_name)
            errors_dict['ctrl_fst_2'] = self.string_verif("Le Prénom", first_name)

        if day:
            errors_dict['ctrl_day'] = self.number_verif("Le jour", day)
        if month:
            errors_dict['ctrl_month'] = self.number_verif("Le mois", month)
        if year:
            errors_dict['ctrl_year'] = self.number_verif("L'année joueur", year)

        if point:
            errors_dict['ctrl_point'] = self.number_float_verif("Le Point", point)
            if not errors_dict['ctrl_point']:
                point = float(point)

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name=er[0], fg="red", pady=None, text=er[1])

        elif identity and last_name and first_name and day and month and year:
            birth = date_fr.FrenchDate().new_format_fr(year, month, day)

            result = self.searching(search_type="compare", last_name=last_name, first_name=first_name, birth=birth)
            result2 = self.searching(search_type="searching", identity=identity)

            if len(result) > 0:
                self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name="error1", fg="red", pady=10, text="il semble que ce joueur est déja enregistré")

            elif len(result2) > 0:
                self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name="error1", fg="red", pady=10, text="Ce numéro d'identité éxiste déja !")
            else:
                # instance d'un joueur
                self.new_player = self.instance_player(None, identity, last_name, first_name, birth, point)
                self.vue.insert_player(self.new_player)
        else:
            pass

    def save_or_tournament(self, result, data_player):
        match result:
            case 'save':
                if PlayersData(data_player):
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7",
                                     name="success", fg="green", pady=10, text="Nouveau joueur inséré")
                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error", fg="red", pady=10,
                                     text="Une erreur est survenue, veuillez réessayer.")

            case 'tournament':
                self.destroy()
                self.create_new_tournament(data_player)

            case _:
                pass

    def search_menu(self, new_frame, result):

        if 'last_name' in result:
            self.search_ctrl_name(new_frame, result)

        elif 'identity' in result:
            self.search_ctrl_identity(new_frame, result)

        else:
            pass

    def search_ctrl_name(self, new_frame, result=None):

        if result:
            errors_dict = {}

            last_name = result['last_name'].get()
            errors_dict['ctrl_lst_1'] = self.long_string_verif("Le Nom", 2, 40, last_name)
            errors_dict['ctrl_lst_2'] = self.string_verif("Le Nom", last_name)

            self.destroy_error(new_frame, 1)

            ctrl_errors = self.create_error(errors_dict)
            if len(ctrl_errors) > 0:
                for er in ctrl_errors:
                    self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                     name=er[0], fg="red", pady=None, text=er[1])
            else:

                new_search = self.searching(search_type="searching", last_name=last_name)

                if len(new_search) > 1:
                    player_list = []
                    for player in new_search:
                        inst_player = self.instance_player(player['id'], player['identity'], player['last_name'],
                                                           player['first_name'], player['birth'], player['point'])
                        player_list.append(inst_player)
                    self.vue.matching_multi_players(player_list)

                elif len(new_search) == 1:
                    new_plr = new_search[0]
                    # instance d'un joueur
                    self.new_player = self.instance_player(new_plr['id'], new_plr['identity'], new_plr['last_name'],
                                                           new_plr['first_name'], new_plr['birth'], new_plr['point'])
                    self.vue.matching_player(self.new_player)

                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error1", fg="red", pady=10, text="Ce joueur n'éxiste pas")
        else:
            pass

    def search_ctrl_identity(self, new_frame, result=None):

        if result:
            identity = result['identity'].get()
            verif = self.identity_verif(identity)
            errors_dict = {'identity': verif}

            self.destroy_error(new_frame, 1)

            ctrl_errors = self.create_error(errors_dict)
            if len(ctrl_errors) > 0:
                for er in ctrl_errors:
                    self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                     name=er[0], fg="red", pady=None, text=er[1])
            else:
                new_search = self.searching(search_type="searching", identity=identity)
                if len(new_search) > 0:
                    new_plr = new_search[0]
                    # instance d'un joueur
                    self.new_player = self.instance_player(new_plr['id'], new_plr['identity'], new_plr['last_name'],
                                                           new_plr['first_name'], new_plr['birth'], new_plr['point'])
                    self.vue.matching_player(self.new_player)

                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error1", fg="red", pady=10, text="Ce joueur n'éxiste pas")
        else:
            pass

    def recover_list(self, type_list=None):

        file_players = self.players_list()
        title = ""
        listing = []
        ordered = None

        match type_list:
            case 'name':
                ordered = sorted(file_players, key=lambda x: x['last_name'])
                title = " Liste par ordre alphabétique "

            case 'registration':
                ordered = sorted(file_players, key=lambda x: x['id'])
                title = " Liste par odre d'inscription "

            case 'score':
                # , reverse=True
                ordered = sorted(file_players, key=lambda x: x['point'])
                title = " Liste par ordre de point "

        if ordered:
            for player in ordered:
                new_player = self.instance_player(player['id'], player['identity'], player['last_name'],
                                                  player['first_name'], player['birth'], player['point'])
                listing.append(new_player)

            self.vue.list_players(title, listing)

    @staticmethod
    def create_new_tournament(player_tournament):
        rotation('t', player_tournament)

    @staticmethod
    def instance_player(id_player, identity, last_name, first_name, birth, point):
        instance = PlayersMdl(id_player=id_player, identity=identity, last_name=last_name, first_name=first_name,
                              birth=birth, point=point)
        return instance
