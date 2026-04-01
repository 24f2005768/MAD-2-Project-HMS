from app import *
from models import *
from datetime import time, date, timedelta, datetime
from sqlalchemy import or_, desc, asc
from datetime import datetime

# Get current local date and time
now = datetime.now()
print(now) # Output: 2026-04-01 10:53:15.123456