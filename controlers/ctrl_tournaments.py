from tkinter import *
from tkinter import font, Entry
from tkinter import ttk

from core import core
from rotate import rotation
from database import data_tournament as data
from models import mdl_tournament as model
from views import view_tournaments as view


def searching(**kwargs: any) -> False:
    """
        Recherchée correspondance
        si le nom de tournoi
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


class TournamentsCtrl(core.Core):
    def __init__(self, data_transfer=None):
        super().__init__()

        print('TournamentsCtrl', data_transfer)

        self.vue = view.TournamentsViews(self)

        self.vue.new_menu()
        self.vue.menu_choice()

        if data_transfer:
            self.new_player = data_transfer
            self.vue.new_tournament()

    def result_menu(self, result: str | None = None):
        match result:
            case 'create':
                self.vue.new_tournament()

            case 'search':
                self.vue.search_tournament()

            case _:
                pass

    def tournament_ctrl(self, new_frame, plr_data):
        errors_dict = {}
        name = plr_data['name'].get()
        address = plr_data['address'].get()
        day = plr_data['birth_start']['day'].get()
        month = plr_data['birth_start']['month'].get()
        year = plr_data['birth_start']['year'].get()
        tour_type = plr_data['tour_type']

        if name:
            errors_dict['ctrl_lst_1'] = self.long_string_verif("Le Nom", 2, 40, name)
        if address:
            errors_dict['ctrl_fst_1'] = self.long_string_verif("L'adresse'", 2, 100, address)
        if day:
            errors_dict['ctrl_day'] = self.number_verif("Le jour", day)
        if month:
            errors_dict['ctrl_month'] = self.number_verif("Le mois", month)
        if year:
            errors_dict['ctrl_year'] = self.number_verif("L'année tournoi", year)

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name=er[0], fg="red", pady=None, text=er[1])

        elif name and address and day and month and year:
            birth = year + '-' + month + '-' + day

            # instance tournoi
            dt_tour = model.TournamentMdl(name=name, address=address, birth=birth, tour_type=tour_type).instance_tournament()
            self.new_tour = {'Nom': dt_tour[0], 'Adresse': dt_tour[1], 'Date': dt_tour[2], 'Joueurs': dt_tour[3], 'Round1': dt_tour[4]}
            self.new_tour_choice_view()
        else:
            pass

    def new_tour_choice_view(self):
        tr = self.new_tour
        print(f"new_tour_choice_view =>")
        print(tr['Nom'])
        print(tr['Adresse'])
        print(tr['Date'])
        print('JOUEURS =>', tr['Joueurs'])
        print('ROUND1 =>', tr['Round1'])


