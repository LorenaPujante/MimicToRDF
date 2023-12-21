
import math 
from classes import *


##################################
# SET NUMBER OF EVENTS PER MONTH #
##################################

def getEventsPerMonth(dicEpisodes, maxEvents):
    
    if maxEvents == 0:
        eventsPerMonthList = None
    
    else:
        
        eventsPerMonth = math.floor(maxEvents/12)
        
        # Get how many Events there are in each month
        eventsPerMonthList = getNumEventsPerMonth(dicEpisodes)
        epml_aux = []
        for m in eventsPerMonthList:
            epml_aux.append(m)  # Auxiliary variable to not lose the information, since the other array will be overwritten

        # See which months have fewer Events than average 
        dicMonthsLess = getMonthsLessEvents(eventsPerMonthList, eventsPerMonth)
        
        # And distribute the difference between the rest of the months
        eventsToRepartir = 0
        for pair in dicMonthsLess.values():
            eventsToRepartir += pair[1]
        eventsSum = eventsToRepartir/(12-len(dicMonthsLess))
        eventsSum = math.floor(eventsSum)
        newEventsPerMonth = eventsPerMonth + eventsSum

        # Set the new number of Events in each month
        total = 0
        for i in range(12):
            if eventsPerMonthList[i] > newEventsPerMonth:  
                eventsPerMonthList[i] = newEventsPerMonth
            total += eventsPerMonthList[i]
    
        # If there are still Events to be distributed to reach maxEvents, these are added one by one to those months that may still have more Events
        shareRestEvents(total, maxEvents, newEventsPerMonth, eventsPerMonthList, epml_aux)
        
        # Add a small margin to the months that may still have more events
        # This is because in December, if you go strictly, there are still many events to add
        # Reason:
        # Many of the December Events belong to November Episodes.
        # And if November is full -> There will be Episodes that will not be included -> And, consequently, their December Events will not be included either
        addLoosenessToEventsPerMonth(eventsPerMonthList, epml_aux)

    return eventsPerMonthList


# Get how many Events start each month
def getNumEventsPerMonth(dicEpisodes):
    eventsPerMonthList = []
    
    for i in range(12):
        eventsPerMonthList.append(0)
    for ep in dicEpisodes.values():
        for ev in ep.events:
            start = ev.start
            startMonth = start.month
            eventsPerMonthList[startMonth-1] += 1

    return eventsPerMonthList


# Get which months have fewer events than they should by averaging maxEvents/12
def getMonthsLessEvents(eventsPerMonthList, eventsPerMonth):
    dicMonthsLess = {}
    for i in range(12):
        events = eventsPerMonthList[i]
        if events < eventsPerMonth:
            dicMonthsLess[i+1] = []
            dicMonthsLess[i+1].append(events)
            dicMonthsLess[i+1].append(eventsPerMonth-events)
            
    return dicMonthsLess        


# Distribute the unassigned number of Events among the months that still allow more Events
def shareRestEvents(totalEvents, maxEvents, eventsPerMonth, eventsPerMonthList, epml_aux):
    if totalEvents < maxEvents:

        diff = maxEvents-totalEvents
        
        # List with the months to which more Events can still be added
        monthsCanMore = []
        for i in range(12):
            if epml_aux[i] > eventsPerMonth:
                monthsCanMore.append(i)

        # An Event is added to each Month as long as that Month has enough Events
        k = 0
        for i in range(diff):
            continuing = True
            initK = k
            while continuing:
                ind = monthsCanMore[k]
                if eventsPerMonthList[ind]+1 <= epml_aux[ind]: 
                    eventsPerMonthList[ind] += 1
                    continuing = False
                
                k = (k+1)%len(monthsCanMore)
                if k == initK: 
                    continuing = False


# Add slack to the number of Events you can have each month
def addLoosenessToEventsPerMonth(eventsPerMonthList, epml_aux):
    potentialIncrease = 5
    for i in range(12): 
        if eventsPerMonthList[i] < epml_aux[i]: 
            if eventsPerMonthList[i] + potentialIncrease <= epml_aux[i]:
                eventsPerMonthList[i] += potentialIncrease
            else:
                potentialIncrease = epml_aux[i]-eventsPerMonthList[i]
                eventsPerMonthList[i] = epml_aux[i]
            potentialIncrease += 5



