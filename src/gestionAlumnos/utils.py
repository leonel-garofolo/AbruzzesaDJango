import datetime, calendar

def sqlDateFormat(date):
    dt = datetime.datetime.strptime(date, '%d/%m/%Y')
    return '{0:02}/{1}/{2}'.format(dt.year % 100, dt.month, dt.day)


def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)