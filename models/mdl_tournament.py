from faker import Faker
import json
import os
import random
from datetime import date

fake = Faker("fr_FR")


class TournamentMdl:
    def __init__(self, name: str | None = None, address: str | None = None, birth: str | None = None,
                 number_turns: str | None = None, players=None):

        self.name = None
        self.address = None
        self.birth = None
        self.number_turns = None
        self.players = None

        if name and address and birth and number_turns and len(players) > 0:
            self.name = name.capitalize()
            self.address = str(address)
            self.birth = str(birth)
            self.number_turns = int(number_turns)
            self.players: dict = players

            self.instance_tournament()

    def instance_tournament(self):

        # print('instance_tournament', self.name, self.address, self.birth, self.number_turns, self.players)
        """players = []
        for x in range(self.tour_type):
            last_name = fake.last_name()
            first_name = fake.first_name()
            players.append((last_name, first_name))"""

        # pour numéroter les prochains tours faire comme id des joueurs dans data
        # prendre le dernier tour crée + 1
        # voir la date
        # un tuple pour les joueurs dans les matchs

        number_round = 1
        start_date = date.today()
        finish_date = ''
        pair_players = self.pair()

        new_round: dict = {'round': number_round, 'start_date': start_date, 'finish_date': finish_date,
                           'match': pair_players}

        return self.name, self.address, self.birth, self.number_turns, self.players, new_round

    def pair(self):
        players_pair = []
        players_count = int(len(self.players) / 2)
        print('NOMBRE DE PAIRS =>', players_count)

        for y in range(players_count):
            pair = random.sample(self.players, 2)
            players_pair.append(pair)

        return players_pair
