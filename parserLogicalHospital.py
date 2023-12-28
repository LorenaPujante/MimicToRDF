import math

from classes import *
from variablesFiles import *


############
# SERVICES #
############
def parseServices():
    
    dicServices = {}

    nameFile = setFileInput(filesName["service"])
    with open(nameFile) as file:
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')
            
                id = int(line[0])
                abrev = line[1]
                description = line[2]
                
                typeStr = line[3]
                if typeStr == "Med":
                    type = ServiceType.Medical
                elif typeStr == "Surg":
                    type = ServiceType.Surgical
                else:
                    type = ServiceType.Neonatal
                
                service = Service(id, description, abrev, type)
                
                dicServices[id] = service

    file.close()

    return dicServices


#######
# HUs #
#######

def createHUS_multipleHUsByServ(dicServices):

    dicHUs = {}

    nameFile = setFileInput(filesName["hu"])
    with open(nameFile) as file:
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')

                idServ = int(line[0])
                s = dicServices[idServ]

                nEvents = line[2]
                nEvents = nEvents[:-1]
                nEvents = int(nEvents)

                # HUs are created so that each one will have approximately 1,500 hospitalizations
                nHUcreated = nEvents/1500
                if nHUcreated < 1:
                    nHUcreated = 1
                else:
                    rest = nHUcreated-math.floor(nHUcreated)
                    if rest > 0.5:
                        nHUcreated = math.ceil(nHUcreated)
                    else:
                        nHUcreated = math.floor(nHUcreated)
                
                for i in range(nHUcreated):
                    idHU = int(idServ) + 1000 + i*100
                    abrevHU = "{}_HU".format(s.abrev)
                    descHU = "{} Hospitalization Unit {}".format(s.description, i)

                    hu = HospUnit(idHU, descHU, abrevHU)

                    hu.service = s
                    s.hospUnits.append(hu.id)

                    dicHUs[idHU] = hu

    file.close()  

    return dicHUs



#####################
# FUNCION PRINCIPAL #
#####################

def parseLogicalHospital():
    
    dicServices = parseServices()
    dicHUs = createHUS_multipleHUsByServ(dicServices)
    return dicServices, dicHUs

