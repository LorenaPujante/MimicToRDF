
from datetime import datetime, timedelta

from classes import Event, EventType
from variablesFilesNormYear import *
from alphabets import abcCap
from dateNormalizer import isLeapyear
from durationCalculator import *


########################################
# AUXILIARY CLASS FOR HOSPITALIZATIONS #
########################################

class HospitalizationAux:
    def __init__(self, id, episode, start, end):
        self.id = id
        self.start = start
        self.end = end
        self.episode = episode
        self.location = None    # ID is saved
        self.service = None     # Name is saved 



#############################################
# READING INPUT FILES AS HospitalizationAux #
#############################################

def parseHospitalization_InBed(dicHospsAux, dicEpisodes, minYearN, maxYearN, minYear, maxYear):   # This function must be executed before "parseHospitalization_InService()"
    nameFile = setFileOutput(filesName["ev_hosp_loc"], minYearN, maxYearN)
    with open(nameFile) as file:
        
        lastHosp = None
        lastHospEnd = None
        
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')
    
                start_str = line[6]
                start_hosp = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                end_str = line[7]
                end_str = end_str[:-1]
                end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
                
                idEp = int(line[2])

                if start_hosp.year >= minYear  and  end.year <= maxYear  and  idEp in dicEpisodes:

                    
                    idWard = int(line[5])

                        # It may happen that the first hospitalization does not begin at the same time as the episode to which it belongs   ->  We keep the Minor date
                    start_ep = dicEpisodes[idEp].start
                    if lastHosp is not None:
                        if lastHosp.id != idEp:
                            if start_ep <= start_hosp:
                                start = start_ep
                            else:
                                start = start_hosp
                                dicEpisodes[idEp].start = start
                        else:
                            start = start_hosp
                    else:
                        if start_ep <= start_hosp:
                            start = start_ep
                        else:
                            start = start_hosp
                            dicEpisodes[idEp].start = start
            
                        # It may happen that the last hospitalization does not end at the same time as the episode to which it belongs  ->  We keep the older date 
                    if lastHosp is not None:
                        if lastHosp.id != idEp:
                            lastEpEnd = dicEpisodes[lastHosp.id].end
                            if lastEpEnd >= lastHospEnd:
                                lastHosp.end = lastEpEnd
                            else:
                                lastHosp.end = lastHospEnd
                                dicEpisodes[lastHosp.id].end = lastHospEnd
            
                    hosp = HospitalizationAux(idEp, idEp, start, end)
                    hosp.location = idWard 

                    lastHosp = hosp
                    lastHospEnd = end

                    if idEp in dicHospsAux:
                        dicHospsAux[idEp].append(hosp)
                    else:
                        dicHospsAux[idEp] = []
                        dicHospsAux[idEp].append(hosp) 

        lastHosp.end = dicEpisodes[lastHosp.id].end

    file.close()


def parseHospitalization_InService(dicHospsAux, dicEpisodes, minYearN, maxYearN, minYear):
    nameFile = setFileOutput(filesName["ev_hosp_serv"], minYearN, maxYearN)
    
    with open(nameFile) as file:
        
        lastHosp = None

        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')
            
                start_str = line[3]
                start_hosp = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                
                idEp = int(line[2])

                if start_hosp.year >= minYear  and  idEp in dicEpisodes:
                    
                    nameService = line[4]
                    nameService = nameService[:-1]

                        # It may happen that the first hospitalization does not begin at the same time as the episode to which it belongs   ->  We keep the Minor date
                    start_ep = dicEpisodes[idEp].start
                    if lastHosp is not None:
                        if lastHosp.id != idEp:
                            if start_ep <= start_hosp:
                                start = start_ep
                            else:
                                start = start_hosp
                                dicEpisodes[idEp].start = start
                                if idEp in dicHospsAux:
                                    dicHospsAux[idEp][0].start = start
                    else:
                        if start_ep <= start_hosp:
                            start = start_ep
                        else:
                            start = start_hosp
                            dicEpisodes[idEp].start = start
                            if idEp in dicHospsAux:
                                dicHospsAux[idEp][0].start = start

                    hosp = HospitalizationAux(idEp, idEp, start, None)
                    hosp.service = nameService

                    if lastHosp is not None:
                        if lastHosp.episode == idEp:
                            lastHosp.end = start
                        else:
                            lastHosp.end = dicEpisodes[lastHosp.episode].end 

                    if idEp in dicHospsAux:
                        dicHospsAux[idEp].append(hosp)
                    else:
                        dicHospsAux[idEp] = []
                        dicHospsAux[idEp].append(hosp)

                    lastHosp = hosp

        lastHosp.end = dicEpisodes[lastHosp.episode].end 

    file.close()



