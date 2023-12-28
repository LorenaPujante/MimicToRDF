from variablesFiles import baseStringNorm


def getTwoLastDigitsNumber(number):
    number_str = "{}".format(number)
    number_str = number_str[-2:]
    return number_str

def setFileOutput(name, minYear, maxYear):
    minYear_str = getTwoLastDigitsNumber(minYear)
    maxYear_str = getTwoLastDigitsNumber(maxYear)
        
    nameFile = baseStringNorm + "{}_normYear_{}-{}.csv".format(name, minYear_str, maxYear_str)

    return nameFile

