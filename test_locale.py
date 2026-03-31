import locale
from datetime import datetime
try:
    locale.setlocale(locale.LC_ALL, '')
    print(locale.nl_langinfo(locale.D_FMT))
except Exception as e:
    print(e)
print(datetime.now().strftime('%x'))
