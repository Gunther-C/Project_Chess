from tkinter import *
from tkinter import font, Entry
from tkinter import ttk
import time
import subprocess

from core import core
from database import data_players as data
from models import mdl_players as model
from views import view_players as view


def players_list():
    # fichier json des joueurs
    file_players = data.PlayersData().load_players_file()
    if file_players:
        return file_players


def searching(**kwargs: any) -> False:
    """
        Recherchée correspondance
        si le joueur est déja dans la bdd à l'inscription
        recherche si un joueur éxiste retourne ses infos en cas de success
    """
    file_players = players_list()
    if file_players:

        multi_player = []
        type_search = 1
        last_name = None
        first_name = None
        birth = None
        identity = None
        if 'last_name' in kwargs:
            last_name = kwargs['last_name'].strip().replace(' ', '').lower()
        if 'first_name' in kwargs:
            first_name = kwargs['first_name'].strip().replace(' ', '').lower()
        if 'birth' in kwargs:
            birth = kwargs['birth']
        if 'identity' in kwargs:
            identity = kwargs['identity']

        for player in file_players:

            data_user = []
            for keys, values in player.items():
                if keys == 'Nom':
                    values = values.strip().replace(' ', '').lower()
                    if last_name == values:
                        data_user.append(values)

                if keys == 'Prénom':
                    values = values.strip().replace(' ', '').lower()
                    if first_name == values:
                        data_user.append(values)

                if keys == 'Date de naissance':
                    if birth == values:
                        data_user.append(values)

                if keys == 'Identité':
                    if identity == values:
                        data_user.append(values)

            if kwargs['search_type'] == 'compare':
                type_search = 3

            if len(data_user) == type_search:
                multi_player.append(player)

        return multi_player

class PlayersCtrl(core.Core):
    def __init__(self, data_transfer=None):
        super().__init__()

        self.vue = view.PlayersViews(self)

        self.vue.new_menu()
        self.vue.menu_choice()

    def new_player_ctrl(self, new_frame, plr_data):
        errors_dict = {}
        last_name = plr_data['last_name'].get()
        first_name = plr_data['first_name'].get()
        day = plr_data['birth']['day'].get()
        month = plr_data['birth']['month'].get()
        year = plr_data['birth']['year'].get()
        identity = plr_data['identity'].get()

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

        if identity:
            errors_dict['identity'] = self.identity_verif(identity)

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name=er[0], fg="red", pady=None, text=er[1])

        elif identity and last_name and first_name and day and month and year:
            birth = year + '-' + month + '-' + day

            result = searching(search_type="compare", last_name=last_name, first_name=first_name, birth=birth)
            result2 = searching(search_type="searching", identity=identity)

            if len(result) > 0:
                self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name="error1", fg="red", pady=10, text="il semble que ce joueur est déja enregistré")

            elif len(result2) > 0:
                self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name="error1", fg="red", pady=10, text="Ce numéro d'identité éxiste déja !")

            else:
                # instance d'un joueur
                data_pl = model.PlayersMdl(
                    identity=identity,
                    last_name=last_name,
                    first_name=first_name,
                    birth=birth
                ).instance_player()

                self.new_player = {
                    'Identité': data_pl[0],
                    'Nom': data_pl[1],
                    'Prénom': data_pl[2],
                    'Date de naissance': data_pl[3]
                }
                self.vue.insert_player(self.new_player)
        else:
            pass

    def new_player_choice(self, result, new_frame):
        match result:
            case 'list':
                self.new_player_save(new_frame)

            case 'tournament1':
                self.create_new_tournament()

            case 'tournament2':
                pass

            case _:
                pass

    def new_player_save(self, new_frame):
        if data.PlayersData(self.new_player):
            self.vue.message(family=None, size=12, weight="bold", slant="roman", underline=False, bg="#FEF9E7",
                             name="success", fg="blue", pady=10, text="Joueur inséré")
        else:
            self.vue.message(family=None, size=12, weight="bold", slant="roman", underline=False,
                             bg="#FEF9E7", name="error", fg="red", pady=10,
                             text="Une erreur est survenue, veuillez réessayer.")
        self.after(7000, new_frame.destroy)

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

                new_search = searching(search_type="searching", last_name=last_name)

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
                new_search = searching(search_type="searching", identity=identity)
                if len(new_search) > 0:
                    self.vue.matching_player(new_search[0])

                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                                     bg="#FEF9E7", name="error1", fg="red", pady=10, text="Ce joueur n'éxiste pas")
        else:
            pass


    def search_choice(self, result: str, data_player: dict):

        if len(data_player) == 4:
            print(data_player)
            data_pl = model.PlayersMdl(
                identity=data_player['Identité'],
                last_name=data_player['Nom'],
                first_name=data_player['Prénom'],
                birth=data_player['Date de naissance']
            ).instance_player()

            self.new_player = {
                'Identité': data_pl[0],
                'Nom': data_pl[1],
                'Prénom': data_pl[2],
                'Date de naissance': data_pl[3]
            }

            match result:
                case 'tournament1':
                    self.create_new_tournament()

                case 'tournament2':
                    pass

                case _:
                    pass
        else:
            self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False,
                             bg="#FEF9E7", name="error1", fg="red", pady=10, text="La création du joueur à échoué")

    def create_new_tournament(self):

        print('create_new_tournament', self.new_player)

        """
        if self.quit():
            from controlers import ctrl_tournaments
            ctrl_tournaments.TournamentsCtrl(self.new_player)

        self.menu.destroy()
        self.frame.destroy()
        self.new_self.destroy()
        self.quit()"""
        """
        
        from controlers import ctrl_tournaments
        ctrl_tournaments.TournamentsCtrl(self.new_player)
        """

        # exec(open(f"controlers/ctrl_tournaments/TournamentsCtrl({self.new_player})").read())
        # subprocess.run(["python", f"controlers/ctrl_tournaments/TournamentsCtrl({self.new_player})"])
        """from controlers import ctrl_tournaments
        time.sleep(2)
        ctrl_tournaments.TournamentsCtrl(self.new_player)"""
        # core.start_tournament(self.new_player)

    def recover_list(self, type_list=None):

        file_players = players_list()

        match type_list:
            case 'names':
                liste = []
                for x in range(10):
                    for player in file_players:
                        liste.append(player)
                ordered = sorted(liste, key=lambda x: x['Nom'])
                # ordered = sorted(file_players, key=lambda x: x['Nom'])

                self.vue.list_player('Liste par ordre alphabétique', ordered)

            case 'tournaments':
                ordered = sorted(file_players, key=lambda x: x['Tournoi gagné'], reverse=True)
                self.vue.list_player('Liste par tournoi(s) gagné(s)', ordered)

            case 'games':
                ordered = sorted(file_players, key=lambda x: x['partie gagnée'], reverse=True)
                self.vue.list_player('Liste par partie(s) gagnée(s)', ordered)


"""if __name__ == '__main__':
    window = PlayersCtrl()
    window.mainloop()"""

window = PlayersCtrl()
window.mainloop()
