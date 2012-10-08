import locale

def number_format(number, localeset='', places=0):
    localeset = str(localeset)
    saved = locale.getlocale(locale.LC_NUMERIC)
    locale.setlocale(locale.LC_NUMERIC, localeset)
    ret = locale.format('%.*f', (places, number), True)
    locale.setlocale(locale.LC_NUMERIC, saved)
    return ret
    

