from tkinter import *
from tkinter import font, Entry
from tkinter import ttk

from core import core
from rotate import rotation
from database import data_tournament as data
from models import mdl_tournament as model
from views import view_tournaments as view


class TournamentsCtrl(core.Core):
    def __init__(self, data_transfer=None):
        super().__init__()

        print('TournamentsCtrl data_transfer', data_transfer)

        self.new_all_players: list = []

        self.vue = view.TournamentsViews(self)
        self.vue.new_menu()
        self.vue.menu_choice()

        if data_transfer:
            self.new_player = data_transfer
            self.new_all_players.append(self.new_player)
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
        number_turns = plr_data['numberRound'].get()

        players = plr_data['players']
        ctrl_number_players = len(players)

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
        if number_turns:
            errors_dict['ctrl_round'] = self.number_verif("numberRound", number_turns)
        if day and month and year:
            errors_dict['ctrl_date'] = self.date_verif(year, month, day)
        if not ctrl_number_players % 2 == 0:
            errors_dict['ctrl_nbr_plrs'] = f"Vous devez sélectionner un nombre pair de joueurs"

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(mst=new_frame, family=None, size=9, weight="normal", slant="roman", underline=False, bg="#FEF9E7",
                                 name=er[0], fg="red", pady=None, text=er[1])

        elif name and address and day and month and year:
            birth = year + '-' + month + '-' + day
            # instance tournoi
            dt_tour = model.TournamentMdl(name=name, address=address, birth=birth, number_turns=number_turns,
                                          players=players).instance_tournament()

            self.new_tournoi = {'Nom': dt_tour[0], 'Adresse': dt_tour[1], 'Date': dt_tour[2],
                                'number_turns': dt_tour[3], 'Joueurs': dt_tour[4],
                                'Round': dt_tour[5]}

            self.vue.detail_tournament(self.new_tournoi)
            self.new_tour_choice_view()
        else:
            pass

    def tournament_ctrl_player(self, new_frame, plr_data) -> False:
        errors_dict = {}
        last_name = plr_data['last_name'].get()
        first_name = plr_data['first_name'].get()
        identity = plr_data['identity'].get()

        if last_name:
            errors_dict['ctrl_lst_1'] = self.long_string_verif("Le Nom", 2, 40, last_name)
            errors_dict['ctrl_lst_2'] = self.string_verif("Le Nom", last_name)
        if first_name:
            errors_dict['ctrl_fst_1'] = self.long_string_verif("Le Prénom", 2, 40, first_name)
            errors_dict['ctrl_fst_2'] = self.string_verif("Le Prénom", first_name)
        if identity:
            errors_dict['identity'] = self.identity_verif(identity)

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(mst=new_frame, family=None, size=9, weight="normal", slant="roman", underline=False,
                                 bg="#FEF9E7", name=er[0], fg="red", pady=None, text=er[1])

        elif identity and last_name and first_name:

            rst1 = self.searching(search_type="compare", last_name=last_name, first_name=first_name, identity=identity)
            rst2 = self.searching(search_type="searching", identity=identity)

            if len(rst1) > 0:
                self.vue.message(mst=new_frame, family=None, size=10, weight="normal", slant="roman", underline=False,
                                 bg="#FEF9E7", name="error1", fg="red", pady=10,
                                 text="il semble que ce joueur est déja enregistré")
            elif len(rst2) > 0:
                self.vue.message(mst=new_frame, family=None, size=10, weight="normal", slant="roman", underline=False,
                                 bg="#FEF9E7", name="error1", fg="red", pady=10,
                                 text="Ce numéro d'identité éxiste déja !")
            else:
                id_last = identity[:2].upper()
                id_first = identity[2:]
                identity = id_last + id_first
                last_name = str(last_name).capitalize()
                first_name = str(first_name).capitalize()

                return identity, last_name, first_name
        else:
            pass

    def new_tour_choice_view(self):
        tr = self.new_tournoi
        print(f"new_tour_choice_view =>")
        print(tr['Nom'])
        print(tr['Adresse'])
        print(tr['Date'])
        print('JOUEURS =>', tr['Joueurs'])
        print('ROUND =>', tr['number_turns'])
        print('Match =>', tr['Round'])


