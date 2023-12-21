
import os
from classes import *
from variablesFilesNormYear import getTwoLastDigitsNumber
from parserPhysicalHospital import splitIdRoom


##################
# INICIALIZACION #
##################

def setFolderSummary(folder):
    global folderOutput
    folderOutput = folder
    if (not os.path.exists(folderOutput)):
        os.makedirs(folderOutput)



#########################
# ESCRITURA DE RESMUNES #
#########################

def writeResumePEE(file, dicPatients):

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


def writeResumeCorridors(file, dicCorridors):

    file.write("\n\n\t- CORRIDORS\n")

    nSurg = 0
    listSurg = []
    nMix = 0
    listMix = []
    nMed = 0
    listMed = []
    nOther = 0
    listOther = []

    for c in dicCorridors.values():
        if 'Surgical' in c.description:
            nSurg += 1
            listSurg.append(c.id)
        elif 'Mixed' in c.description:
            nMix += 1
            listMix.append(c.id)
        elif 'Medical' in c.description:
            nMed += 1
            listMed.append(c.id)
        elif 'Neonatal' in c.description:
            nOther += 1
            listOther.append(c.id)

    file.write("\nTOTAL: {} Corridors\n".format(len(dicCorridors)))

    file.write("\nSURGICAL ({}):\t{}".format(len(listSurg), listSurg))
    file.write("\nMIX ({}):\t{}".format(len(listMix), listMix))
    file.write("\nMEDICAL ({}):\t{}".format(len(listMed), listMed))
    file.write("\nOTHER ({}):\t{}\n".format(len(listOther), listOther))


def writeResumeRooms(file, listsRooms):
    
    file.write("\n\n\t- ROOMS ORDERED BY TYPE (Service type that most uses the Room)\n")

    listSurg = listsRooms[0]
    listMix = listsRooms[1]
    listMed = listsRooms[2]
    listOther = listsRooms[3]

    totalRooms = len(listSurg) + len(listMix) + len(listMed) + len(listOther)
    file.write("\nTOTAL: {} Rooms\n".format(totalRooms))

    file.write("\nSURGICAL ({}):\t{}".format(len(listSurg), listSurg))
    file.write("\nMIX ({}):\t{}".format(len(listMix), listMix))
    file.write("\nMEDICAL ({}):\t{}".format(len(listMed), listMed))
    file.write("\nOTHER ({}):\t{}\n".format(len(listOther), listOther))


def writeResumeBeds(file, listsRooms, dicRooms):

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
    nBedsOther = 0
    for idRoom in listOther:
        idWard, numRoom = splitIdRoom(idRoom) 
        room = dicRooms[idWard][numRoom]
        nBeds = len(room.beds)
        toWrite += "{}: {} beds\n".format(room.description, nBeds)
        nBedsOther += nBeds
    file.write("\nOTHER: {} Beds\n".format(nBedsOther))
    file.write(toWrite) 
    
    totalBeds = nBedsSurg + nBedsMix + nBedsMed + nBedsOther
    file.write("\nTOTAL: {} Beds".format(totalBeds))


#################
# MAIN FUNCTION #
#################

def writeResumes(dicPatients, dicCorridors, dicRooms, listsRooms, minYearN, maxYearN, minYear, maxYear, maxEvents):
    minYearN_2digits = getTwoLastDigitsNumber(minYearN)
    maxYearN_2digits = getTwoLastDigitsNumber(maxYearN)
    minYear_2digits = getTwoLastDigitsNumber(minYear)
    maxYear_2digits = getTwoLastDigitsNumber(maxYear)
    if maxEvents == 0:
        maxEvents_div1000 = "all"
    else:
        maxEvents_div1000 = int(maxEvents/1000)

    nameFile = '\\resumen_{}-{}__{}-{}__{}.txt'.format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    fichero = open(folderOutput + nameFile, 'w')
    
    writeResumePEE(fichero, dicPatients)
    writeResumeCorridors(fichero, dicCorridors)
    writeResumeRooms(fichero, listsRooms)
    writeResumeBeds(fichero, listsRooms, dicRooms)

    fichero.close()