#########################################
# POST-PROCESSING OF HospitalizationAux #
#########################################

def deleteEpisodesWithout_LocsOrServs(dicEpisodes, dicHospsAux, dicPatients):
    for key in dicHospsAux.copy():
        nLocs = 0
        nServs = 0
        ep = dicHospsAux[key]
        for h in ep:
            if h.location is not None:
                nLocs += 1
            elif h.service is not None:
                nServs += 1

        # Episodes are removed        
        if nLocs == 0  or  nServs == 0:
            
            # Their Patients are removed
            patId = dicEpisodes[key].patient
            pat = dicPatients[patId]
            i = 0
            continuing = True
            while i<len(pat.episodes) and continuing:
                epAux = pat.episodes[i]
                if epAux.id == key:
                    continuing = False
                else:
                    i += 1
            dicPatients[patId].episodes.pop(i)

            # They are removed from the dictionaries
            dicEpisodes.pop(key)
            dicHospsAux.pop(key)


def unionHospLocSameLocation(dicHospsAux):
    for keyEp,ep in dicHospsAux.items():
        
        listRes = []
        hospBefore = None

        for hosp in ep:
            if hospBefore is not None:
                if hosp.location is not None:
                    if hosp.location == hospBefore.location:
                        lenListaRes = len(listRes)
                        listRes[lenListaRes-1].end = hosp.end
                    else:
                        listRes.append(hosp)
                else:
                    listRes.append(hosp)
            else:
                listRes.append(hosp)

            hospBefore = hosp
        
        dicHospsAux[keyEp] = listRes

def unionHospLocSameService(dicHospsAux):
    for keyEp,ep in dicHospsAux.items():
        
        listRes = []
        hospBefore = None

        for hosp in ep:
            if hospBefore is not None:
                if hosp.service is not None:
                    if hosp.service == hospBefore.service:
                        lenListaRes = len(listRes)
                        listRes[lenListaRes-1].end = hosp.end
                    else:
                        listRes.append(hosp)
                else:
                    listRes.append(hosp)
            else:
                listRes.append(hosp)

            hospBefore = hosp
        
        dicHospsAux[keyEp] = listRes 
        


######################################
# CREATION OF HOSPITALIZATION EVENTS #
######################################

def getIdHosp(idSimple, indLetter):
    indLetter += 1
    
    if indLetter >= len(abcCap):
        indAux = indLetter%len(abcCap)
        nExtraTimes = indLetter // len(abcCap)
        letras = "{}".format(abcCap[indAux])
        for i in range(nExtraTimes):
            letras += "{}".format(abcCap[indAux])
    
        idHosp = "{}{}".format(idSimple, letras)
    
    else:
        idHosp = "{}{}".format(idSimple, abcCap[indLetter])

    return idHosp, indLetter

