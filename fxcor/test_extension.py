import julian
import datetime as dt

date = 2458731.48319221
date_norm = julian.from_jd(date, fmt='jd')
print(date_norm)