import json
import os


class TournamentData:

    def __init__(self, new_data: object):

        self.data: dict = {}

        if new_data and new_data[0] and new_data[1] and new_data[2] and new_data[3] and new_data[4] and new_data[5]:

            self.data = {
                'id': int(1),
                'Nom': str(data[0]).capitalize(),
                'Adresse': str(data[1]),
                'Date': str(data[2]),
                'Nombre de manche': int(data[3]),
                'Joueurs': data[4],
                'Round': data[5]
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
                    json.dump(current_file, file)
                    return True
                except json.JSONEncodeError as e:
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


