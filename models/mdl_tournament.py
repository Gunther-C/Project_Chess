from faker import Faker
import json
import os
import random

fake = Faker("fr_FR")


class TournamentMdl:

    def __init__(self, **kwargs: any):

        if kwargs:
            self.name = str(kwargs['name']).capitalize()
            self.address = str(kwargs['address']).capitalize()
            self.birth = str(kwargs['birth'])
            self.tour_type = int(kwargs['tour_type'])
            # self.instance_tournament()

    def instance_tournament(self):

        print(self.name, self.address, self.birth, self.tour_type)
        players = []
        for x in range(self.tour_type):
            last_name = fake.last_name()
            first_name = fake.first_name()
            players.append((last_name, first_name))

        players_pair = []
        nbr_match = int(self.tour_type / 2)

        for y in range(nbr_match):
            pair = random.sample(players, 2)
            players_pair.append(pair)

        return self.name, self.address, self.birth, players, players_pair
