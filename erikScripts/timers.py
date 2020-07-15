#This function takes some variables which represent times to do certain actions in order ot calculate

#in terms of minutes, this is how long you spend between missions on avg
setUpTime = 1.5

#In terms of minutes, this is how long it takes to run any given mission to the first drop on average
avgMissionTime = 4.5

#this is the number of void traces that drop from cracking open a relic on average
voidTracesPDrop = 18.75



def main(missionType, relicRarity, dropChance, rotation = 'a'):
    rotation = rotation.lower()
    missionType = missionType.lower()
    relicRarity = relicRarity.lower()


    if rotation == 'a':
        rotation = 0
    elif rotation == 'b':
        rotation = 1
    elif rotation == 'c':
        rotation = 2
    else:
        print("invalid rotation value.")
        return

    elite = 0
    if missionType == 'elite sanctuary onslaught':
        missionType = 'sanctuary onslaught'
        elite = 1

    #missionTypes = ['survival', 'capture', 'exterminate', 'defence', 'interception', 'excavation', 'spy', 'mobile defence', 'skirmish', 'disruption', 'pursuit', 'sanctuary onslaught', 'defection', 'infested salvage', 'sabotage', 'rush' ]

    #this is a dict where each key is a mission type, and each value is the list of avg times to get a drop of that rarity (going [A,B,C] or just [A] if it's not an endless missions)
    missionDict = dict()

    missionDict['survival'] = [(setUpTime + 10) / 2, setUpTime + 15, setUpTime + 20]
    #assuming 3 minutes to do a full capture mission
    missionDict['capture'] = [setUpTime + 3]
    #assuming 6 minutes to complete an exterminate node
    missionDict['exterminate'] = [setUpTime + 6]
    #this assumes an avg time of going through 5 waves as 5 minutes
    fiveWaveTime = 5
    missionDict['defence'] = [(setUpTime + (fiveWaveTime * 2)) / 2 , setUpTime + (fiveWaveTime * 3) , setUpTime + (fiveWaveTime * 4)]
    #since a perfect time to hit 100% is 3 minutes, and since you probably won't get totally perfect and that you have to kill everyone on the mission, 4 minutes sounds avg
    waveTime = 4
    missionDict['interception'] = [(setUpTime + (waveTime * 2)) / 2 , setUpTime + (waveTime * 3) , setUpTime + (waveTime * 4)]
    #assumes an avg time to crack an excavator at 1.25 minutes, which assumes some overlap in excavator run times
    excavatorTime = 1.25
    missionDict['excavation'] = [(setUpTime + (excavatorTime * 4)) / 2 , setUpTime + (excavatorTime * 6) , setUpTime + (excavatorTime * 8)]
    runThroughTime = 3
    vaultTime = 3
    #check out missions.txt for the logic behind this mission times
    missionDict['spy'] = [setUpTime + runThroughTime + vaultTime, setUpTime + runThroughTime + vaultTime, setUpTime + runThroughTime + (2*vaultTime)]

    terminalTime = 2.5
    missionDict['mobile defence'] = [setUpTime + (2.5 * terminalTime)]

    missionDict['skirmish'] = [setUpTime + 10]

    #check out missions.txt for logic on this
    maxWaves = 8
    disrWaveTime = 3
    missionDict['disruption'] = [(setUpTime + (disrWaveTime * 3)) / 3 , (setUpTime + (disrWaveTime * maxWaves)) / maxWaves, (setUpTime + (disrWaveTime * maxWaves)) / (maxWaves - 2)]

    missionDict['pursuit'] = [setUpTime + 7]

    missionDict['sanctuary onslaught'] = [(setUpTime + 10) / 2 , setUpTime + 15 , setUpTime + 20]

    missionDict['defection'] = [0]

    missionDict['infested salvage'] = [0]

    missionDict['sabotage'] = [0]

    missionDict['rush'] = [0]

    #uses the mission type, rotation, and drop chance to get the avg amount of time to recieve the relic you're looking for
    avgTime = missionDict[missionType][rotation]
    avgTime = avgTime * ((dropChance / 100) ** -1.0)


    # after this line avgTime is the time to farm and crack your specific relic
    avgTime += setUpTime + avgMissionTime


    #this dict will contain chances to get a specific item of the chosen rarity.
    # each list contains the chance to get an itme of the chosen rarity at intact quality at [0], exceptional at [1], flawless at [2], and radiant at [3]
    rarityDict = dict()
    rarityDict['common'] = [25.33, 23.33, 20, 16.67]
    rarityDict['uncommon'] = [11, 13, 17, 20]
    rarityDict['rare'] = [2, 4, 6, 10]


    #in this case we have four cases to check, not upgrading the relic at all, upgrading it to exceptional, upgrading to flawless, and upgrading to radiant
    #once we have seen the avg times to get the item we are looking for using each of these methods, we pick the shortest time and the upgrad lvl
    if elite == 0:
        #this is the amount of time it takes to farm one void trace in minutes, helps with other calcs
        oneTrace = (avgMissionTime + setUpTime) / voidTracesPDrop

        #since you get some traces when cracking a relic, you have less to farm to upgrade your relic
        # this list is the amount of time you need to farm the traces to upgrade to each tier of quality
        timeNeeded = [0, (25 - voidTracesPDrop) * oneTrace, (50 - voidTracesPDrop) * oneTrace, (100 - voidTracesPDrop) * oneTrace]
        chances = rarityDict[relicRarity]
        qualities = ['Intact', 'Exceptional', 'Flawless', 'Radiant']
        bestTime = 0
        for x in range(4):
            time = (avgTime + timeNeeded[x]) * ((chances[x] / 100) ** -1.0)
            if time < bestTime or bestTime == 0:
                bestTime = time
                upgradeLvl = qualities[x]
        if bestTime != 0:
            avgTime = bestTime
        else:
            return "best time equalled 0/ Something went wrong"


    #else happens when running elite sanctuary onslaught
    else:
        upgradeLvl = 'Radiant'
        if relicRarity == 'common':
            chance = 16.67
        elif relicRarity == 'uncommon':
            chance = 20
        elif relicRarity == 'rare':
            chance = 10
        #now avgTime is the time to get the item you are looking for and we are ready to return
        avgTime = avgTime * ((chance/ 100) ** -1.0)


    return upgradeLvl, str(round(avgTime, 2)) + ' minutes'



print(main('capture', 'uncommon', 11.06, 'a'))