

class PlayersMdl:

    def __init__(self, identity: str | None = None, last_name: str | None = None, first_name: str | None = None,
                 birth: str | None = None):

        self.identity = None
        self.last_name = None
        self.first_name = None
        self.birth = None

        if identity and last_name and first_name and birth:

            id_last = identity[:2].upper()
            id_first = identity[2:]
            self.identity = id_last + id_first
            self.last_name = str(last_name).capitalize()
            self.first_name = str(first_name).capitalize()
            self.birth = str(birth)
            self.instance_player()

            """
            self.new_player = {
                'Nom': self.last_name,
                'Prénom': self.first_name,
                'Date de naissance': self.birth
            }
            """

            # self.create_player()

    def instance_player(self):
        return self.identity, self.last_name, self.first_name, self.birth






