from datetime import datetime
from classes import *


###########################################################################
# A DICTIONARY IS CREATED IN WHICH EACH ROOM HAS ALL ITS HOSPITALIZATIONS #
###########################################################################

def getDicLocHosps(dicEpisodes):
    
    dicLocHosps = {}

    for ep in dicEpisodes.values():
        for hosp in ep.events:
            if hosp.type is EventType.Hospitalization:
                loc = hosp.location

                if loc in dicLocHosps:
                    dicLocHosps[loc].append(hosp)
                else:
                    dicLocHosps[loc] = []
                    dicLocHosps[loc].append(hosp)

    # Ordenar por hosp.start
    for loc in dicLocHosps.keys():
        dicLocHosps[loc].sort(key=lambda x: (x.start, x.end))

    return dicLocHosps



###################################
# EACH EVENT IS ASSIGNED TO A BED #
###################################

def eventsToBeds(dicLocHosps, dicRooms):

    minDatetime = datetime(1900, 1, 1, 00, 00, 00, 00000)
    for loc, hosps in dicLocHosps.items():
    
        # Get the Beds
        listBedsFree = []
        nameWard = "{}r".format(loc)
        ward = dicRooms[nameWard]
        for room in ward.values():
            for bed in room.beds:
                pairBedTime = [bed, minDatetime]
                listBedsFree.append(pairBedTime)
    
        # Greedy algorithm to put each event in the next free Bed    
        i = 0
        for event in hosps:
            found = False
            initI = i
            vueltas = 0
            while not found:
                if i == initI and vueltas > 0:
                    print("- event {} did not find a Bed in ward {}".format(event.id, loc))
                    print("\t- Start: {}\t- End: {}".format(event.start, event.end))
                    print("\n\tPAIRS")
                    for par in listBedsFree:
                        print("\t* Bed: {}\t- Date: {}".format(par[0], par[1]))
                    exit()
                else:
                    vueltas += 1

                pairBT = listBedsFree[i]
                if pairBT[1] < event.start:
                    found = True
                    pairBT[1] = event.end
                    event.location = pairBT[0]

                i = (i+1)%len(listBedsFree)



#####################
# FUNCION PRINCIPAL #
#####################

def distributeEvents(dicEpisodes, dicRooms):
    dicLocHosps = getDicLocHosps(dicEpisodes)
    eventsToBeds(dicLocHosps, dicRooms)






