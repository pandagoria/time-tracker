class File_manage:
    def __init__(self):
        __today_date = str(datetime.date.today())
        __file = file_read()

    @staticmethod
    def if_started() -> str:
        started_unix_time = re.search("started=([0-9]*\.[0-9]*)", __file)
        if started_unix_time is None:
            return None
        return started_unix_time

    @staticmethod
    def file_read():
        with open("data/template") as f:
            file = f.read()
        return file

    @property
    def get_today_date(self):
        return self.__today_date

    @property
    def get_file(self):
        return self.__file