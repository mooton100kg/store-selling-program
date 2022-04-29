from datetime import datetime,timedelta
y = '22'
date_time_obj = datetime.strptime(y, '%y').strftime('%Y')
print(date_time_obj)