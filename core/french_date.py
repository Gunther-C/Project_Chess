import datetime
import locale


class FrenchDate:
    def __init__(self) -> None:
        self.array_month_fr = (
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre',
            'Décembre')
        # locale.setlocale(locale.LC_TIME, 'fr_FR')
        current_date = datetime.datetime.now()
        today_fr = str(current_date.date().day)
        month_fr = current_date.date().month
        month_fr = self.array_month_fr[month_fr - 1]
        year_fr = str(current_date.date().year)
        hour_fr = str(current_date.hour)
        minute_fr = str(current_date.minute)

        self.date_fr = today_fr + ' ' + month_fr + ' ' + year_fr
        self.date_hour_fr = today_fr + ' ' + month_fr + ' ' + year_fr + ' A ' + hour_fr + 'H ' + minute_fr

    def new_format_fr(self, year, month, day):

        month = int(month) - 1
        month_fr = self.array_month_fr[month]
        return day + ' ' + month_fr + ' ' + year
