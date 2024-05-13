from rotate import rotation


def cmd(value=None):
    if not value:
        print("[J] Joueurs")
        print("[T] Tournois")
        print("[Q] Quitter")
        value = input('Entrez votre choix: ')
        value = value.lower()

    match value:
        case 'j':
            rotation('j')
        case 't':
            rotation('t')
        case 'q':
            quit()
        case _:
            print("\nChoisissez parmi les choix proposés \n")
            cmd()


if __name__ == '__main__':
    # cmd()
    rotation('j')

