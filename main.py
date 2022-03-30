import re
import datetime
import time
import os
# from File_manage import File_manage

today_date = str(datetime.date.today())

def push_start() -> None:
    with open("data/template", "r") as file:
        reader = file.read()
    started = re.search("started=([0-9]*\.[0-9]*)", reader)
    if started is not None:
        print("Уже существует начатый временнной промежуток. Команда \"finish\", чтобы завершить.")
    else:
        start = str(time.time())
        h = re.search(today_date, reader)
        new_file = reader[:19] + start + reader[20:]
        if h is None:
            with open("data/template", "w") as file:
                file.write(new_file + "\n" + today_date + ",")
        else:
            with open("data/template", "w") as file:
                file.write(new_file)
        print("Секунды с начала эпохи Unix бегут для тебя. Хорошего кодинга:)")


def push_finish() -> None:
    with open("data/template", "r") as file:
        reader = file.read()
    # Ищем, есть ли начатый отсчет времени
    started = re.search("started=([0-9]*\.[0-9]*)", reader)
    if started is None:
        print("Нет начатого временого промежутка, команда \"start\", чтобы начать.")
    else:
        finished = time.time()  # Сохраняем время окончания пром.
        total_secs = int(float(finished)) - int(float(started[1]))  # Считаем разницу начала и конца промежутка
        total = datetime.timedelta(seconds=total_secs)  # Переводим из epoch в читабельный формат
        check = re.search(today_date+",([0-9]:[0-9]{2}:[0-9]{2})", reader)  # Ищем, кодили ли уже сегодня
        if check is not None:  # Если промежуток за сегодня существует
            last_updated = check[1]  # группа только с промежутком вр
            total += datetime.timedelta(hours=int(last_updated[0]),
                                        minutes=int(last_updated[2:4]), seconds=int(last_updated[5:7]))
            reader = re.sub(last_updated, "", reader)
        reader = re.sub(str(started[1]), " ", reader)
        with open("data/template", "w") as file:
            file.write(reader + str(total))
        print("Сегодня ({}) ты кодил(-а) {} ч. {} мин.".format(today_date, str(total)[0], str(total)[2:4]))


def statistics_for_period(stat):
    # Looking for requested dates
    dates = re.search("([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]{4}-[0-9]{2}-[0-9]{2})", stat)
    # Checking if the date format was written correctly
    if dates is None:
        dates = re.search("([0-9]{4}-[0-9]{2}-[0-9]{2})", stat)
        if dates is not None:
            one_day_statistics(dates)
        else:
            print("Введен неверный формат")
        return
    with open("data/template") as file:
        reader = file.read()
    # Creating variables w requested periods in datetime.date format
    date1 = datetime.date(int(dates[1][0:4]), int(dates[1][5:7]), int(dates[1][8:10]))
    date2 = datetime.date(int(dates[2][0:4]), int(dates[2][5:7]), int(dates[2][8:10]))
    # Checking if the user was active during requested period. If no activity, printing error
    if str(date1) not in reader:
        # if there's any date before the end of period in data file, counting until finding the first one that matches,
        # saving in original date variable
        while str(date1) not in reader:
            date1 += datetime.timedelta(days=1)
            if date1 > date2:
                print("Нет активности за данный временной промежуток, либо введен невалидный временной промежуток.")
                return
    if str(date2) not in reader:
        # if there's any date before the start of period in data file, counting until finding the first one
        # that matches, saving in original date variable
        while str(date2) not in reader:
            date2 -= datetime.timedelta(days=1)
            if date2 < date1:
                print("Нет активности за данный временной промежуток, либо введен невалидный временной промежуток.")
                return
    # Creating new string including only periods and time spans of requested period
    # Searching for time span of the first date of the period
    last_time = re.search(str(date2) + ",([0-9]:[0-9]{2}:[0-9]{2})", reader)
    if last_time is None:
        print("Нет активности за данный временной промежуток, либо введен невалидный временной промежуток.")
        return
    # Creating new string
    new_reader = reader[reader.index(str(date1)):reader.index(last_time[1]) + 7]
    # Initializing variable that will contain total activity time
    new_time = datetime.timedelta()
    # Initializing variable that contains only all activity time periods of the req.period, divided into groups
    timing = re.findall("([0-9]:[0-9]{2}:[0-9]{2})", new_reader)
    # Counting the sum of total activity time in datetime.timedelta format
    for i in timing:
        new_time += datetime.timedelta(hours=int(i[0]),
                                       minutes=int(i[2:4]), seconds=int(i[5:7]))
    new_time = str(new_time).split(':')
    print("С {} по {} ты кодил(-а) {} ч. {} мин.".format(dates[1], dates[2], new_time[0], new_time[1]))


def one_day_statistics(dates):
    with open("data/template") as file:
        reader = file.read()
    # Creating variables w requested periods in datetime.date format
    date = datetime.date(int(dates[1][0:4]), int(dates[1][5:7]), int(dates[1][8:10]))
    timing = re.search(str(date) + ",([0-9]:[0-9]{2}:[0-9]{2})", reader)
    # Checking if the user was active during requested period. If no activity, printing error
    if str(date) not in reader or timing is None:
        print("Нет активности за данный временной промежуток, либо введен невалидный временной промежуток.")
        return
    new_time = str(timing[1]).split(':')
    print("{} ты кодил(-а) {} ч. {} мин.".format(dates[1], new_time[0], new_time[1]))


def main():
    print("Доступные команды: start, finish, stat, exit")
    while True:
        try:
            user_input = input()
            if user_input == "start":
                push_start()
            elif user_input == "finish":
                push_finish()
            elif user_input == "stat":
                stat = input(
                    "Введи за какой период нужна статистика в формате:\"YYYY-MM-DD YYYY-MM-DD\" или \"YYYY-MM-DD\": ")
                statistics_for_period(stat)
            elif user_input == "exit":
                return
            else:
                print("Доступные команды: start, finish, stat, exit")
        except EOFError:
            return

if __name__ == '__main__':
    main()