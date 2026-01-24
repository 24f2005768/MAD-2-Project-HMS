from app import *
from models import *
from datetime import time

# shift1 = Shift(name = 'Morning',start_time = time(hour=9), end_time = time(hour = 12))
# db.session.add(shift1)

shift1 = Shift(name = 'Afternoon',start_time = time(hour=14), end_time = time(hour = 17))
db.session.add(shift1)

shift1 = Shift(name = 'Evening',start_time = time(hour=20), end_time = time(hour = 23))
db.session.add(shift1)
db.session.commit()