#######################################
# DELETE LEFTOVER EVENTS AND EPISODES #
#######################################

def reachMaxEvents(dicEpisodes, dicPatients, eventsPerMonth):

    if eventsPerMonth is not None:

        # We order the Episodes so that:
        #  - Let's first include those that have a higher proportion of Hospitalizations by TestMicro
        #  - The last Episodes to add are those that only have Hospitalizations and 0 TM
        sortEps = sortEpisodesByHospsAndTM(dicEpisodes)

    
        # Events are distributed by their Start Month
        dicEvsByMonth = {}
        for i in range(12):
            dicEvsByMonth[i] = []
        for ep in sortEps:
            for ev in ep.events:
                month = ev.start.month
                dicEvsByMonth[month-1].append(ev)
        
        
        # List to save the ID of the included Episodes
        epIncluded = []
        evsPerMonthCount = []
        for i in range(12):
            evsPerMonthCount.append(0)

        # Events are 'added' for each Month
        for i in range(12):
            evs = dicEvsByMonth[i]
            
            # All Events that begin in the Month are traversed until the quota for the Month has been filled.
            # For each Event it is checked if its Episode has already been added:
            # - If NOT, this Event and all the Events of the same Episode are added (each one in its corresponding month)
            # - If YES, move on to the next Event
            continuing = True
            k = 0
            while continuing and k<len(evs):
                ev = evs[k]
                if len(epIncluded) == 0 or (ev.episode != epIncluded[len(epIncluded)-1]  and  ev.episode not in epIncluded):  # The first 2 checks are so that the last check (the most expensive) is done as little as possible.
                    ep = dicEpisodes[ev.episode]

                    # To prevent an Event that starts in a month after the start of its Episode from being included when this Episode has NOT been included
                    evFirst = ep.events[0]
                    if evFirst.id == ev.id  or  evFirst.start.month >= ev.start.month:
                        evsPerMonthCount[i] += 1
                        epIncluded.append(ev.episode)

                        for j in range(len(ep.events)-1):  # The -1 (and the next +1) is because the first Event of the Episode has already been added
                            ev2 = ep.events[j+1]
                            evsPerMonthCount[ev2.start.month-1] += 1

                        if evsPerMonthCount[i] >= eventsPerMonth[i]:
                            continuing = False

                k += 1

        # Delete Episodes not included
        deleteEpisodesOutOfEventsPerMonth(dicEpisodes, epIncluded, dicPatients)           


# Sort the Episodes according to their number of Hospitalizations and TestMicro
def sortEpisodesByHospsAndTM(dicEpisodes):
    for idEp, ep in dicEpisodes.items():
        nHosp = 0
        nTM = 0
        for ev in ep.events:
            if ev.type is EventType.Hospitalization:
                nHosp += 1
            elif ev.type is EventType.TestMicro:
                nTM += 1

        if nTM == 0:
            hospPerTM = 0
        else:
            hospPerTM = nHosp/nTM
        dicEpisodes[idEp].hospPerTM = hospPerTM
    
    sortEps = list(dicEpisodes.values())
    sortEps.sort(key=lambda k: k.hospPerTM, reverse=True)

    return sortEps


# Delete Episodes not included in the final result
def deleteEpisodesOutOfEventsPerMonth(dicEpisodes, epIncluded, dicPatients):
    epKeys = list(dicEpisodes.keys())
    for key in epKeys:
        if key not in epIncluded:

            # The Episode is deleted from its Patient
            patId = dicEpisodes[key].patient
            pat = dicPatients[patId]
            i = 0
            continuing = True
            while i<len(pat.episodes) and continuing:
                ep = pat.episodes[i]
                if ep.id == key:
                    continuing = False
                else:
                    i += 1
            dicPatients[patId].episodes.pop(i)

            # Episode removed from dictionary
            dicEpisodes.pop(key)     
