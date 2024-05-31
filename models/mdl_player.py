

class PlayersMdl:

    def __init__(self, id_player: str | None = None, identity: str | None = None, last_name: str | None = None,
                 first_name: str | None = None, birth: str | None = None, point: float | None = None):

        self.id_player = None
        self.identity = None
        self.last_name = None
        self.first_name = None
        self.birth = None
        self.point = 0

        self.instance_player(id_player, identity, last_name, first_name, birth, point)

    def instance_player(self, id_player, identity, last_name, first_name, birth, point):

        if identity and last_name:

            id_last = identity[:2].upper()
            id_first = identity[2:]
            self.identity = id_last + id_first
            self.last_name = str(last_name).capitalize()

            if id_player:
                self.id_player = id_player
            if first_name:
                self.first_name = str(first_name).capitalize()
            if birth:
                self.birth = str(birth)
            if point:
                self.point = point





