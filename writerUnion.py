import os

from variablesWriter import nameFiles_Classes, nameFiles_Rels



##########################
# NAMES OF FILES TO JOIN #
##########################


def getInfiles_Classes(folderClasses):
    infiles = ["{}{}{}".format(folderClasses, nameFiles_Classes['patient'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['episode'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['death'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['hospitalization'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['testMicro'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['microorganism'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['uh'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['service'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['bed'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['room'], '.nt'),
             "{}{}{}".format(folderClasses, nameFiles_Classes['corridor'], '.nt')]

    return infiles

def getInfiles_Relations(folderRels):
    infiles = ["{}{}{}".format(folderRels, nameFiles_Rels['ep_pat'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['ev_ep'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['test_micro'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['ev_bed'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['ev_uh'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['serv_uh'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['bed_room'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['room_corridor'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['bed_nt'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['bed_ot'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['room_nt'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['room_ot'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['corridor_nt'], '.nt')]
    
    return infiles

def getInfiles_Relations_star(folderRels):
    infiles = ["{}{}{}".format(folderRels, nameFiles_Rels['ep_pat'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['ev_ep'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['test_micro'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['ev_bed'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['ev_uh'], '.nt'),
             "{}{}{}".format(folderRels, nameFiles_Rels['serv_uh'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['bed_room'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['room_corridor'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['bed_nt'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['bed_ot'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['room_nt'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['room_ot'], '.ttl'),
             "{}{}{}".format(folderRels, nameFiles_Rels['corridor_nt'], '.ttl')]
    
    return infiles



##############
# FILE UNION #
##############

def unionNTFiles_Classes(folderClasses, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000):
    
    infiles = getInfiles_Classes(folderClasses)

    outfileName = folderClasses + "\\Classes_complete_{}-{}__{}-{}_{}.nt".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    with open(outfileName, "w") as outfile:
        for infileName in infiles:
            copyFileWithChunks(infileName, outfile)

    outfile.close()
    print("\t- {} : Complete".format(outfileName))
    

def unionNTFiles_Relations(folderRels, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000, star):

    if star:
        infiles = getInfiles_Relations_star(folderRels)
        outfileName = folderRels + "\\Relations_complete_{}-{}__{}-{}_{}.ttl".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    else:
        infiles = getInfiles_Relations(folderRels)
        outfileName = folderRels + "\\Relations_complete_{}-{}__{}-{}_{}.nt".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    
    with open(outfileName, "w") as outfile:
        for infileName in infiles:
            copyFileWithChunks(infileName, outfile)

    outfile.close()
    print("\t- {} : Complete".format(outfileName))


def unionNTFiles_Full(folder, folderClasses, folderRels, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000, star):
    infiles_Classes = getInfiles_Classes(folderClasses)
    if star:
        infiles_Rels = getInfiles_Relations_star(folderRels)
        outfileName = folder + "\\data_complete_{}-{}__{}-{}_{}.ttl".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    else:
        infiles_Rels = getInfiles_Relations(folderRels)
        outfileName = folder + "\\data_complete_{}-{}__{}-{}_{}.nt".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    
    with open(outfileName, "w") as outfile:
        for infileName in infiles_Classes:
            copyFileWithChunks(infileName, outfile)

        for infileName in infiles_Rels:
            copyFileWithChunks(infileName, outfile)

    outfile.close()
    print("\t- {} : Complete".format(outfileName))



#############
# COPY FILE #
#############

def copyFileWithChunks(infileName, outfile):
    
    chunk_size = 1024 * 1024 * 10  # 10 MB
    with open(infileName, "r") as infile:
        infileSizeBytes = getFileSize(infileName)
        
        if infileSizeBytes < chunk_size:
            outfile.write(infile.read())
            outfile.write('\n')
            infile.close()
        else:
            nChunks = infileSizeBytes // chunk_size
            ultChunkSize = infileSizeBytes % chunk_size
            
            for i in range(nChunks+1):
                if i==nChunks:  #lastChunk
                    chunk_size = ultChunkSize
                
                chunk = infile.read(chunk_size)
                outfile.write(chunk)

            infile.close()


def getFileSize(fileName):
    file_stats = os.stat(fileName)
    sizeBytes = file_stats.st_size

    return sizeBytes


########
# MAIN #
########

def unionFiles(folder, folderClasses, folderRels, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000, star):
    unionNTFiles_Classes(folderClasses, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    unionNTFiles_Relations(folderRels, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000, star)

    unionNTFiles_Full(folder, folderClasses, folderRels, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000, star)
