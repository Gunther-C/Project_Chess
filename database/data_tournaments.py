import json
import os
from core import french_date as date_fr


class TournamentData:

    def __init__(self, new_data: object | None = None):

        self.data: dict = {}

        if new_data:

            _rd = new_data.rounds[0]
            match_list = []
            player_list = []

            for player in new_data.players:
                player_list.append({"identity": player.identity, "last_name": player.last_name,
                                    "first_name": player.first_name, "point": 0.0})

            for match in _rd.matchs_list:
                match_list.append(([match.identity_plr1, match.name_plr1, 0.0],
                                   [match.identity_plr2, match.name_plr2, 0.0]))
            round_1: list = [{"round": _rd.id_round, "start": '', "finish": '', "matchs": match_list}]

            self.data = {
                'id': int(1),
                'Nom': str(new_data.name).capitalize(),
                'Adresse': str(new_data.address).capitalize(),
                'Date': str(new_data.date),
                'Manches': int(new_data.number_turns),
                'Joueurs': player_list,
                'Rounds': round_1,
                'Commentaires': str(new_data.comment)
            }
            self.insert_tournament()

    def insert_tournament(self) -> False:

        current_file = []
        if os.path.isfile("database/data_tournaments.json"):
            current_file = self.load_tournament_file()
            new_id = int(current_file[-1]['id']) + 1
            self.data['id'] = new_id
            current_file.append(self.data)
        else:
            current_file.append(self.data)

        try:
            with open("database/data_tournaments.json", "w", encoding="utf-8-sig", newline="") as file:
                try:
                    json.dump(current_file, file, indent=4)
                    return self.data

                except json.JSONEncodeError:
                    """print(f"Erreur lors de l'écriture des données JSON : {e}")"""
                    return False

        except IOError:
            """print("Erreur lors de l'ouverture du fichier :", er)"""
            return False

        except UnicodeEncodeError:
            """print("Erreur D'encodage :", err)"""
            return False

    @staticmethod
    def update_scores(new_scores) -> False:
        nw_sc = new_scores
        try:
            with open("database/data_tournaments.json", "r+", encoding="utf-8-sig", newline="") as file:

                try:
                    new_file = json.load(file)
                    for tournament in new_file:
                        # tournoi
                        if tournament['id'] == nw_sc[0]:

                            # liste des rounds
                            rounds = tournament['Rounds']
                            rd = rounds[-1]

                            # liste des matchs
                            matchs = rd['matchs']
                            match = matchs[int(nw_sc[1])]

                            player_1 = match[0]
                            player_2 = match[1]

                            if player_1[0] == nw_sc[2][0][0]:
                                player_1[2] = nw_sc[2][0][1]
                                player_2[2] = nw_sc[2][1][1]

                            elif player_2[0] == nw_sc[2][0][0]:
                                player_2[2] = nw_sc[2][0][1]
                                player_1[2] = nw_sc[2][1][1]

                    file.seek(0)
                    json.dump(new_file, file, indent=4)
                    return True
                except json.JSONDecodeError as e:
                    return False

        except IOError:
            return False

        except UnicodeEncodeError:
            return False

    @staticmethod
    def update_date(data_date) -> False:

        to_day = date_fr.FrenchDate().date_hour_fr
        try:
            with open("database/data_tournaments.json", "r+", encoding="utf-8-sig", newline="") as file:

                try:
                    new_file = json.load(file)

                    for tournament in new_file:
                        # tournoi
                        if tournament['id'] == data_date[1]:
                            # liste des rounds
                            rounds = tournament['Rounds']
                            rd = rounds[-1]

                            if data_date[0] == 'start' and len(rd['start']) < 1:
                                rd['start'] = to_day

                            elif data_date[0] == 'finish' and len(rd['finish']) < 1:
                                rd['finish'] = to_day

                    file.seek(0)

                    json.dump(new_file, file, indent=4)

                    return to_day

                except json.JSONDecodeError:
                    return False

        except IOError:
            return False

        except UnicodeEncodeError:
            return False

    @staticmethod
    def update_comment(new_tournament):
        try:
            with open("database/data_tournaments.json", "r", encoding="utf-8-sig", newline="") as file:

                try:
                    new_file = json.load(file)
                    for tournament in new_file:
                        if tournament['id'] == new_tournament.id_tour:
                            tournament['Commentaires'] = new_tournament.comment
                except json.JSONDecodeError as e:
                    print(f"Erreur lors de l'écriture des données JSON : {e}")

            with open("database/data_tournaments.json", "w", encoding="utf-8-sig", newline="") as fl:

                try:
                    json.dump(new_file, fl, indent=4)
                except json.JSONEncodeError as e:
                    print(f"Erreur lors de l'écriture des données JSON : {e}")

        except IOError as er:
            print("Erreur lors de l'ouverture du fichier :", er)
            print("En cas de première insertion, une erreur (no such file) peut apparaître.")

        except UnicodeEncodeError as err:
            print("Erreur D'encodage :", err)

    @staticmethod
    def treatment_round(new_tournament):
        try:
            with open("database/data_tournaments.json", "r+", encoding="utf-8-sig", newline="") as file:

                try:
                    new_file = json.load(file)
                    # tournoi
                    for tournament in new_file:
                        if tournament['id'] == new_tournament['id']:
                            tournament['Joueurs'] = new_tournament['players']
                            tournament['Rounds'] = new_tournament['rounds']
                            break

                    file.seek(0)
                    json.dump(new_file, file, indent=4)

                except json.JSONDecodeError as e:
                    print(f"Erreur lors de l'écriture des données JSON : {e}")

        except IOError as er:
            print("Erreur lors de l'ouverture du fichier :", er)
            print("En cas de première insertion, une erreur (no such file) peut apparaître.")

        except UnicodeEncodeError as err:
            print("Erreur D'encodage :", err)

    @staticmethod
    def load_tournament_file():
        try:
            with open("database/data_tournaments.json", encoding="utf-8-sig", newline="") as file:

                try:
                    new_file = json.load(file)
                    return new_file

                except json.JSONDecodeError as e:
                    print(f"Erreur lors de la lecture des données JSON : {e}")

        except IOError as er:
            print("Erreur lors de l'ouverture du fichier :", er)
            print("En cas de première insertion, une erreur (no such file) peut apparaître.")

        except UnicodeEncodeError as err:
            print("Erreur D'encodage :", err)
