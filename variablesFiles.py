
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


baseStringNorm = ".\\Input\\"

def setFileInput(name):
    nameFile = baseStringNorm + "{}.csv".format(name)
    return nameFile
