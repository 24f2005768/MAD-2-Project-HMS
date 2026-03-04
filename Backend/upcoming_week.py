from models import *
from datetime import date, timedelta

def add_missing_shifts():
    next_week_dates = [(date.today() + timedelta(days = i)) for i in range(8)]
    for d in next_week_dates:
        # date in Shift is stored as DateTime, so we need to make a datetime object first
        d_str = datetime.strftime(d, '%d-%m-%Y')
        d_dt = datetime.strptime(d_str, '%d-%m-%Y')
        flag = Shift.query.filter(Shift.date == d_dt).first()
        if flag == None:
            s1 = Shift(date = d, name = 'Morning',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=9), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 12))
            s2 = Shift(date = d, name = 'Afternoon',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=14), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 17))
            s3 = Shift(date = d, name = 'Evening',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=20), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 23))

            db.session.add(s1)
            db.session.add(s2)
            db.session.add(s3)
    db.session.commit()
    return True
