from dateNormalizer import normalizeDates

from classes import *

from parserPatients import parsePatients
from parserLogicalHospital import parseLogicalHospital
from parserEpisodesEvents import parseEpisodesAndEvents
from parserPhysicalHospital import parsePhysicalHospital
from eventDistributor import distributeEvents

from writerCSV import setFolderOutputCSV, printCSV
from writerNT import setFolderOutputNT, printNT
from writerNT_star import setFolderOutputNT_star, printNT_star
from writerResumes import setFolderSummary, writeResumes
from writerUnion import unionFiles


def generateSolution(minYearN, maxYearN, minYear, maxYear, maxEvents):
    # If maxEvents=0 -> All Events that exist are added to the solution 

    # Normalize the years of the files
    print("NORMALIZING DATES TO: {} - {}".format(minYearN, maxYearN))
    normalizeDates(minYearN, maxYearN)

    # Variables to filter only the Events/Episodes of a time period
    print("FILTERING EPISODES/EVENTS OF THE YEARS: {} - {}".format(minYear, maxYear))
    

    # Parsing and creating elements
    print("PARSING INPUT")
    dicPatients = parsePatients()
    dicServices, dicHUs = parseLogicalHospital()
    dicEpisodes, dicMicroorganisms = parseEpisodesAndEvents(dicPatients, dicServices, minYearN, maxYearN, minYear, maxYear, maxEvents)
    dicCorridors, dicRooms, dicBeds, listSurg, listMed, listMix, listOther = parsePhysicalHospital()
    distributeEvents(dicEpisodes, dicRooms)


    # Writing
    print("WRITING OUTPUT")

    print(" ... CSV")
    dirCSV = ".\\OutputCSV"
    setFolderOutputCSV(dirCSV, minYearN, maxYearN, minYear, maxYear, maxEvents)
    printCSV(dicServices, dicHUs, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms)

    print(" ... NT")
    dirNT = ".\\OutputRDF"
    dirClasses_NT, dirRels_NT, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000 = setFolderOutputNT(dirNT, minYearN, maxYearN, minYear, maxYear, maxEvents)
    printNT(dicServices, dicHUs, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms)

    print(" ... RDF_star")
    dirNT_star = ".\\OutputNT_star"
    dirClasses_NTstar, dirRels_NTstar, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000 = setFolderOutputNT_star(dirNT_star, minYearN, maxYearN, minYear, maxYear, maxEvents)
    printNT_star(dicServices, dicHUs, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms)

    print(" ... File Union")
    unionFiles(dirNT, dirClasses_NT, dirRels_NT, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000, False)
    unionFiles(dirNT_star, dirClasses_NTstar, dirRels_NTstar, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000, True)

    print(" ... Location Summary")
    setFolderSummary(".\\OutputSummary")
    listsRooms = []
    listsRooms.append(listSurg)
    listsRooms.append(listMix)
    listsRooms.append(listMed)
    listsRooms.append(listOther)
    writeResumes(dicPatients, dicCorridors, dicRooms, listsRooms, minYearN, maxYearN, minYear, maxYear, maxEvents)




def main():
    
    tests = []
    
    tests.append([2000,2025,2005,2005,25000])   # 0
    tests.append([2000,2007,2004,2004,75000])   # 1
    tests.append([2000,2004,2002,2002,125000])  # 2
    tests.append([2000,2003,2001,2001,175000])  # 3
    tests.append([2000,2002,2000,2000,225000])  # 4
    tests.append([2000,2000,2000,2000,275000])  # 5
    tests.append([2000,2000,2000,2000,325000])  # 6
    tests.append([2000,2000,2000,2000,375000])  # 7
    tests.append([2000,2000,2000,2000,425000])  # 8
    tests.append([2000,2000,2000,2000,0])   # 9

    for i in range(len(tests)):
         print("\n\n##########################")
         print("# TEST {} - {} Events #".format(i, tests[i][4]))
         print("##########################\n")
         generateSolution(tests[i][0],tests[i][1],tests[i][2],tests[i][3], tests[i][4])


if __name__ == "__main__":
    main()

