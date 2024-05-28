
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
        for pr in pair:
            if len(pr[0]) > 1 and len(pr[1]) > 1:
                self.identity_plr1 = pr[0][0]
                self.name_plr1 = pr[0][1]
                if len(pr[0]) > 2:
                    self.score_plr1 = pr[0][2]

                self.identity_plr1 = pr[1][0]
                self.name_plr1 = pr[1][1]
                if len(pr[1]) > 2:
                    self.score_plr1 = pr[1][2]


