import json
import os


class TournamentData:

    def __init__(self, new_data: object | None = None):

        self.data: dict = {}

        if new_data:
            self.data = {
                'id': int(1),
                'Nom': str(new_data.name).capitalize(),
                'Adresse': str(new_data.address),
                'Date': str(new_data.date),
                'Nombre de manche': int(new_data.number_turns),
                'Joueurs': new_data.players,
                'Rounds': new_data.rounds
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


