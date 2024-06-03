from tkinter import *
from tkinter import font, Entry
from tkinter import ttk

from core import core
from core import french_date as date_fr
from rotate import rotation
from database import data_tournaments as data

from models.mdl_tournament import TournamentMdl
from models.mdl_round import RoundMdl
from models.mdl_player import PlayersMdl

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
            birth = date_fr.FrenchDate().new_format_fr(year, month, day)

            self.tournament_treatment('create', new_frame, None, name, address, birth, number_turns,
                                      None, players)
            self.new_all_players.clear()
        else:
            pass

    def tournament_ctrl_player(self, new_frame, data_player) -> False:
        errors_dict = {}
        last_name = data_player['last_name'].get()
        first_name = data_player['first_name'].get()
        identity = data_player['identity'].get()
        point = data_player['point'].get()

        if last_name:
            errors_dict['ctrl_lst_1'] = self.long_string_verif("Le Nom", 2, 40, last_name)
        if first_name:
            errors_dict['ctrl_fst_1'] = self.long_string_verif("Le Prénom", 2, 40, first_name)
        if identity:
            errors_dict['identity'] = self.identity_verif(identity)
        if point:
            errors_dict['ctrl_point'] = self.number_float_verif("Le Point", point)
            if not errors_dict['ctrl_point']:
                point = float(point)

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

                return identity, last_name, first_name, point
        else:
            pass

    def tournament_treatment(self, treatment, new_frame, id_tour, name, address, birth, number_turns, rounds, players):
        # instance tournoi
        self.new_tournament = TournamentMdl(id_tour=id_tour, name=name, address=address, birth=birth,
                                            number_turns=number_turns, rounds=rounds, players=players)
        if treatment == 'create':
            # insertion json
            if data.TournamentData(self.new_tournament):
                self.vue.detail_tournament(self.new_tournament)
            else:
                self.vue.message(mst=new_frame, family=None, size=12, weight="bold", slant="roman", underline=False,
                                 bg="#FEF9E7", name="error", fg="red", pady=10,
                                 text="Une erreur est survenue, veuillez réessayer.")

        elif treatment == 'data':
            self.vue.detail_tournament(self.new_tournament)

    def tournament_lists(self, list_type):
        tournaments = self.tournaments_list()
        title = None
        ordered = None
        if len(tournaments) > 0:
            if list_type == 'first':
                ordered = sorted(tournaments, key=lambda x: x['Date'])
                title = 'Liste par dates croissantes'
            elif list_type == 'last':
                ordered = sorted(tournaments, key=lambda x: x['Date'], reverse=True)
                title = 'Liste par dates décroissantes'

            if ordered:
                self.vue.list_tournament(title, ordered)
        else:
            pass

    def instance_player(self, _players_list=None):

        data_players: list = []
        if not _players_list:
            file_players = self.players_list()
            _players_list = sorted(file_players, key=lambda x: x['last_name'])

        for player in _players_list:
            instance = PlayersMdl(identity=player['identity'], last_name=player['last_name'],
                                  first_name=player['first_name'], point=player['point'])
            data_players.append(instance)

        return data_players

    def update_score(self, new_scores):
        if data.TournamentData().update_scores(new_scores):
            pass

    def update_date(self, data_date):
        new_date = data.TournamentData().update_date(data_date)
        return new_date

    def round_treatment(self, id_tournament):

        _tour = None

        tournaments = self.tournaments_list()
        for _tr in tournaments:
            if _tr['id'] == id_tournament:
                _tour = _tr
                break

        if _tour:

            _number_turn = int(_tour['Nombre de manche'])
            _players: list = _tour['Joueurs']
            _rounds: list = _tour['Rounds']

            number_player = len(_players)
            number_round = len(_rounds)

            # date de fin round en cours
            current_round: dict = _rounds[-1]
            id_crt_round = current_round['round']
            current_round['finish'] = date_fr.FrenchDate().date_hour_fr

            # Récupération des joueurs du round en cours
            match_players = []
            for _match in current_round['matchs']:
                match_players.append(_match[0])
                match_players.append(_match[1])

            # récupération de tous les matchs du tournoi
            matchs_list = []
            for _rds in _rounds:
                for match_ in _rds['matchs']:
                    matchs_list.append([[match_[0][0], match_[0][1]], [match_[1][0], match_[1][1]]])

            # Mise à jour des points du joueur / Création liste pour traitement nouveau round
            disorderly_list = []
            for player in _players:
                player_name = None

                for ch_plr in match_players:
                    if player['identity'] == ch_plr[0]:
                        player_name = ch_plr[1]
                        player['point'] = float(player['point'] + ch_plr[2])

                disorderly_list.append([player['identity'], player_name, player['point']])

            # Liste des joueurs classés par nombre de points
            players_list = sorted(disorderly_list, key=lambda x: x[2], reverse=True)
            for rm in players_list:
                rm.remove(rm[2])

            def restart():
                match_count = int(number_player / 2)
                new_matchs_list = []

                for x in range(match_count):
                    xx = x + 1
                    player1 = players_list[x]
                    player2 = players_list[xx]
                    m_players: tuple = (player1, player2)
                    new_matchs_list.append(m_players)

                    for rm_player in match_players:
                        players_list.remove(rm_player)
                _rounds.append({"round": int(id_round + 1), "start": '', "finish": '', "matchs": new_matchs_list})
                # Mise à jour du tournoi

            def new_round():
                # Copie liste des joueurs classés par nombre de points
                copy_list = players_list.copy()

                # Créer une liste comprenant les matchs
                new_matchs_list = []
                for _player in players_list:
                    id_player = _player[0]

                    # Joueur déja sélectionné
                    if _player not in copy_list:
                        continue
                    copy_list.remove(_player)

                    # Copie liste des joueurs restant pour match
                    confronted = copy_list.copy()

                    # tous les matchs de chaque round du tournoi
                    for _mts in matchs_list:

                        plr1 = _mts[0]
                        plr2 = _mts[1]

                        if id_player == plr1[0] and plr2 in confronted:
                            confronted.remove(plr2)

                        if id_player == plr2[0] and plr1 in confronted:
                            confronted.remove(plr1)

                    # s'il reste des joueurs
                    if len(confronted) > 0:
                        new_matchs_list.append((_player, confronted[0]))
                        copy_list.remove(confronted[0])

                _rounds.append({"round": int(id_crt_round + 1), "start": '', "finish": '', "matchs": new_matchs_list})
                """rd_ = RoundMdl(int(id_crt_round + 1), "", "", new_matchs_list)
                _rounds.append(rd_)"""
                # Mise à jour du tournoi
                for ii in _tour['Rounds']:
                    print(f"{ii} \n")

            if _number_turn == number_round:
                # Fin des tours, mise à jour du tournoi et fin
                print('Application data')

            else:
                # nombre de fois qu'un joueur en rencontre un autre
                adversary = int(number_player - 1)
                reste = _number_turn - number_round

                # tout le monde s'est rencontrés
                if number_round == adversary:
                    restart()

                # tout le monde s'est rencontrés encore
                elif reste == adversary:
                    restart()

                else:
                    new_round()










            """ 
                # nombre de fois qu'un joueur en rencontre un autre
                adversary = int(number_player - 1)
                reste = _number_turn - number_round

                # tout le monde s'est rencontrés au moins 1 fois
                if number_round == adversary:
                    restart()

                # tout le monde s'est rencontrés au moins 2 fois
                if reste == adversary:
                    restart()

                # si moins de deux rencontres restes avec les mêmes joueurs
                if reste < adversary:
                    new_round()

                # si plus de deux rencontres restes avec les mêmes joueurs
                if reste > adversary:
                    pass

            """