import time

print(time.time())
print(time.clock())
print("start")
time.sleep(1)
print("end")

from datetime import datetime

t = datetime(2018,5,24,21,30)
for it in t.timetuple():
    print(it)
print(t.year)
print(t.weekday())
print(datetime.now())
print(datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M"))