def createHospitalizations(dicHospsAux, dicEpisodes):
    
    for ep in dicHospsAux.values():

        hospsLoc = []
        hospsServ = []
        for h in ep:
            if h.location is not None:
                hospsLoc.append(h)
            elif h.service is not None:
                hospsServ.append(h)

        episode = dicEpisodes[hospsLoc[0].id]
        indLetter = -1
        i = 0
        for hl in hospsLoc:

            continuar = True
            while continuar and i<len(hospsServ):
                hs = hospsServ[i]

                if hl.start == hs.start:
                    if hl.end == hs.end  or  hl.end < hs.end:
                        # Create Hospitalization that starts and ends with hl.start and hl.endend
                        idHosp, indLetter = getIdHosp(hl.id, indLetter)

                        hosp = Event(idHosp, episode.description, hl.start, hl.end, hl.location, hs.service, episode.id, EventType.Hospitalization)
                        dicEpisodes[hl.id].events.append(hosp)

                    else:   #hl.end > hs.end:
                        # Create Hospitalization that starts and ends with hs.start and hs.end 
                        idHosp, indLetter = getIdHosp(hl.id, indLetter)

                        hosp = Event(idHosp, episode.description, hs.start, hs.end, hl.location, hs.service, episode.id, EventType.Hospitalization)
                        dicEpisodes[hl.id].events.append(hosp)
                
                elif hl.start < hs.start:
                    if hl.end == hs.end  or  hl.end < hs.end:
                        # Create Hospitalization that starts and ends with hs.start and hl.end 
                        idHosp, indLetter = getIdHosp(hl.id, indLetter)

                        hosp = Event(idHosp, episode.description, hs.start, hl.end, hl.location, hs.service, episode.id, EventType.Hospitalization)
                        dicEpisodes[hl.id].events.append(hosp)
                    
                    else: # hl.end > hs.end
                        # Create Hospitalization that starts and ends with hs.start and hs.end 
                        idHosp, indLetter = getIdHosp(hl.id, indLetter)

                        hosp = Event(idHosp, episode.description, hs.start, hs.end, hs.location, hs.service, episode.id, EventType.Hospitalization)
                        dicEpisodes[hl.id].events.append(hosp)
                    
                else:   #elif hl.start > hs.start:
                    if hl.end == hs.end  or  hl.end < hs.end:
                        # Create Hospitalization that starts and ends with hl.start and hl.end 
                        idHosp, indLetter = getIdHosp(hl.id, indLetter)

                        hosp = Event(idHosp, episode.description, hl.start, hl.end, hl.location, hs.service, episode.id, EventType.Hospitalization)
                        dicEpisodes[hl.id].events.append(hosp)
                        
                    else:   # hl.end > hs.end:
                        # Create Hospitalization that starts and ends with hl.start and hs.end  
                        idHosp, indLetter = getIdHosp(hl.id, indLetter)

                        hosp = Event(idHosp, episode.description, hl.start, hs.end, hl.location, hs.service, episode.id, EventType.Hospitalization)
                        dicEpisodes[hl.id].events.append(hosp)

                if hl.end <= hs.end:
                    continuar = False 
                if hl.end >= hs.end:
                    i += 1



##########################################
# POST-PROCESSING HOSPITALIZATION EVENTS #
##########################################

def correctJumpBetweenYears(dicEpisodes):
    for keyEp in dicEpisodes.keys():
        ep = dicEpisodes[keyEp]
        if ep.start > ep.end:
            daysSubt = 365
            if isLeapyear(ep.start.year):
                daysSubt = 366
            dicEpisodes[keyEp].start = ep.start - timedelta(days=daysSubt)  
            
            for i in range(len(ep.events)):
                ev = ep.events[i]
                if ev.start > ep.end:
                    dicEpisodes[keyEp].events[i].start = ev.start - timedelta(days=daysSubt)
                elif ev.end > ep.end:
                    dicEpisodes[keyEp].events[i].end = ev.end - timedelta(days=daysSubt)

def deleteEpEvOutFilterYear(dicEpisodes, dicPatients, minYear, maxYear):
    epIdDelete = []

    for ep in dicEpisodes.values():
        if ep.start.year < minYear  or  ep.end.year > maxYear:
            epIdDelete.append(ep.id)

    # Removing Episodes
    for epId in epIdDelete:
        # Removing its Patient
        patId = dicEpisodes[epId].patient
        pat = dicPatients[patId]
        i = 0
        continuar = True
        while i<len(pat.episodes) and continuar:
            epAux = pat.episodes[i]
            if epAux.id == epId:
                continuar = False
            else:
                i += 1
        dicPatients[patId].episodes.pop(i)
        
        # Removing from the dictionary
        dicEpisodes.pop(epId)

def deleteHospsDurationCero(dicEpisodes):
    for keyEp in dicEpisodes.keys():
        ep = dicEpisodes[keyEp]
        listEvDurationMoreZero = []
        for ev in ep.events:
            if ev.type is EventType.Hospitalization:
                duration_in_m = getDurationInMinutes(ev.start, ev.end)
                if duration_in_m != 0:
                    listEvDurationMoreZero.append(ev)
            else:
                listEvDurationMoreZero.append(ev)

        dicEpisodes[keyEp].events = listEvDurationMoreZero

                

