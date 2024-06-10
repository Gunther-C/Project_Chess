import json
import os


class PlayersData:

    def __init__(self, player: object | None = None):

        self.data: dict = {}

        if player and player.identity and player.last_name and player.first_name and player.birth and player.point:

            _point = 0.0
            if player.point and type(player.point) is float:
                _point = player.point

            self.data = {
                'id': int(1),
                'identity': str(player.identity),
                'last_name': str(player.last_name).capitalize(),
                'first_name': str(player.first_name).capitalize(),
                'birth': str(player.birth),
                'point': float(_point),
            }
            self.insert_player()

    def insert_player(self) -> False:

        current_file = []

        if os.path.isfile("database/data_players.json"):
            current_file = self.load_players_file()
            new_id = int(current_file[-1]['id']) + 1
            self.data['id'] = new_id
            current_file.append(self.data)
        else:
            current_file.append(self.data)

        try:
            with open("database/data_players.json", "w", encoding="utf-8-sig", newline="") as file:

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

    @staticmethod
    def load_players_file():
        try:
            with open("database/data_players.json", encoding="utf-8-sig", newline="") as file:

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

    @staticmethod
    def update_score(data_players):
        try:
            with open("database/data_players.json", "r+", encoding="utf-8-sig", newline="") as file:
                try:
                    new_file = json.load(file)
                    for player in new_file:
                        for current_player in data_players:
                            if player['identity'] == current_player['identity']:
                                player['point'] = float(player['point'] + current_player['point'])

                    file.seek(0)
                    json.dump(new_file, file, indent=4)

                    return True

                except json.JSONDecodeError as e:
                    print(f"Erreur lors de l'écriture des données JSON : {e}")
                    return False

        except IOError as er:
            print("Erreur lors de l'ouverture du fichier :", er)
            print("En cas de première insertion, une erreur (no such file) peut apparaître.")
            return False

        except UnicodeEncodeError as err:
            print("Erreur D'encodage :", err)
            return False
