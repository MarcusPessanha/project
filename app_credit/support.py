from datetime import datetime, date


class Support():

    def get_time():
        time = datetime.now()
        return time

    def get_date():
        today = datetime.date(datetime.now())
        return today