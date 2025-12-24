import datetime
from unicodedata import category
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore
import json


def load_ui(file_path, parent=None):
    loader = QUiLoader()
    ui_file = QtCore.QFile(file_path)
    ui_file.open(QtCore.QFile.ReadOnly)
    ui = loader.load(ui_file, parent)
    ui_file.close()
    return ui


def save_habits(name, habit_class, points):
    json_dict = json.load(open("data.json"))
    habit_id = json_dict["habits"]["last_id"] + 1
    json_dict["habits"]["last_id"] += 1
    json_dict["habits"][habit_class][habit_id] = {
        "name": name,
        "points": points
    }
    json_dict["stat_for_day"]["habits"][habit_class][habit_id] = {
        "ended": False,
    }
    json.dump(json_dict, open("data.json", "w"), indent=4)


def delete_habits(habit_id, habit_class):
    json_dict = json.load(open("data.json"))
    del json_dict["habits"][habit_class][habit_id]
    del json_dict["stat_for_day"]["habits"][habit_class][habit_id]
    json.dump(json_dict, open("data.json", "w"), indent=4)


def load_day_stat(habit_class) -> dict:
    json_dict = json.load(open("data.json"))
    return json_dict["stat_for_day"]["habits"][habit_class]


def load_habits(habit_class):
    json_dict = json.load(open("data.json"))
    return json_dict["habits"][habit_class]


def load_stat_percents(habit_class):
    json_dict = json.load(open("data.json"))
    list_of_stat = json_dict["stat_for_day"]["habits"][habit_class].values()
    if len(list_of_stat) != 0:
        return (round((sum([1 if elem["ended"] else 0 for elem in list_of_stat]) /
                len(list_of_stat)) * 100))
    return 0


def load_global_stat(time="year"):
    json_dict = json.load(open("data.json"))
    stats = json_dict["stats"]
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    categories = []
    percents_bad_habits = []
    percents_good_habits = []
    if time == "month":
        for stat in stats:
            stat_date = datetime.datetime.strptime(stat["date"], "%d.%m.%Y")
            
            if (stat_date.year == current_year and
                    stat_date.month == current_month):
                percents_good_habits.append(stat["good_habit_percents"] * 100)
                percents_bad_habits.append(stat["bad_habit_percents"] * 100)
                categories.append(stat_date.strftime("%d"))
    elif time == "year":
        tmp_dict_good_habits = dict()
        tmp_dict_bad_habits = dict()
        for stat in stats:
            stat_date = datetime.datetime.strptime(stat["date"], "%d.%m.%Y")
            if stat_date.year == current_year:
                if stat_date.strftime("%b") in tmp_dict_good_habits.keys():
                    tmp_dict_good_habits[stat_date.strftime("%b")].append(stat["good_habit_percents"] * 100)
                    tmp_dict_bad_habits[stat_date.strftime("%b")].append(stat["bad_habit_percents"] * 100)
                else:
                    tmp_dict_good_habits[stat_date.strftime("%b")] = [stat["good_habit_percents"] * 100]
                    tmp_dict_bad_habits[stat_date.strftime("%b")] = [stat["bad_habit_percents"] * 100]
        for i in range(len(tmp_dict_good_habits.values())):
            percents_good_habits.append(sum(list(tmp_dict_good_habits.values())[i]) / len(list(tmp_dict_good_habits.values())[i]))
            percents_bad_habits.append(sum(list(tmp_dict_bad_habits.values())[i]) / len(list(tmp_dict_bad_habits.values())[i]))
            categories.append(list(tmp_dict_good_habits.keys())[i])
    else:
        percents_good_habits = load_stat_percents("good_habits")
        percents_bad_habits = load_stat_percents("bad_habits")
    return percents_good_habits, percents_bad_habits, categories


def update_stat(habit_id, habit_class):
    json_dict = json.load(open("data.json"))
    json_dict["stat_for_day"]["habits"][habit_class][habit_id]["ended"] = True
    json.dump(json_dict, open("data.json", "w"), indent=4)


def update_global_stat():
    json_dict = json.load(open("data.json"))
    if (json_dict["stat_for_day"]["date"] !=
            datetime.datetime.now().strftime("%d.%m.%Y")):

        count_ended_good_habits = 0
        count_good_habits = 0
        for elem in json_dict["stat_for_day"
                              ]["habits"
                                ]["good_habits"].values():
            count_good_habits += 1
            if elem["ended"]:
                count_ended_good_habits += 1
                elem["ended"] = False
        count_ended_bad_habits = 0
        count_bad_habits = 0
        for elem in json_dict["stat_for_day"]["habits"]["bad_habits"].values():
            count_bad_habits += 1
            if elem["ended"]:
                count_ended_bad_habits += 1
                elem["ended"] = False
        json_dict["stats"].append({
            "date": json_dict["stat_for_day"]["date"],
            "good_habit_percents": count_ended_good_habits / count_good_habits
            if count_good_habits != 0 else 1,
            "bad_habit_percents": count_ended_bad_habits / count_bad_habits
            if count_bad_habits != 0 else 1,
        })
        json_dict["stat_for_day"]["date"] = (
            datetime.datetime.now().strftime("%d.%m.%Y"))
        json.dump(json_dict, open("data.json", "w"), indent=4)
