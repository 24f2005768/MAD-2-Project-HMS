from app import *
from models import *
from datetime import time, date, timedelta
from sqlalchemy import or_, desc

dates = Shift.query.order_by(desc(Shift.id)).all()
print(dates[0])
search_query = "23"

lst = Patient.query.join(User).filter(or_(Patient.name.like(f"%{search_query}%"),User.email.like(f"%{search_query}%"))).all()
print(lst)
