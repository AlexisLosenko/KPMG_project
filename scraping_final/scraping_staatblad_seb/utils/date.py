import datetime

def dategenerator():
    dt = datetime.datetime(2018, 1, 1)
    end = datetime.datetime(2018, 12, 31)
    step = datetime.timedelta(days=1)

    result = []

    while dt < end:
        result.append(dt.strftime('%Y-%m-%d'))
        dt += step
    return result 


