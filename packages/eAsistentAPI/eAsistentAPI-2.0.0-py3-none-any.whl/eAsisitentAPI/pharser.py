import datetime
import json
import pandas as pd

from src.eAsisitentAPI.scraper import *

# Import school data
from git_hidden.get_secrets import get_schoold_id, get_class_id

SCHOOL_ID, CLASS_ID = get_schoold_id(), get_class_id()


def data_to_date(date: str):
    """
    :param date: Works for dates formatted with YYYY-MM-DD
    :return: datetime.date
    """
    split_date = date.split("-")
    return datetime.date(
        year=int(split_date[0]), month=int(split_date[1]), day=int(split_date[2])
    )


def hour_from_to_to_time(hour_from_to: str):
    split_time = hour_from_to.split("-")
    hour_from = split_time[0].split(":")
    hour_to = split_time[1].split(":")
    return [
        datetime.time(hour=int(hour_from[0]), minute=int(hour_from[1])),
        datetime.time(hour=int(hour_to[0]), minute=int(hour_to[1])),
    ]


def dict_to_json(dict_data):
    return json.dumps(dict_data, indent=4, ensure_ascii=False)


class eAsistentAPI:
    def __init__(self,
                 school_id: str,
                 class_id=0,
                 day=None,
                 hour=None,
                 hour_in_block=None,
                 professor=0,
                 classroom=0,
                 interest_activity=0,
                 school_week=0,
                 student_id=0,
                 ):
        schedule_data = get_schedule(school_id, class_id)
        for i in schedule_data.days:
            print(i.hours)
        # for i in schedule_data["0"]:
        #     print(i)
        #     print("---------")
        return
        schedule_request_data = schedule_data["request_data"]
        selection_data = schedule_data
        if day is not None:
            selection_data = selection_data.get(str(day))

        if type(hour) == int:
            count = 0
            for item in selection_data.keys():
                if count == hour:
                    selection_data = selection_data.get(str(item))
                    break
                count += 1

        print(dict_to_json(selection_data))
        self.request_time = schedule_request_data["request_epoch"]
        self.request_week = schedule_request_data["request_week"]
        self.hour_times = schedule_request_data["hour_times"]
        self.class_name = schedule_request_data["class"]
        self.dates = [data_to_date(day) for day in schedule_request_data["dates"]]
        self.hour_times = [hour_from_to_to_time(from_to) for from_to in
                           schedule_request_data["hour_times"]]


schedule_data = get_schedule("bf448609b88479b09bd27f52d555982cbd98affe", 504155, school_week=12)

