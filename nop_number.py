import locale

def number_format(number, localeset='', places=0):
    localeset = str(localeset)
    saved = locale.getlocale(locale.LC_NUMERIC)
    try:
        locale.setlocale(locale.LC_NUMERIC, localeset)
    except:
        try:
            localeset = localeset + '.utf8' #quick+dirty, will be fixed later
            locale.setlocale(locale.LC_NUMBERIC, localeset)
        except:
            pass
    if locale:
        ret = locale.format('%.*f', (places, number), True)
        locale.setlocale(locale.LC_NUMERIC, saved)
        return ret
    return number
    

