from core import core
from tkinter import Menu


def rotation(value=None, data_transfer=None):
    view = None
    match value:
        case 'm':
            view = Rotations()

        case 'j':
            from controlers.ctrl_players import PlayersCtrl
            view = PlayersCtrl()

        case 't':
            from controlers.ctrl_tournaments import TournamentsCtrl
            view = TournamentsCtrl(data_transfer)

    view.mainloop()


class Rotations(core.Core):
    def __init__(self):
        super().__init__()
        self.window_master()

    def window_master(self):

        def rotate_choice(choice):
            self.destroy()
            rotation(choice)

        self.menu_options = Menu(self.menu, tearoff=0, postcommand=lambda: self.menu_list())
        self.menu.add_command(label="Coté Tournois", command=lambda: rotate_choice('t'))
        self.menu.add_command(label="Coté Joueurs", command=lambda: rotate_choice('j'))
        self.menu.add_cascade(label="Options", menu=self.menu_options)
        self.config(menu=self.menu)

    def menu_list(self):
        if not self.widjets_menu:
            self.menu_options.add_command(label="Debug", command=lambda: self.debug())
            self.menu_options.add_command(label="Quitter", command=self.destroy)
            self.widjets_menu = True


if __name__ == '__main__':
    rotation()