# The HU are added to the Hospitalizations of each Episode so that:
#   - All Hosps within an Episode that have been attended by a Service have the same HU
#   - But those from the next Episode must be attended by other HU      ->  This is a rotation of HUs between Episodes 
def changeServiceByUH(dicEpisodes, dicServices):
    
    # Since in 'transfers' file the Services were represented by their Abbreviation, we create this dictionary to go from Abbreviation to Id
    dicServsAux = {}
    for serv in dicServices.values():
        dicServsAux[serv.abrev] = serv.id

    # Array to know for each Service (with more than 1 HU) which is the next HU that should be used
    servKeys = list(dicServices.keys())
    servsUsedIndHU = {}
    for keyServ in servKeys:
        if len(dicServices[keyServ].hospUnits) > 1:
            servsUsedIndHU[keyServ] = 0
    
    # HU are added to the Hospitalizations of each Episode 
    for keyEp,ep in dicEpisodes.items():

        servicesUsed = []
        husUsed = []

        for i in range(len(ep.events)):
            hosp = ep.events[i]
            if hosp.type is EventType.Hospitalization:
                nameServ = dicEpisodes[keyEp].events[i].service
                idServ = dicServsAux[nameServ]
                dicEpisodes[keyEp].events[i].service = idServ   # The Abbreviation is changed to the Id

                if idServ not in servicesUsed:
                    servicesUsed.append(idServ)
                    serv = dicServices[idServ]
                    if len(serv.hospUnits) == 1:
                        husUsed.append(serv.hospUnits[0])
                        huId = serv.hospUnits[0]
                    else:
                        indHU = servsUsedIndHU[idServ]
                        huId = serv.hospUnits[indHU]
                        husUsed.append(huId)
                        
                        indHU = (indHU+1)%len(serv.hospUnits)   # Updated for next Episode
                        servsUsedIndHU[idServ] = indHU
                else:
                    indServ = servicesUsed.index(idServ)
                    huId = husUsed[indServ]
                dicEpisodes[keyEp].events[i].hospUnit = huId 


def renameHospitalizations(dicEpisodes):    # TODO: It does not take into account that there may be IDs with double letters, such as 123AA, 123ABA... but this type of ID should not be reached, as it would mean that the same Episode would have more than 26 Hospitalizations
    for keyEp in dicEpisodes.keys():
        ep = dicEpisodes[keyEp]
        countHosp = -1
        for i in range(len(ep.events)):
            h = ep.events[i] 
            if h.type is EventType.Hospitalization:
                countHosp += 1
                letter = h.id[-1:]
                if letter != abcCap[countHosp]:
                    idHosp = h.id[:-1]
                    idHosp += abcCap[countHosp]
                    dicEpisodes[keyEp].events[i].id = idHosp
                

def updateEpisodesToPatients(dicEpisodes, dicPatients):
    dicPatEp = {}
    for ep in dicEpisodes.values():
        idPat = ep.patient
        if idPat in dicPatEp:
            dicPatEp[idPat].append(ep)
        else:
            dicPatEp[idPat] = []
            dicPatEp[idPat].append(ep)

    for idPat in dicPatEp.keys():
        dicPatients[idPat].episodes = dicPatEp[idPat]



################
# FUNCION MAIN #
################

def parseHospitalizations(dicEpisodes, dicServices, dicPatients, minYearN, maxYearN, minYear, maxYear):
    
    # Auxiliary hospitalizations
    dicHospsAux = {}
    parseHospitalization_InBed(dicHospsAux, dicEpisodes, minYearN, maxYearN, minYear, maxYear)
    parseHospitalization_InService(dicHospsAux, dicEpisodes, minYearN, maxYearN, minYear)    

    # There are Episodes that only have Services or Locs
    deleteEpisodesWithout_LocsOrServs(dicEpisodes, dicHospsAux, dicPatients)
    # There are Hospitalizations that happen in the same Ward than the previous one 
    #unionHospLocSameLocation(dicHospsAux)  # This will be a change of Bed
    # There are Hospitalizations that happen in the same Service than the previous one 
    unionHospLocSameService(dicHospsAux)
    
    # Creation of Hospitalization Events
    createHospitalizations(dicHospsAux, dicEpisodes)

    # There may be Hospitalizations with duration = 0
    deleteHospsDurationCero(dicEpisodes)
    # There are Episodes/Events that end "before" their start due to the normalization of the years
    correctJumpBetweenYears(dicEpisodes)
    # After correcting the years, it may happen that the start or end of the Episodes are outside the defined range
    deleteEpEvOutFilterYear(dicEpisodes, dicPatients, minYear, maxYear)
    # There may again be Hospitalizations with duration = 0
    deleteHospsDurationCero(dicEpisodes)  
    
    # What is in hosp.hospUnits are Service ids, not Hospitalization Unit ids
    changeServiceByUH(dicEpisodes, dicServices)
    
    # Update the letters of the Hospitalization IDs
    renameHospitalizations(dicEpisodes) 

    