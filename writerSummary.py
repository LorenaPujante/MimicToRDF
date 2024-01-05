
import os
from classes import *
from variablesFiles import getTwoLastDigitsNumber
from parserPhysicalHospital import splitIdRoom


##################
# INITIALIZATION #
##################

def setFolderSummary(folder):
    global folderOutput
    folderOutput = folder
    if (not os.path.exists(folderOutput)):
        os.makedirs(folderOutput)



###################
# SUMMARY WRITING #
###################

def writeSummaryPEE(file, dicPatients):

    file.write("\n\t- NUM PATIENTS, EPISODES, EVENTS\n")

    nPatients = len(dicPatients.keys())
    file.write("\nPatients: {}".format(nPatients))

    nEpisodes = 0
    nEvents = 0
    for patient in dicPatients.values():
        nEpisodes += len(patient.episodes)    
        for ep in patient.episodes:
            nEvents += len(ep.events)

    file.write("\nEpisodes: {}".format(nEpisodes))
    file.write("\nEvents: {}\n".format(nEvents))


def writeSummaryCorridors(file, dicCorridors):

    file.write("\n\n\t- CORRIDORS\n")

    listSurg = []
    listMix = []
    listMed = []
    listNeo = []

    for c in dicCorridors.values():
        if 'Surgical' in c.description:
            listSurg.append(c.id)
        elif 'Mixed' in c.description:
            listMix.append(c.id)
        elif 'Medical' in c.description:
            listMed.append(c.id)
        elif 'Neonatal' in c.description:
            listNeo.append(c.id)

    file.write("\nTOTAL: {} Corridors\n".format(len(dicCorridors)))

    file.write("\nSURGICAL ({}):\t{}".format(len(listSurg), listSurg))
    file.write("\nMIX ({}):\t{}".format(len(listMix), listMix))
    file.write("\nMEDICAL ({}):\t{}".format(len(listMed), listMed))
    file.write("\nNEONATAL ({}):\t{}\n".format(len(listNeo), listNeo))


def writeSummaryRooms(file, listsRooms):
    
    file.write("\n\n\t- ROOMS ORDERED BY TYPE (Service type that most uses the Room)\n")

    listSurg = listsRooms[0]
    listMix = listsRooms[1]
    listMed = listsRooms[2]
    listNeo = listsRooms[3]

    totalRooms = len(listSurg) + len(listMix) + len(listMed) + len(listNeo)
    file.write("\nTOTAL: {} Rooms\n".format(totalRooms))

    file.write("\nSURGICAL ({}):\t{}".format(len(listSurg), listSurg))
    file.write("\nMIX ({}):\t{}".format(len(listMix), listMix))
    file.write("\nMEDICAL ({}):\t{}".format(len(listMed), listMed))
    file.write("\nNEONATAL ({}):\t{}\n".format(len(listNeo), listNeo))


def writeSummaryBeds(file, listsRooms, dicRooms):

    file.write("\n\n\t- ROOMS AND THEIR BEDS\n")

    listSurg = listsRooms[0]
    listMix = listsRooms[1]
    listMed = listsRooms[2]
    listOther = listsRooms[3]

    toWrite = ""
    nBedsSurg = 0
    for idRoom in listSurg:
        idWard, numRoom = splitIdRoom(idRoom) 
        room = dicRooms[idWard][numRoom]
        nBeds = len(room.beds)
        toWrite += "{}: {} beds\n".format(room.description, nBeds)
        nBedsSurg += nBeds
    file.write("\nSURGICAL: {} Beds\n".format(nBedsSurg))
    file.write(toWrite)

    toWrite = ""
    nBedsMix = 0
    for idRoom in listMix:
        idWard, numRoom = splitIdRoom(idRoom) 
        room = dicRooms[idWard][numRoom]
        nBeds = len(room.beds)
        toWrite += "{}: {} beds\n".format(room.description, nBeds)
        nBedsMix += nBeds
    file.write("\nMIX: {} Beds\n".format(nBedsMix))
    file.write(toWrite)       

    toWrite = ""
    nBedsMed = 0
    for idRoom in listMed:
        idWard, numRoom = splitIdRoom(idRoom) 
        room = dicRooms[idWard][numRoom]
        nBeds = len(room.beds)
        toWrite += "{}: {} beds\n".format(room.description, nBeds)
        nBedsMed += nBeds
    file.write("\nMED: {} Beds\n".format(nBedsMed))
    file.write(toWrite) 

    toWrite = ""
    nBedsNeo = 0
    for idRoom in listOther:
        idWard, numRoom = splitIdRoom(idRoom) 
        room = dicRooms[idWard][numRoom]
        nBeds = len(room.beds)
        toWrite += "{}: {} beds\n".format(room.description, nBeds)
        nBedsNeo += nBeds
    file.write("\nNEONATAL: {} Beds\n".format(nBedsNeo))
    file.write(toWrite) 
    
    totalBeds = nBedsSurg + nBedsMix + nBedsMed + nBedsNeo
    file.write("\nTOTAL: {} Beds".format(totalBeds))


#################
# MAIN FUNCTION #
#################

def writeSummarys(dicPatients, dicCorridors, dicRooms, listsRooms, minYearN, maxYearN, minYear, maxYear, maxEvents):
    minYearN_2digits = getTwoLastDigitsNumber(minYearN)
    maxYearN_2digits = getTwoLastDigitsNumber(maxYearN)
    minYear_2digits = getTwoLastDigitsNumber(minYear)
    maxYear_2digits = getTwoLastDigitsNumber(maxYear)
    if maxEvents == 0:
        maxEvents_div1000 = "all"
    else:
        maxEvents_div1000 = int(maxEvents/1000)

    nameFile = '\\summary_{}-{}__{}-{}__{}.txt'.format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    fichero = open(folderOutput + nameFile, 'w')
    
    writeSummaryPEE(fichero, dicPatients)
    writeSummaryCorridors(fichero, dicCorridors)
    writeSummaryRooms(fichero, listsRooms)
    writeSummaryBeds(fichero, listsRooms, dicRooms)

    fichero.close()
