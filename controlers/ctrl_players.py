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

        type_search = 1
        last_name = None
        first_name = None
        birth = None

        if 'last_name' in kwargs:
            last_name = kwargs['last_name'].strip().replace(' ', '').lower()
        if 'first_name' in kwargs:
            first_name = kwargs['first_name'].strip().replace(' ', '').lower()
        if 'birth' in kwargs:
            birth = kwargs['birth']

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

            if kwargs['search_type'] == 'compare':
                type_search = 3
            if len(data_user) == type_search:
                return player


class PlayersCtrl(core.Core):
    def __init__(self, data_transfer=None):
        super().__init__()

        self.vue = view.PlayersViews(self)

        self.vue.new_menu()
        self.vue.menu_choice()

    def result_menu(self, result: str | None = None):
        match result:
            case 'create':
                self.vue.new_player()

            case 'search':
                self.vue.search_player()

            case _:
                pass

    ###

    def new_player_ctrl(self, new_frame, plr_data):
        errors_dict = {}
        last_name = plr_data['last_name'].get()
        first_name = plr_data['first_name'].get()
        day = plr_data['birth']['day'].get()
        month = plr_data['birth']['month'].get()
        year = plr_data['birth']['year'].get()

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

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name=er[0], fg="red", pady=None, text=er[1])

        elif last_name and first_name and day and month and year:
            birth = year + '-' + month + '-' + day
            result = searching(search_type="compare", last_name=last_name, first_name=first_name, birth=birth)
            if result:
                self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name="error1", fg="red", pady=10, text="il semble que ce joueur est déja enregistré")
            else:
                # instance d'un joueur
                dt_player = model.PlayersMdl(last_name=last_name, first_name=first_name, birth=birth).instance_player()
                self.new_player = {'Nom': dt_player[0], 'Prénom': dt_player[1], 'Date de naissance': dt_player[2]}
                self.new_player_choice_view()
        else:
            pass

    def new_player_choice_view(self):
        self.vue.insert_player(self.new_player)

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

    def search_ctrl(self, new_frame, name=None):
        if name:
            name = name['last_name'].get()
            errors_dict: dict = {'ctrl_1': self.long_string_verif("Le Nom", 2, 50, name),
                                 'ctrl_2': self.string_verif("Le Nom", name)}
            self.destroy_error(new_frame, 1)

            ctrl_errors = self.create_error(errors_dict)
            if len(ctrl_errors) > 0:
                for er in ctrl_errors:
                    self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                     name=er[0], fg="red", pady=None, text=er[1])
            else:
                result = searching(search_type="searching", last_name=name)
                if result:
                    self.new_player = result
                    self.search_choice_view(result)
                else:
                    self.vue.message(family=None, size=10, weight="normal", slant="roman", underline=False, bg="#FEF9E7"
                                     , name="error1", fg="red", pady=10, text="Ce joueur n'éxiste pas")
        else:
            pass

    def search_choice_view(self, result):
        self.vue.matching_player(result)

    def search_choice(self, result: str | None = None):
        match result:
            case 'tournament1':
                self.create_new_tournament()

            case 'tournament2':
                pass

            case _:
                pass

    def create_new_tournament(self):
        self.menu.destroy()
        self.frame.destroy()
        self.quit()

        from controlers import ctrl_tournaments
        ctrl_tournaments.TournamentsCtrl(self.new_player)

        def suite():
            from controlers import ctrl_tournaments
            ctrl_tournaments.TournamentsCtrl(self.new_player)

            """
            if self.quit():
                from controlers import ctrl_tournaments
                ctrl_tournaments.TournamentsCtrl()
            """

            """
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
