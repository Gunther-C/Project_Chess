from faker import Faker
import json
import os
import random
from datetime import date

fake = Faker("fr_FR")


class TournamentMdl:
    def __init__(self, name: str | None = None, address: str | None = None, birth: str | None = None,
                 number_turns: str | None = None, rounds=None, players=None):

        self.name = None
        self.address = None
        self.date = None
        self.number_turns = None
        self.players = None
        self.rounds = None

        self.instance_tournament(name, address, birth, number_turns, rounds, players)

    def instance_tournament(self, name, address, birth, number_turns, rounds, players):

        if name and address and birth and number_turns and len(players) > 1:

            self.name = str(name).capitalize()
            self.address = str(address)
            self.date = str(birth)
            self.number_turns = int(number_turns)
            self.players: list = players

            if rounds:
                self.rounds: dict = rounds
            else:
                players_lists: list = []
                for player in players:
                    first_name = player.pop('Prénom', None)
                    capital = first_name[0]
                    player['Nom'] = f"{player['Nom']}.{capital}"
                    player_list = [player['Identité'], player['Nom']]
                    players_lists.append(player_list)
                first_match = self.pair(players_lists)
                self.rounds: dict = {"round": 1, "start": '', "finish": '',  "matchs": first_match}

    def pair(self, match) -> list:
        players_count = int(len(match) / 2)
        players_lists: list = []
        for y in range(players_count):
            pair = random.sample(match, 2)
            match_players: tuple = (pair[0], pair[1])
            for element in pair:
                match.remove(element)
            players_lists.append(match_players)

        return players_lists


    """players = []
    for x in range(self.tour_type):
        last_name = fake.last_name()
        first_name = fake.first_name()
        players.append((last_name, first_name))"""