r = Schedule(days=[SchoolDay(date=datetime.date(2023, 11, 14), hours=[Hour(name='1. ura', hour_blocks=[HourBlock(subject='DDP_MAT', teacher='I. Pustotnik', classroom='ma2', group=None, event=None, hour='1. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='2. ura', hour_blocks=[HourBlock(subject='ŠPO', teacher='V. Godnič', classroom='šp3', group=['Dekleta'], event=None, hour='2. ura', hour_in_block=0, date=datetime.date(2023, 11, 14)), HourBlock(subject='ŠPO', teacher='A. Pirc', classroom='šp1', group=['Fantje'], event=None, hour='2. ura', hour_in_block=1, date=datetime.date(2023, 11, 14))]), Hour(name='3. ura', hour_blocks=[HourBlock(subject='SLJ', teacher='I. Uranič', classroom='sl2', group=None, event=None, hour='3. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='4. ura', hour_blocks=[HourBlock(subject='MAT', teacher='T. Stanić', classroom='zgo', group=None, event=None, hour='4. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='5. ura', hour_blocks=[HourBlock(subject='NAR', teacher='V. Cunk', classroom='bio', group=None, event=None, hour='5. ura', hour_in_block=0, date=datetime.date(2023, 11, 14)), HourBlock(subject='DSP', teacher='M. Grah', classroom='is/ds ma', group=None, event=None, hour='5. ura', hour_in_block=1, date=datetime.date(2023, 11, 14))]), Hour(name='6. ura', hour_blocks=[HourBlock(subject='TJA', teacher='D. Jakljič', classroom='sl2', group=None, event=None, hour='6. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='7. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='7. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='8. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='8. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='9. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='9. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='10. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='10. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='11. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='11. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='12. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='12. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='13. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='13. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))]), Hour(name='14. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='14. ura', hour_in_block=0, date=datetime.date(2023, 11, 14))])]), SchoolDay(date=datetime.date(2023, 11, 15), hours=[Hour(name='1. ura', hour_blocks=[HourBlock(subject='športni dan', teacher=None, classroom=None, group=None, event='Dogodek', hour='1. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='2. ura', hour_blocks=[HourBlock(subject='športni dan', teacher=None, classroom=None, group=None, event='Dogodek', hour='2. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='3. ura', hour_blocks=[HourBlock(subject='športni dan', teacher=None, classroom=None, group=None, event='Dogodek', hour='3. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='4. ura', hour_blocks=[HourBlock(subject='športni dan', teacher=None, classroom=None, group=None, event='Dogodek', hour='4. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='5. ura', hour_blocks=[HourBlock(subject='športni dan', teacher=None, classroom=None, group=None, event='Dogodek', hour='5. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='6. ura', hour_blocks=[HourBlock(subject='športni dan', teacher=None, classroom=None, group=None, event='Dogodek', hour='6. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='7. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='7. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='8. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='8. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='9. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='9. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='10. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='10. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='11. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='11. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='12. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='12. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='13. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='13. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))]), Hour(name='14. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='14. ura', hour_in_block=0, date=datetime.date(2023, 11, 15))])]), SchoolDay(date=datetime.date(2023, 11, 16), hours=[Hour(name='1. ura', hour_blocks=[HourBlock(subject='DDP_ANG', teacher='M. Mihelec', classroom='tj1', group=None, event=None, hour='1. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='2. ura', hour_blocks=[HourBlock(subject='NAR', teacher='V. Cunk', classroom='bio', group=None, event=None, hour='2. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='3. ura', hour_blocks=[HourBlock(subject='NAR', teacher='V. Cunk', classroom='bio', group=None, event=None, hour='3. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='4. ura', hour_blocks=[HourBlock(subject='GUM', teacher='M. Wolf', classroom='gla', group=None, event=None, hour='4. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='5. ura', hour_blocks=[HourBlock(subject='TJA', teacher='D. Jakljič', classroom='sl2', group=None, event=None, hour='5. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='6. ura', hour_blocks=[HourBlock(subject='MAT', teacher='T. Stanić', classroom='kem', group=None, event=None, hour='6. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='7. ura', hour_blocks=[HourBlock(subject='IP_ŠAH', teacher='M. Škrlj', classroom='zgo', group=None, event=None, hour='7. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='8. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='8. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='9. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='9. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='10. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='10. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='11. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='11. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='12. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='12. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='13. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='13. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))]), Hour(name='14. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='14. ura', hour_in_block=0, date=datetime.date(2023, 11, 16))])]), SchoolDay(date=datetime.date(2023, 11, 17), hours=[Hour(name='1. ura', hour_blocks=[HourBlock(subject='ŠPO', teacher='V. Godnič', classroom='šp3', group=['Dekleta'], event=None, hour='1. ura', hour_in_block=0, date=datetime.date(2023, 11, 17)), HourBlock(subject='ŠPO', teacher='V. Godnič', classroom='šp1', group=['Fantje'], event='Nadomeščanje', hour='1. ura', hour_in_block=1, date=datetime.date(2023, 11, 17))]), Hour(name='2. ura', hour_blocks=[HourBlock(subject='SLJ', teacher='I. Uranič', classroom='sl2', group=None, event=None, hour='2. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='3. ura', hour_blocks=[HourBlock(subject='TJA', teacher='D. Jakljič', classroom='ma3', group=None, event=None, hour='3. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='4. ura', hour_blocks=[HourBlock(subject='TJA', teacher='M. Mihelec', classroom='geo', group=None, event='Nadomeščanje', hour='4. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='5. ura', hour_blocks=[HourBlock(subject='ZGO', teacher='M. Škrlj', classroom='zgo', group=None, event=None, hour='5. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='6. ura', hour_blocks=[HourBlock(subject='MAT', teacher='T. Stanić', classroom='lik', group=None, event=None, hour='6. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='7. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='7. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='8. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='8. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='9. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='9. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='10. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='10. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='11. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='11. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='12. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='12. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='13. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='13. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))]), Hour(name='14. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='14. ura', hour_in_block=0, date=datetime.date(2023, 11, 17))])]), SchoolDay(date=datetime.date(2023, 11, 18), hours=[Hour(name='1. ura', hour_blocks=[HourBlock(subject='DDP_PE', teacher='Š. Pernar', classroom='sl1', group=None, event=None, hour='1. ura', hour_in_block=0, date=datetime.date(2023, 11, 18)), HourBlock(subject='UP_ŽR', teacher='I. Uranič', classroom='sl2', group=None, event=None, hour='1. ura', hour_in_block=1, date=datetime.date(2023, 11, 18))]), Hour(name='2. ura', hour_blocks=[HourBlock(subject='SLJ', teacher='I. Uranič', classroom='sl2', group=None, event=None, hour='2. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='3. ura', hour_blocks=[HourBlock(subject='TJA', teacher='D. Jakljič', classroom='lik', group=None, event='Nadomeščanje', hour='3. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='4. ura', hour_blocks=[HourBlock(subject='TIT', teacher='I. Pavlin', classroom='tj3', group=['Skupina 2'], event='Nadomeščanje', hour='4. ura', hour_in_block=0, date=datetime.date(2023, 11, 18)), HourBlock(subject='TIT', teacher='I. Pavlin', classroom='teh', group=['Skupina 1'], event=None, hour='4. ura', hour_in_block=1, date=datetime.date(2023, 11, 18))]), Hour(name='5. ura', hour_blocks=[HourBlock(subject='TIT', teacher='I. Pavlin', classroom='gos', group=['Skupina 2'], event='Nadomeščanje', hour='5. ura', hour_in_block=0, date=datetime.date(2023, 11, 18)), HourBlock(subject='TIT', teacher='I. Pavlin', classroom='teh', group=['Skupina 1'], event=None, hour='5. ura', hour_in_block=1, date=datetime.date(2023, 11, 18))]), Hour(name='6. ura', hour_blocks=[HourBlock(subject='TJA', teacher='D. Jakljič', classroom='gla', group=None, event=None, hour='6. ura', hour_in_block=0, date=datetime.date(2023, 11, 18)), HourBlock(subject='SZT', teacher='M. Grah', classroom='is/ds ma', group=None, event=None, hour='6. ura', hour_in_block=1, date=datetime.date(2023, 11, 18))]), Hour(name='7. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='7. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='8. ura', hour_blocks=[HourBlock(subject='UP_ŽR', teacher='T. Stanić', classroom='1', group=None, event=None, hour='8. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='9. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='9. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='10. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='10. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='11. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='11. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='12. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='12. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='13. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='13. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))]), Hour(name='14. ura', hour_blocks=[HourBlock(subject=None, teacher=None, classroom=None, group=None, event=None, hour='14. ura', hour_in_block=0, date=datetime.date(2023, 11, 18))])])], hour_times=['7:30-8:15', '8:20-9:05', '9:25-10:10', '10:15-11:00', '11:05-11:50', '11:55-12:40', '12:45-13:30', '13:45-14:30', '14:35-15:20', '15:25-16:10', '16:15-17:00', '17:05-17:50', '17:55-18:40', '18:45-19:30'], dates=[datetime.date(2023, 11, 14), datetime.date(2023, 11, 15), datetime.date(2023, 11, 16), datetime.date(2023, 11, 17), datetime.date(2023, 11, 18)], class_name='7.b', request_week=12, request_epoch=1674293182, used_data=UsedData(school_id='bf448609b88479b09bd27f52d555982cbd98affe', class_id=504155, professor=0, classroom=0, interest_activity=0, school_week=12, student_id=0))

print(schedule_data.days == r.days)
exit()
sc = []
# Iterate over the days in the schedule
for day in schedule_data.days:
    # Iterate over the hours in the day
    for hour in day.hours:
        # Iterate over the hour blocks in the hour
        sc.append({
            "Date": day.date,
            "Hour": hour.name,
            "Block Data": [{
                "hour_in_block": x.hour_in_block,
                "group": x.group,
                "event": x.event,
                "classroom": x.classroom,
                "subject": x.subject,
                "teacher": x.teacher,
            } for x in hour.hour_blocks]
        })


print(sc)
# Create a DataFrame from the schedule data
schedule_df = pd.DataFrame(sc)

# Export the DataFrame to a CSV file
schedule_df.to_csv("schedule.csv", index=False)
# v = eAsistentAPI(SCHOOL_ID, class_id=CLASS_ID, day=1, hour=3)
# print(a.hour_times, a.dates, a.class_name, a.request_week, a.request_time,
#       a.hour_times,
#       sep="\n")


# def hour_data(
#         school_id: str,
#         hour=None,
#         day=None,
#         class_id=0,
#         professor=0,
#         classroom=0,
#         interest_activity=0,
#         school_week=0,
#         student_id=0,
# ):
#     """
#     Date format is: YYYY-MM-DD
#     If school id is invalid ValueError is raised
#
#     :param school_id: The ID of the school you want to get data for
#     :type school_id: str
#     :param hour: What hours do you want to get data for, defaults to None (optional)
#     :type hour: int
#     :param day: What day you want to get data for, 0 Monday, 1 Tuesday, 2 Wednesday, 3 Thursday, 4 Friday, 5 Saturday, 6 Sunday, None is all, defaults to None (optional)
#     :type day int
#     :param class_id: The ID of the class you want to get data for, 0 is all classes, defaults to 0 (optional)
#     :param professor: The ID of the professor you want to get data for,  0 is all professors, defaults to 0 (optional)
#     :param classroom: The classroom you want to get data for,  0 is all classrooms, defaults to 0 (optional)
#     :param interest_activity: The activity you want to get data for, 0 is all interest activities, defaults to 0 (optional)
#     :param school_week: school week that you want to get the data for, 0 is the current week, defaults to 0 (optional)
#     :param student_id: The ID of the student you want to get the schedule for,0 is all students, defaults to 0 (optional)
#     :return: A dictionary with the data.
#     """
#
#     schedule_data: dict = get_schedule_data(school_id=school_id,
#                                             class_id=class_id,
#                                             professor=professor,
#                                             classroom=classroom,
#                                             interest_activity=interest_activity,
#                                             school_week=school_week,
#                                             student_id=student_id)
#     for data_day in schedule_data:
#         if data_day != "week_data":
#             for data_hour in schedule_data[data_day]:
#                 print(data_hour)
