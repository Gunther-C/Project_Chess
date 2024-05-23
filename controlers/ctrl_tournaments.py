from tkinter import *
from tkinter import font, Entry
from tkinter import ttk

from core import core
from rotate import rotation
from database import data_tournaments as data
from models import mdl_tournament as model
from views import view_tournaments as view


class TournamentsCtrl(core.Core):
    def __init__(self, new_player=None):
        super().__init__()

        print('TournamentsCtrl data_player', new_player)

        self.new_all_players: list = []

        self.vue = view.TournamentsViews(self)
        self.vue.new_menu()
        self.vue.menu_choice()

        if new_player:
            self.new_all_players.append(new_player)
            self.vue.new_tournament()

    def result_menu(self, result: str | None = None):
        match result:
            case 'create':
                self.vue.new_tournament()
            case 'search':
                self.vue.search_tournament()
            case _:
                pass

    def tournament_ctrl(self, new_frame, data_tournament):

        errors_dict = {}
        name = data_tournament['name'].get()
        address = data_tournament['address'].get()
        day = data_tournament['birth_start']['day'].get()
        month = data_tournament['birth_start']['month'].get()
        year = data_tournament['birth_start']['year'].get()
        number_turns = data_tournament['numberRound'].get()

        players = data_tournament['players']
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
            if not errors_dict['ctrl_day'] and not errors_dict['ctrl_month'] and not errors_dict['ctrl_year']:
                errors_dict['ctrl_date'] = self.date_verif(year, month, day)
        if not ctrl_number_players % 2 == 0:
            errors_dict['ctrl_nbr_plrs'] = f"Vous devez sélectionner un nombre pair de joueurs"

        self.destroy_error(new_frame, 1)

        ctrl_errors = self.create_error(errors_dict)
        if len(ctrl_errors) > 0:
            for er in ctrl_errors:
                self.vue.message(mst=new_frame, family=None, size=9, weight="normal", slant="roman", underline=False,
                                 bg="#FEF9E7", name=er[0], fg="red", pady=None, text=er[1])

        elif name and address and day and month and year:
            birth = year + '-' + month + '-' + day
            self.tournament_treatment('create', new_frame, None, name, address, birth, number_turns,
                                      None, players)
        else:
            pass

    def tournament_ctrl_player(self, new_frame, data_player) -> False:
        errors_dict = {}
        last_name = data_player['last_name'].get()
        first_name = data_player['first_name'].get()
        identity = data_player['identity'].get()

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

    def tournament_treatment(self, treatment, new_frame, id_tour, name, address, birth, number_turns, rounds, players):
        # instance tournoi
        self.new_tournament = model.TournamentMdl(id_tour=id_tour, name=name, address=address, birth=birth,
                                                  number_turns=number_turns, rounds=rounds, players=players)
        if treatment == 'create':

            if data.TournamentData(self.new_tournament):
                self.vue.detail_tournament(self.new_tournament)
            else:
                self.vue.message(mst=new_frame, family=None, size=12, weight="bold", slant="roman", underline=False,
                                 bg="#FEF9E7", name="error", fg="red", pady=10,
                                 text="Une erreur est survenue, veuillez réessayer.")

        elif treatment == 'data':

            self.vue.detail_tournament(self.new_tournament)




        print(f"new_tour_choice_view =>")
        print('NOM =>', self.new_tournament.name)
        print('ADRESSE =>', self.new_tournament.address)
        print('DATE =>', self.new_tournament.date)
        print('JOUEURS =>', self.new_tournament.players)
        print('ROUND =>', self.new_tournament.number_turns)
        print('Match =>', self.new_tournament.rounds)

    def tournament_lists(self, list_type):
        tournaments = self.tournaments_list()
        if len(tournaments) > 0:
            if list_type == 'first':
                ordered = sorted(tournaments, key=lambda x: x['Date'])
                self.vue.list_tournament('Liste par dates croissantes', ordered)
            elif list_type == 'last':
                ordered = sorted(tournaments, key=lambda x: x['Date'], reverse=True)
                self.vue.list_tournament('Liste par dates décroissantes', ordered)
        else:
            pass

    def tournament_view(self, instance_type, new_frame, name, address, birth, number_turns, rounds, players):


        if not rounds:

            if data.TournamentData(self.new_tournament):
                self.vue.detail_tournament(self.new_tournament)
            else:
                self.vue.message(mst=new_frame, family=None, size=12, weight="bold", slant="roman", underline=False,
                                 bg="#FEF9E7", name="error", fg="red", pady=10,
                                 text="Une erreur est survenue, veuillez réessayer.")

        self.vue.detail_tournament(self.new_tournament)

