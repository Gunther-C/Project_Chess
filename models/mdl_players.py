

class PlayersMdl:

    def __init__(self, **kwargs: any):

        # self.new_player = None

        if kwargs:
            self.last_name = str(kwargs['last_name']).capitalize()
            self.first_name = str(kwargs['first_name']).capitalize()
            self.birth = str(kwargs['birth'])
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
        return self.last_name, self.first_name, self.birth






