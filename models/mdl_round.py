from models.mdl_match import MatchMdl as M_mdl


class RoundMdl:
    def __init__(self, id_round: int | None = None, start: str | None = None, finish: str | None = None,
                 matchs: list | None = None):

        self.id_round = None
        self.start = None
        self.finish = None
        self.matchs_list = []

        if id_round > 0:
            self.instance_round(id_round, start, finish, matchs)

    def instance_round(self, id_round, start, finish, matchs):

        self.id_round = id_round

        if start:
            self.start = start

        if finish:
            self.finish = finish

        for match in matchs:
            object_match = M_mdl(match)
            self.matchs_list.append(object_match)


