
from datetime import datetime

from classes import *
from variablesFilesNormYear import *
from parserHospitalizations import parseHospitalizations
from trimEvents import getEventsPerMonth, reachMaxEvents



##################
# MICROORGANISMS #
##################

def parseMicroorganims():

    dicMicroorganisms = {}

    nameFile = setFileInput(filesName["micro"])
    with open(nameFile) as file:
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')
            
                id = int(line[0])
                description = line[1]
                description = description[:-1]
                if description[0] == '"':
                    description = description[1:]
                if description[len(description)-1] == '"':
                    description = description[:-1]            
                
                microorganism = Microorganism(id,description)
                
                dicMicroorganisms[id] = microorganism

    file.close()

    return dicMicroorganisms



############
# EPISODES #
############

def parseEpisodes(dicPatients, minYearN, maxYearN, minYear, maxYear):
    
    dicEpisodes = {}

    nameFile = setFileOutput(filesName["episode"], minYearN, maxYearN)
    with open(nameFile) as file:
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')
            
                start_str = line[2]
                start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                end_str = line[3]
                end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
            
                if start.year >= minYear  and  end.year <= maxYear:
    
                    patId = int(line[0])
                    id = int(line[1])
                    description = line[4]
                    description = description[:-1]
                
                    episode = Episode(id, description, start, end, patId)
                    dicEpisodes[id] = episode

                    patientId = int(line[0])
                    dicPatients[patientId].episodes.append(episode)

    file.close()

    return dicEpisodes



#################################
# EVENTS (NOT HOSPITALIZATIONS) #
#################################

def parseTestsMicro(dicEpisodes, dicMicroorganisms, minYearN, maxYearN, minYear, maxYear):
    nameFile = setFileOutput(filesName["ev_tm"], minYearN, maxYearN)
    with open(nameFile) as file:
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')
            
                start_str = line[3]
                start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                end = start
                
                episodeId = int(line[1])

                if start.year >= minYear  and  end.year <= maxYear  and  episodeId in dicEpisodes:

                    idNum = int(line[0])
                    id = "{}tm".format(idNum)
                    
                    testMicro = Event(id, "testMicro", start, end, None, None, episodeId, EventType.TestMicro)

                    microorgId = int(line[2])
                    testMicro.extra1 = dicMicroorganisms[microorgId]

                    mmr = line[4]
                    mmr = mmr[:-1]
                    if mmr == "0":
                        testMicro.extra2 = False
                    elif mmr == "1":
                        testMicro.extra2 = True

                    dicEpisodes[episodeId].events.append(testMicro)

    file.close()


def parseDeaths(dicEpisodes, minYearN, maxYearN, minYear, maxYear):
    nameFile = setFileOutput(filesName["ev_death"], minYearN, maxYearN)
    with open(nameFile) as file:
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')

                start_str = line[3]
                start_str = start_str[:-1]
                start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                end = start
                
                episodeId = int(line[2])
                
                if start.year >= minYear  and  end.year <= maxYear  and  episodeId in dicEpisodes:
                    
                    idNum = int(line[0])
                    id = "{}death".format(idNum)

                    episodeId = int(line[2])
                    episode = dicEpisodes[episodeId]
                    if end > episode.end:
                        start = episode.end
                        end = episode.end

                    death = Event(id, "death", start, end, None, None, episodeId, EventType.Death)

                    dicEpisodes[episodeId].events.append(death)

    file.close()



###################
# POST-PROCESSING #
###################

def removeEpisodesWithNoHospitalizations(dicEpisodes, dicPatients):
    
    # Get the Episodes with no Hospitalizations
    epNoHosp = []
    for ep in dicEpisodes.values():
        nHosps = 0
        for ev in ep.events:
            if ev.type is EventType.Hospitalization:
                nHosps += 1
        if nHosps == 0:
            epNoHosp.append(ep.id)
    
    # Deleting Episodes
    for epId in epNoHosp:
        
        # Episode is removed from its Patient
        patId = dicEpisodes[epId].patient
        pat = dicPatients[patId]
        i = 0
        continuing = True
        while i<len(pat.episodes) and continuing:
            ep = pat.episodes[i]
            if ep.id == epId:
                continuing = False
            else:
                i += 1
        dicPatients[patId].episodes.pop(i)

        # Episode is removed from the dictionary
        dicEpisodes.pop(epId)


def removePatientsWithNoEpisode(dicPatients, dicEpisodes):
    
    patsWithEps = []
    
    for ep in dicEpisodes.values():
        idPat = ep.patient
        patsWithEps.append(idPat)

    keysPats = list(dicPatients.keys())
    for k in keysPats:
        if k not in patsWithEps:
            dicPatients.pop(k)


