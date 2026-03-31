from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, '')
d = datetime(1999, 10, 22)
formatted = d.strftime('%x')
print("locale format string:", formatted)

fmt = formatted.replace('1999', '%Y').replace('99', '%y').replace('10', '%m').replace('22', '%d')
print("derived format:", fmt)

# Test parsing
from datetime import datetime
print("parsing with derived:", datetime.strptime(formatted, fmt))
