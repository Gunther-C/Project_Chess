from tkinter import *
from tkinter import font, Entry
from tkinter import ttk

from core import core
from rotate import rotation
from database import data_players as data
from models import mdl_player as model
from views import view_players as view
from core import french_date as date_fr


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
            errors_dict['ctrl_point'] = self.number_verif("Point", point)
            if not errors_dict['ctrl_point']:
                point = int(point)

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name=er[0], fg="red", pady=None, text=er[1])

        elif identity and last_name and first_name and day and month and year:
            birth = date_fr.FrenchDate().new_format_fr(year, month, day)
            # birth = year + '-' + month + '-' + day

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
                self.new_player = model.PlayersMdl(identity=identity, last_name=last_name, first_name=first_name,
                                                   birth=birth, point=point)

                print(self.new_player.identity)
                print(self.new_player.last_name)
                print(self.new_player.first_name)
                print(self.new_player.birth)
                print(self.new_player.point)
                # self.vue.insert_player(self.new_player)
        else:
            pass

    def save_or_tournament(self, result, data_player):
        match result:
            case 'save':
                if data.PlayersData(self.new_player):
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7",
                                     name="success", fg="blue", pady=10, text="Joueur inséré")
                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error", fg="red", pady=10,
                                     text="Une erreur est survenue, veuillez réessayer.")

            case 'tournament':
                data_player.pop('Date de naissance', None)
                if len(data_player) == 3:
                    self.create_new_tournament(data_player)
                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error1", fg="red", pady=10,
                                     text="La création du joueur à échoué")
            case _:
                pass

    ###

    def search_menu(self, new_frame, result):
        if 'Nom' in result:
            self.search_ctrl_name(new_frame, result)

        elif 'Identité' in result:
            self.search_ctrl_identity(new_frame, result)

        else:
            pass

    def search_ctrl_name(self, new_frame, result=None):

        if result:
            errors_dict = {}

            last_name = result['Nom'].get()
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
                    self.vue.matching_multi_players(new_search)

                elif len(new_search) == 1:
                    self.vue.matching_player(new_search[0])
                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error1", fg="red", pady=10, text="Ce joueur n'éxiste pas")
        else:
            pass

    def search_ctrl_identity(self, new_frame, result=None):

        if result:
            identity = result['Identité'].get()
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
                    self.vue.matching_player(new_search[0])

                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error1", fg="red", pady=10, text="Ce joueur n'éxiste pas")
        else:
            pass

    def create_new_tournament(self, player_tournament):
        self.destroy()
        rotation('t', player_tournament)

    def recover_list(self, type_list=None):

        file_players = self.players_list()

        match type_list:
            case 'names':
                ordered = sorted(file_players, key=lambda x: x['Nom'])
                self.vue.list_player('Liste par ordre alphabétique', ordered)

            case 'tournaments':
                ordered = sorted(file_players, key=lambda x: x['id'])
                self.vue.list_player("Liste par odre d'inscription", ordered)

            case 'games':
                ordered = sorted(file_players, key=lambda x: x['Point'])
                self.vue.list_player("Liste par point(s)", ordered)
                # , reverse=True
