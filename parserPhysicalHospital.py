import math

from classes import *
from variablesFilesNormYear import *


##############################
# CREATION OF ROOMS AND BEDS #
##############################

def createRoomsAndBeds():
    dicRooms = {}
    dicBeds = {}

    nameFile = setFileInput(filesName["room"])
    with open(nameFile) as file:
        
        idBedNum = 0
        
        for lineString in file:

            lineString = str(lineString)
            if lineString[0] == 'R':
                line = lineString.split(',')

                descInit = line[0]
                idInit = line[1]
                nBeds = int(line[2])
                nRooms = line[3]
                nRooms = nRooms[:-1]
                nRooms = int(nRooms)

                dicRooms[idInit] = {}

                a = nRooms*10
                if nBeds < 10:
                    aux = 2
                elif a == nBeds:
                    aux = 0
                else:
                    b = nRooms*9
                    if b >= nBeds:
                        c = b - nBeds
                        aux = -1
                    else:
                        c = nBeds - b
                        aux = 1

                for i in range(nRooms):
                    
                    # The Room is created
                    idRoom = "{}_{}".format(idInit,i)
                    descRoom = "{}_{}".format(descInit,i)
                    room = Room(idRoom, descRoom)

                    # The Beds of each Room are created
                    if aux == 2:
                        bedsPerRoom = nBeds
                    elif aux == 0:
                        bedsPerRoom = 10
                    elif aux == 1:
                        bedsPerRoom = 9
                        if i < c:
                            bedsPerRoom += 1
                    else:
                        bedsPerRoom = 9
                        cAux = c
                        while cAux > nRooms:
                            bedsPerRoom -= 1
                            bAux = nRooms * bedsPerRoom
                            cAux = bAux - nBeds
                        if i < cAux:
                            bedsPerRoom -= 1
                        
                    beds = []
                    for j in range(bedsPerRoom):
                        idBed = "{}b".format(idBedNum)
                        descBed = "BED{}_{}".format(j,descRoom)
                        bed = Bed(idBed, descBed)
                        bed.parent = idRoom

                        beds.append(bed.id)
                        dicBeds[bed.id] = bed
                        
                        idBedNum += 1

                    room.beds = beds

                    dicRooms[idInit][i] = room

    return dicRooms, dicBeds


# NEIGHBORHOOD BETWEEN BEDS
def setNeighbourBeds(beds, dicBeds):
    if len(beds) == 2:
        dicBeds[beds[0]].nextTo.append(dicBeds[beds[1]].id)
        dicBeds[beds[1]].nextTo.append(dicBeds[beds[0]].id)
    elif len(beds) > 2:
        for i in range(len(beds)):
            if i%2 == 0:
                if i+1 < len(beds):
                    dicBeds[beds[i]].opposite.append(dicBeds[beds[i+1]].id)
                    dicBeds[beds[i+1]].opposite.append(dicBeds[beds[i]].id)
                if i+2 < len(beds):
                    dicBeds[beds[i]].nextTo.append(dicBeds[beds[i+2]].id)
                    dicBeds[beds[i+2]].nextTo.append(dicBeds[beds[i]].id)
            else:
                if i+2 < len(beds):
                    dicBeds[beds[i]].nextTo.append(dicBeds[beds[i+2]].id)
                    dicBeds[beds[i+2]].nextTo.append(dicBeds[beds[i]].id)


# GROUP ROOMS BY TYPE ACCORDING TO PREPARED FILE (Majority Type of Service in Events)
def parseRoomsType(dicRooms):

    listSurg = []
    listMed = []
    listMix = []
    listOther = []

    nameFile = setFileInput(filesName["roomType"])
    with open(nameFile) as file:
        
        for lineString in file:

            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')

                idWard = line[0]
                typeWard = line[1]
                typeWard = typeWard[:-1]

                dicWard = dicRooms[idWard]
                for key, room in dicWard.items():
                    if typeWard == "Med":
                        listMed.append(room.id)
                    if typeWard == "Surg":
                        listSurg.append(room.id)
                    if typeWard == "Mix":
                        listMix.append(room.id)
                    if typeWard == "Other":
                        listOther.append(room.id)

    return listSurg, listMed, listMix, listOther



