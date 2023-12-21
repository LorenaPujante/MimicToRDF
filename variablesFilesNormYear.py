
baseStringNorm = ".\\Input\\"

filesName = {}
filesName["episode"] = "episodes"
filesName["ev_death"] = "deaths"
filesName["ev_tm"] = "testsMicro"
filesName["ev_hosp_loc"] = "transfers_loc"
filesName["ev_hosp_serv"] = "transfers_services"

filesName["patient"] = "patients"
filesName["service"] = "services"
filesName["micro"] = "microorganisms"
filesName["hu"] = "servsEvents"
filesName["room"] = "wardsAndRooms"
filesName["roomType"] = "wardsByType"


def getTwoLastDigitsNumber(number):
    number_str = "{}".format(number)
    number_str = number_str[-2:]
    return number_str

def setFileOutput(name, minYear, maxYear):
    minYear_str = getTwoLastDigitsNumber(minYear)
    maxYear_str = getTwoLastDigitsNumber(maxYear)
        
    nameFile = baseStringNorm + "{}_normYear_{}-{}.csv".format(name, minYear_str, maxYear_str)

    return nameFile

def setFileInput(name):
    nameFile = baseStringNorm + "{}.csv".format(name)
    return nameFile


