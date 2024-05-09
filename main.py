from controlers import ctrl_players
def cmd():
    print("[J] Joueurs")
    print("[T] Tournois")
    print("[Q] Quitter")
    value = input('Entrez votre choix: ')
    value = value.lower()

    match value:
        case 'j':
            from controlers.ctrl_players import PlayersCtrl
            """window = PlayersCtrl()
            window.mainloop()"""
        case 't':
            from controlers import ctrl_tournaments
            # ctrl_tournaments.TournamentsCtrl()
        case 'q':
            quit()
        case _:
            print("\nChoisissez parmi les choix proposés \n")
            cmd()


if __name__ == '__main__':
    pass
    # cmd()
    # ctrl_players.PlayersCtrl()
