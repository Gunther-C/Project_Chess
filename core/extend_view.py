from tkinter import Entry, Label, font


class ExtendViews:
    def __init__(self, frame: any):
        self.frame = frame

        self.new_r = font.Font(family='Times New Roman', size=15, weight="bold", slant="roman")
        self.new_r_mini = font.Font(family='Times New Roman', size=10, weight="bold", slant="roman")

        self.lc_cal = font.Font(family='Lucida Calligraphy', size=20, weight="bold", slant="italic", underline=True)
        self.lc_cal_mini = font.Font(family='Lucida Calligraphy', size=15, weight="bold", slant="italic",
                                     underline=True)

    @staticmethod
    def adjust_x(parent, child) -> list:
        """
        :param parent:
        :param child:
        :return: Liste de valeurs pour centrage des widgets
        valeur1 = Largeur de l'élément parent
        valeur2 = Largeur de l'élément enfant
        valeur3 = Différence entre les deux largeurs ci-dessus
                  (diviser par deux pour les marges gauche et droite de la fenêtre enfant)
        """
        screen_width = parent.winfo_width()
        child_width = child.winfo_width()
        modulo_width = (screen_width - child_width) // 2
        return [screen_width, child_width, modulo_width]

    @staticmethod
    def adjust_y(parent, child) -> list:
        """
        :param parent:
        :param child:
        :return: Liste de valeurs pour centrage des widgets
        valeur1 = hauteur de l'élément parent
        valeur2 = hauteur de l'élément enfant
        valeur3 = Différence entre les deux hauteurs ci-dessus
                  (diviser par deux pour les marges haut et bas de la fenêtre enfant)
        """
        screen_height = parent.winfo_height()
        child_height = child.winfo_height()
        modulo_height = (screen_height - child_height) // 2
        return [screen_height, child_height, modulo_height]

    @staticmethod
    def input_text(**kwargs: any) -> Entry:
        """
        :param kwargs:
        :return: Création widget Label et Entry associés
        """
        label = Label(kwargs['mst'], bg=kwargs['bg'], text=kwargs['text'])
        new_input = Entry(kwargs['mst'], width=kwargs['ip_wh'])
        label.grid(column=kwargs['cols'], columnspan=kwargs['colspan'], row=kwargs['lb_row'], sticky='w')
        new_input.grid(column=kwargs['cols'], columnspan=kwargs['colspan'], row=kwargs['ip_row'], sticky='w')
        new_input.update()
        return new_input

    @staticmethod
    def input_date(**kwargs: any) -> any:
        """
        :param kwargs:
        :return: Création widget Label et multi Entry associés pour la date
        """
        label = Label(kwargs['mst'], bg=kwargs['bg'], text=kwargs['text'])
        label.grid(column=1, columnspan=5, row=kwargs['lb_row'], sticky='w')

        new_day = Entry(kwargs['mst'], width=5, justify='center')
        new_month = Entry(kwargs['mst'], width=5, justify='center')
        new_year = Entry(kwargs['mst'], width=8, justify='center')
        slash1 = Label(kwargs['mst'], width=1, height=1, bg="#FEF9E7", border=0, text="/")
        slash2 = Label(kwargs['mst'], width=1, height=1, bg=kwargs['bg'], border=0, text="/")

        new_day.grid(column=1, row=kwargs['ip_row'], sticky='w')
        slash1.grid(column=2, row=kwargs['ip_row'])
        new_month.grid(column=3, row=kwargs['ip_row'])
        slash2.grid(column=4, row=kwargs['ip_row'])
        new_year.grid(column=5, row=kwargs['ip_row'])

        return {'day': new_day, 'month': new_month, 'year': new_year}

    @staticmethod
    def title(**kwargs: any) -> Label:
        """
        :param kwargs:
        :return: Création widget Label avec font
        """
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])

        title = Label(kwargs['mst'], bg=kwargs['bg'], font=lb_font, justify=kwargs['justify'], text=kwargs['text'],
                      width=kwargs['width'], padx=kwargs['padx'], pady=kwargs['pady'])

        title.grid(row=kwargs['row'], column=kwargs['cols'], columnspan=kwargs['colspan'], sticky=kwargs['sticky'])
        title.update()
        return title

    @staticmethod
    def label(**kwargs: any) -> Label:
        """
        :param kwargs:
        :return: Création widget Label
        """
        label = Label(kwargs['mst'], width=kwargs['width'], height=kwargs['height'], bg=kwargs['bg'],
                      justify=kwargs['justify'], text=kwargs['text'])
        label.grid(row=kwargs['row'], ipadx=kwargs['ipadx'], ipady=kwargs['ipady'], column=kwargs['cols'],
                   columnspan=kwargs['colspan'], sticky=kwargs['sticky'])
        label.update()
        return label
