
def rotation(value=None, data_transfer=None):
    match value:
        case 'j':
            from controlers.ctrl_players import PlayersCtrl
            view = PlayersCtrl(data_transfer)
            view.mainloop()
        case 't':
            from controlers.ctrl_tournaments import TournamentsCtrl
            view = TournamentsCtrl(data_transfer)
            view.mainloop()


if __name__ == '__main__':
    rotation()