def removeMicroorganismsWithNoTestMicro(dicMicroorganisms, dicEpisodes):

    orgsWithEvs = []

    for ep in dicEpisodes.values():
        for ev in ep.events:
            if ev.type is EventType.TestMicro:
                idMicroorg = ev.extra1.id
                orgsWithEvs.append(idMicroorg)

    keysOrgs = list(dicMicroorganisms.keys())
    for k in keysOrgs:
        if k not in orgsWithEvs:
            dicMicroorganisms.pop(k)


# Update Death Events' start and end to match the end of the Episode
def updateDatetime_Death(dicEpisodes):
    for idEp, ep in dicEpisodes.items():
        i = 0
        continuing = True
        while i<len(ep.events) and continuing:
            ev = ep.events[i]
            if ev.type is EventType.Death:
                if ev.start < ep.end:
                    dicEpisodes[idEp].events[i].start = ep.end
                    dicEpisodes[idEp].events[i].end = ep.end
                    
                continuing = False
            i += 1


# Update TestMicro Events' start and end from those that are after the end of their Episode
def updateDatetime_TestMicro(dicEpisodes):
    
    for idEp in dicEpisodes.keys():
    
        # The Events of the Episode are ordered from before to after
        dicEpisodes[idEp].events.sort(key=lambda k: k.start)
        ep = dicEpisodes[idEp]
        
        # The First and Last Hospitalizations are obtained
        listAux = sorted(ep.events, key=lambda k: k.type.name)
        continuing = True
        i = 0
        firstHosp = None 
        lastHosp = None
        while i<len(listAux) and continuing:
            ev = listAux[i]
            if ev.type is EventType.Hospitalization:
                if firstHosp is None:
                    firstHosp = ev
                lastHosp = ev
            elif ev.type is not EventType.Hospitalization  and  lastHosp is not None:
                continuing = False 

            i += 1

        # Two dictionaries are created that store the TestMicro that are before or after the Episode, and their position within the Episode
        listBefore = {}
        listAfter = {}

        i = 0
        continuing = True
        while i<len(ep.events) and continuing:
            ev = ep.events[i]
            
            if ev.type is EventType.TestMicro:
                if ev.start < ep.start:
                    listBefore[i] = ev
                if ev.end > ep.end:
                    listAfter[i] = ev

            i += 1

        # All TestMicro that are Before will have as their start and end the halfway point of the First Hospitalization
        if len(listBefore) > 0:
            mean_dt = getMeanDatetime(firstHosp)
            for i, ev in listBefore.items():
                dicEpisodes[idEp].events[i].start = mean_dt
                dicEpisodes[idEp].events[i].end = mean_dt
                
        # All the TestMicro that are After will have as their start and end the intermediate point of the Last Hospitalization
        if len(listAfter) > 0:
            mean_dt = getMeanDatetime(lastHosp)
            for i, ev in listAfter.items():
                dicEpisodes[idEp].events[i].start = mean_dt
                dicEpisodes[idEp].events[i].end = mean_dt


        # The Events of the Episode are reordered so that updated TMs are in their corresponding position
        dicEpisodes[idEp].events.sort(key=lambda k: k.start)
                

def getMeanDatetime(ev):
    start_ts = ev.start.timestamp()
    end_ts = ev.end.timestamp()
    mean_ts = (start_ts + end_ts)/2
    mean_dt = datetime.fromtimestamp(mean_ts)
    
    return mean_dt       



################
# FUNCION MAIN #
################

def parseEpisodesAndEvents(dicPatients, dicServices, minYearN, maxYearN, minYear, maxYear, maxEvents):
    
    dicEpisodes = parseEpisodes(dicPatients, minYearN, maxYearN, minYear, maxYear)
    dicMicroorganisms = parseMicroorganims()    
    parseDeaths(dicEpisodes, minYearN, maxYearN, minYear, maxYear)
    parseTestsMicro(dicEpisodes, dicMicroorganisms, minYearN, maxYearN, minYear, maxYear)

    parseHospitalizations(dicEpisodes, dicServices, dicPatients, minYearN, maxYearN, minYear, maxYear)  

    # There may be Episodes that only have TestMicro    ->  They will be removed
    removeEpisodesWithNoHospitalizations(dicEpisodes, dicPatients)
    
    # There may be Deaths that happen before the Episode ends.
    updateDatetime_Death(dicEpisodes)
    # There may be TestMicro that happen before the Episode starts or after it ends
    updateDatetime_TestMicro(dicEpisodes)

    # Calculate what is the maximum number of Events that must be in each month to achieve maxEvents
    eventsPerMonthList = getEventsPerMonth(dicEpisodes, maxEvents)
    # Get there to be maxEvents Events, eliminating the excess Events and Episodes
    reachMaxEvents(dicEpisodes, dicPatients, eventsPerMonthList)
        
    # Remove the Patients who are without Episodes now
    removePatientsWithNoEpisode(dicPatients, dicEpisodes)
    # Remove the Microorganisms that aren't found by any TestMicro
    removeMicroorganismsWithNoTestMicro(dicMicroorganisms, dicEpisodes)


    return dicEpisodes, dicMicroorganisms





