from tkinter import *
from tkinter import font, Entry, Radiobutton, Checkbutton
from tkinter import ttk


class ExtendViews:
    def __init__(self, frame: any):
        self.frame = frame

    @staticmethod
    def adjust_x(parent, child) -> list:
        screen_width = parent.winfo_width()
        child_width = child.winfo_width()
        modulo_width = (screen_width - child_width) // 2
        return [screen_width, child_width, modulo_width]

    @staticmethod
    def adjust_y(parent, child) -> list:
        screen_height = parent.winfo_height()
        child_height = child.winfo_height()
        modulo_height = (screen_height - child_height) // 2
        return [screen_height, child_height, modulo_height]

    @staticmethod
    def input_text(**kwargs: any) -> Entry:
        label = Label(kwargs['mst'], bg=kwargs['bg'], text=kwargs['text'])
        new_input = Entry(kwargs['mst'], width=kwargs['ip_wh'])
        label.grid(column=kwargs['cols'], columnspan=kwargs['colspan'], row=kwargs['lb_row'], sticky=W)
        new_input.grid(column=kwargs['cols'], columnspan=kwargs['colspan'], row=kwargs['ip_row'], sticky=W)
        new_input.update()
        return new_input

    @staticmethod
    def input_date(**kwargs: any) -> any:
        label = Label(kwargs['mst'], bg=kwargs['bg'], text=kwargs['text'])
        label.grid(column=1, columnspan=5, row=kwargs['lb_row'], sticky=W)

        new_day = Entry(kwargs['mst'], width=5, justify='center')
        new_month = Entry(kwargs['mst'], width=5, justify='center')
        new_year = Entry(kwargs['mst'], width=8, justify='center')
        slash1 = Label(kwargs['mst'], width=1, height=1, bg="#FEF9E7", border=0, text="/")
        slash2 = Label(kwargs['mst'], width=1, height=1, bg=kwargs['bg'], border=0, text="/")

        new_day.grid(column=1, row=kwargs['ip_row'], sticky=W)
        slash1.grid(column=2, row=kwargs['ip_row'])
        new_month.grid(column=3, row=kwargs['ip_row'])
        slash2.grid(column=4, row=kwargs['ip_row'])
        new_year.grid(column=5, row=kwargs['ip_row'])

        return {'day': new_day, 'month': new_month, 'year': new_year}

    @staticmethod
    def radio_button(**kwargs: any) -> Radiobutton:
        label = Label(kwargs['mst'], bg=kwargs['bg'], text=kwargs['text'], justify=kwargs['justify'])
        radio = Radiobutton(kwargs['mst'], bg='red', justify=kwargs['justify'], variable=kwargs['variable'],
                            value=kwargs['value'], indicatoron=False, offrelief="flat", overrelief="ridge",
                            selectcolor='black')
        label.grid(column=kwargs['cols'], row=kwargs['lb_row'], sticky=kwargs['sticky'])
        radio.grid(column=kwargs['cols'], row=kwargs['ip_row'], sticky=kwargs['sticky'])
        radio.update()
        return radio

    @staticmethod
    def check_button(**kwargs: any) -> Checkbutton:
        check = Checkbutton(kwargs['mst'], variable=kwargs['variable'], onvalue=kwargs['onvalue'],
                            offvalue=kwargs['offvalue'], bg=kwargs['bg'], justify=kwargs['justify'],
                            indicatoron=kwargs['indicatoron'], offrelief="flat", overrelief="ridge",
                            selectcolor=kwargs['selectcolor'], state=kwargs['state'])
        check.grid(column=kwargs['cols'], row=kwargs['row'], sticky=kwargs['sticky'], padx=kwargs['padx'],)
        check.update()
        return check

    @staticmethod
    def title(**kwargs: any) -> Label:
        lb_font = font.Font(family=kwargs['family'], size=kwargs['size'], weight=kwargs['weight'],
                            slant=kwargs['slant'], underline=kwargs['underline'])

        title = Label(kwargs['mst'], bg=kwargs['bg'], font=lb_font, justify=kwargs['justify'], text=kwargs['text'],
                      width=kwargs['width'], padx=kwargs['padx'], pady=kwargs['pady'])

        title.grid(row=kwargs['row'], column=kwargs['cols'], columnspan=kwargs['colspan'], sticky=kwargs['sticky'])
        title.update()
        return title

    @staticmethod
    def label(**kwargs: any) -> Label:
        label = Label(kwargs['mst'], width=kwargs['width'], height=kwargs['height'], bg=kwargs['bg'],
                      justify=kwargs['justify'], text=kwargs['text'])
        label.grid(row=kwargs['row'], ipadx=kwargs['ipadx'], ipady=kwargs['ipady'], column=kwargs['cols'],
                   columnspan=kwargs['colspan'], sticky=kwargs['sticky'])
        label.update()
        return label
