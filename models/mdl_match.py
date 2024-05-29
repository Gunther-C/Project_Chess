
class MatchMdl:
    def __init__(self, pair: list | None = None):

        self.identity_plr1 = None
        self.name_plr1 = None
        self.score_plr1 = None

        self.identity_plr2 = None
        self.name_plr2 = None
        self.score_plr2 = None

        if len(pair) == 2:
            self.instance_match(pair)

    def instance_match(self, pair):

        if len(pair[0]) > 1 and len(pair[1]) > 1:
            self.identity_plr1 = pair[0][0]
            self.name_plr1 = pair[0][1]
            if len(pair[0]) > 2:
                self.score_plr1 = pair[0][2]

            self.identity_plr2 = pair[1][0]
            self.name_plr2 = pair[1][1]
            if len(pair[1]) > 2:
                self.score_plr2 = pair[1][2]