##############################
# NEIGHBORHOOD BETWEEN ROOMS #
##############################

def setRoomsNeighbours(idCorr, indRoom, dicCorridors, dicRooms, listRooms):
    corr = dicCorridors[idCorr]
    nameCorr = getNameCorridor(corr.description)

    lenRooms = len(corr.rooms)
    lenRoomsEven = lenRooms%2==0
    for i in range(lenRooms):
        
        room = dicCorridors[idCorr].rooms[i]
        idWard, numRoom = splitIdRoom(room.id)

        # Neighboring rooms in the same Hall
        if i%2 == 0:
            if i+1 < lenRooms:
                dicCorridors[idCorr].rooms[i].opposite.append(corr.rooms[i+1].id)
                dicCorridors[idCorr].rooms[i+1].opposite.append(room.id)
            
            if i+2 < lenRooms:
                dicCorridors[idCorr].rooms[i].nextTo.append(corr.rooms[i+2].id)
                dicCorridors[idCorr].rooms[i+2].nextTo.append(room.id)
                  
        else:
            if i+2 < lenRooms:
                dicCorridors[idCorr].rooms[i].nextTo.append(corr.rooms[i+2].id)
                dicCorridors[idCorr].rooms[i+2].nextTo.append(room.id)
        
        # Neighboring rooms of the Neighboring Hall 
        if lenRoomsEven:
            if i == lenRooms-1:
                corrNeighId = corr.nextTo[1]
                if corrNeighId is not None:
                    corrNeigh = dicCorridors[corrNeighId]
                    if len(corrNeigh.rooms) >= 2:
                        roomNeigh = corrNeigh.rooms[1]
                        dicCorridors[idCorr].rooms[i].nextTo.append(roomNeigh.id)
                        dicCorridors[corrNeighId].rooms[1].nextTo.append(room.id)

            elif i == lenRooms-2:
                corrNeighId = corr.nextTo[1]
                if corrNeighId is not None:
                    corrNeigh = dicCorridors[corrNeighId]
                    if len(corrNeigh.rooms) >= 1:
                        roomNeigh = corrNeigh.rooms[0]
                        dicCorridors[idCorr].rooms[i].nextTo.append(roomNeigh.id)
                        dicCorridors[corrNeighId].rooms[0].nextTo.append(room.id)

        else:
            if i == lenRooms-1:
                corrNeighId = corr.nextTo[1]
                if corrNeighId is not None:
                    corrNeigh = dicCorridors[corrNeighId]
                    if len(corrNeigh.rooms) >= 1:
                        roomNeigh = corrNeigh.rooms[0]
                        dicCorridors[idCorr].rooms[i].nextTo.append(roomNeigh.id)
                        dicCorridors[corrNeighId].rooms[0].nextTo.append(room.id)
        
        # Neighboring rooms of the Surgical corridor
        if nameCorr != 'Surgical':
            if i%2 == 0:
                upperRoomKey = listRooms[indRoom+1]
                idWardUpper, numRoomUpper = splitIdRoom(upperRoomKey)
                upperRoom = dicRooms[idWardUpper][numRoomUpper]
                dicRooms[idWard][numRoom].nextTo.append(upperRoom.id)
                dicRooms[idWardUpper][numRoomUpper].nextTo.append(room.id)     
            
                if i==lenRooms-1:   # Because of the gap left at the end of the hallway when the number of rooms is odd.
                    indRoom += 1

            indRoom +=1

    return indRoom



###############################################################################
# CORRIDORS ARE CREATED                                                       #
#-----------------------------------------------------------------------------#
# SO THAT THERE ARE NO MORE THAN 20 ROOMS PER CORRIDOR (WITHOUT EXCEPTIONS)   #
# AND THAT EACH GROUP OF ROOMS (PER SERVICE) IS IN ITS CORRESPONDING CORRIDOR #
# #############################################################################
 
