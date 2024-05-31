import json
import os
from core import french_date as date_fr


class TournamentData:

    def __init__(self, new_data: object | None = None):

        self.data: dict = {}

        if new_data:

            player_list = []
            for player in new_data.players:
                player_list.append({"identity": player.identity, "last_name": player.last_name,
                                    "first_name": player.first_name, "point": player.point})

            _rd = new_data.rounds[0]
            match_list = []
            for match in _rd.matchs_list:
                match_list.append(([match.identity_plr1, match.name_plr1], [match.identity_plr2, match.name_plr2]))
            round_1: list = [{"round": _rd.id_round, "start": '', "finish": '', "matchs": match_list}]

            self.data = {
                'id': int(1),
                'Nom': str(new_data.name).capitalize(),
                'Adresse': str(new_data.address).capitalize(),
                'Date': str(new_data.date),
                'Nombre de manche': int(new_data.number_turns),
                'Joueurs': player_list,
                'Rounds': round_1
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
                    return True
                except json.JSONEncodeError as e:
                    print(f"Erreur lors de l'écriture des données JSON : {e}")

        except IOError as er:
            print("Erreur lors de l'ouverture du fichier :", er)
            print("En cas de première insertion, une erreur (no such file) peut apparaître.")

        except UnicodeEncodeError as err:
            print("Erreur D'encodage :", err)

    def update_scores(self, new_scores):
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
                                if len(player_1) > 2:
                                    player_1.remove(player_1[2])
                                    player_2.remove(player_2[2])
                                player_1.append(nw_sc[2][0][1])
                                player_2.append(nw_sc[2][1][1])

                            if player_2[0] == nw_sc[2][0][0]:
                                if len(player_2) > 2:
                                    player_2.remove(player_2[2])
                                    player_1.remove(player_1[2])
                                player_2.append(nw_sc[2][0][1])
                                player_1.append(nw_sc[2][1][1])

                    file.seek(0)

                    json.dump(new_file, file, indent=4)

                except json.JSONDecodeError as e:
                    print(f"Erreur lors de l'écriture des données JSON : {e}")


        except IOError as er:
            print("Erreur lors de l'ouverture du fichier :", er)
            print("En cas de première insertion, une erreur (no such file) peut apparaître.")

        except UnicodeEncodeError as err:
            print("Erreur D'encodage :", err)

    def update_date(self, data_date):

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

                    file.seek(0)

                    json.dump(new_file, file, indent=4)

                    return to_day

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









# with open("packageCsv/essai.csv") as file:
# with open("packageCsv/essai.csv", mode="r") as file: r __lire
# with open("packageCsv/essai.csv", mode="r+") as file: r+ __lire,écrire(sans écraser)
# with open("packageCsv/essai.csv", mode="w") as file: w __écrire(écraser)
# with open("packageCsv/essai.csv", mode="a") as file: a __continuer d'écrire
# text_csv = csv.reader
# text_csv = csv.reader(file, delimiter=",")
# text_csv = csv.DictReader(file)
# text_csv = csv.writer(file, delimiter=',')