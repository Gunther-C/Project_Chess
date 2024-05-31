from faker import Faker
import json
import os
import random
from core import french_date as date_fr
from models.mdl_round import RoundMdl as R_mdl
from models.mdl_player import PlayersMdl as P_mdl

fake = Faker("fr_FR")


class TournamentMdl:
    def __init__(self, id_tour: int | None = None, name: str | None = None, address: str | None = None,
                 birth: str | None = None, number_turns: int | None = None, rounds: list | None = None,
                 players: list | None = None):

        self.id_tour = None
        self.name = None
        self.address = None
        self.date = None
        self.number_turns = None
        self.players = []
        self.rounds = []

        if name and address and birth and number_turns and len(players) > 1:
            self.instance_tournament(id_tour, name, address, birth, number_turns, rounds, players)

    def instance_tournament(self, id_tour, name, address, birth, number_turns, rounds, players):

        self.name = str(name).capitalize()
        self.address = str(address)
        self.date = str(birth)
        self.number_turns = int(number_turns)

        if id_tour and rounds:
            """Tournoi éxistant"""
            self.id_tour = id_tour

            for _round in rounds:
                rd_ = R_mdl(_round['round'], _round['start'], _round['finish'], _round['matchs'])
                self.rounds.append(rd_)

            for player in players:
                instance = P_mdl(identity=player['identity'], last_name=player['last_name'],
                                 first_name=player['first_name'], point=player['point'])
                self.players.append(instance)

        else:
            """Tournoi en création → Création premier round"""
            self.players: list = players

            players_lists: list = []
            for player in players:
                capital = player.first_name[:2]
                new_name = f"{player.last_name}-{capital}"
                player_list = [player.identity, new_name]
                players_lists.append(player_list)

            first_match = self.pair(players_lists)
            rd_ = R_mdl(1, None, None, first_match)
            self.rounds.append(rd_)

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