def createCorridors(dicCorridors, dicRooms, listRooms, nameBaseCorr, nCorr):

    nCorridors = math.ceil(len(listRooms)/20)
    restRooms = len(listRooms)%20
    nCorrsToCreate = nCorridors
    if restRooms < 20/2  and  getNameCorridor(nameBaseCorr) in ['Mixed', 'Medical']:
        nCorrsToCreate = nCorridors-1   # This is done so that in the intermediate services (Mixed and Medical) there is not a last corridor with few Rooms, better one a little longer
        if nCorrsToCreate == 0:
            nCorrsToCreate = 1
    
    idsCorr = []
    
    for i in range(nCorrsToCreate):    
        idCorr = "{}c".format(nCorr)
        descCorr = "{}_{}".format(nameBaseCorr, i)

        corr = Corridor(idCorr, descCorr)
        dicCorridors[idCorr] = corr
        idsCorr.append(idCorr)

        nCorr += 1

        # Set neighbours
        setCorridorNeighbours(idCorr, dicCorridors)

    # Populate Corridors
    populateCorridor(dicCorridors, dicRooms, idsCorr, listRooms)
        
    return nCorr


# NEIGHBORHOOD BETWEEN CORRIDORS
def setCorridorNeighbours(idCorr, dicCorridors):
    splitId = idCorr.split('c')
    idNeighbour = int(splitId[0])
    idNeighbour = "{}c".format(idNeighbour-1)
    if idNeighbour in dicCorridors:
        nameNeigh = getNameCorridor(dicCorridors[idNeighbour].description)
        nameCorr = getNameCorridor(dicCorridors[idCorr].description)
        if nameNeigh != 'Surgical'  or  nameCorr == 'Surgical':     #not(nameNeigh == 'Surgical' and nameCorr != 'Surgical')
            dicCorridors[idCorr].nextTo[0] = dicCorridors[idNeighbour].id
            dicCorridors[idNeighbour].nextTo[1] = idCorr


# ALLOCATE ROOMS TO EACH CORRIDOR
def populateCorridor(dicCorridors, dicRooms, idsCorr, listRooms):
    nRoom = 0
    maxRooms = 20
    for j in range(len(idsCorr)):   #idCorr in idsCorr:
        idCorr = idsCorr[j]
        
        rooms = []
        if j == len(idsCorr)-1:
            maxRooms += 20/2

        i = 0
        while i<maxRooms and nRoom<len(listRooms):
            roomIdFull = listRooms[nRoom]
            splitId = roomIdFull.split('_')
            wardId = splitId[0]
            roomId = int(splitId[1])
            rooms.append(dicRooms[wardId][roomId])
            dicRooms[wardId][roomId].parent = idCorr
            
            i += 1
            nRoom += 1

        dicCorridors[idCorr].rooms = rooms



#####################
# SUPPORT FUNCTIONS #
#####################

def splitIdRoom(idRoom):
    idSplit = idRoom.split('_')
    idWard = idSplit[0]
    numRoom = idSplit[1]
    numRoom = int(numRoom)

    return idWard, numRoom

def getNameCorridor(description):
    nameCorrSplit = description.split('_')
    nameCorr = nameCorrSplit[0]

    return nameCorr



#################
# MAIN FUNCTION #
#################

def parsePhysicalHospital():
    # Rooms and Beds are created from the input file created ad-hoc
    dicRooms, dicBeds = createRoomsAndBeds()
    
    # Neighborhood between Beds is established
    for r1 in dicRooms.values():
        for r in r1.values():
            setNeighbourBeds(r.beds, dicBeds)
    
    # Rooms are grouped according to Service
    listSurg, listMed, listMix, listOther = parseRoomsType(dicRooms)
    listRooms = listSurg + listMix + listMed + listOther
    
    dicCorridors = {}
    nCorr = 0
    nCorr = createCorridors(dicCorridors, dicRooms, listSurg, "Surgical_Corridor", nCorr)
    nCorr = createCorridors(dicCorridors, dicRooms, listMix, "Mixed_Corridor", nCorr)
    nCorr = createCorridors(dicCorridors, dicRooms, listMed, "Medical_Corridor", nCorr)
    nCorr = createCorridors(dicCorridors, dicRooms, listOther, "Neonatal_Corridor", nCorr)


    indRoom = 0
    for idCorr in dicCorridors.keys():
        indRoom = setRoomsNeighbours(idCorr, indRoom, dicCorridors, dicRooms, listRooms)

    return dicCorridors, dicRooms, dicBeds, listSurg, listMed, listMix, listOther


    


if __name__ == "__main__":
    parsePhysicalHospital()