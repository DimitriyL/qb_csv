import csv
print ("Input read-in file")
filename = input()
#reader = csv.DictReader (open ('cin_cle_16.csv', 'rU') )
reader = csv.DictReader (open (filename, 'rU') )
#fieldnames = ['Detail', 'CLE', 'CIN', 'Down', 'ToGo', 'Location', 'Time', 'Quarter', 'EPA', 'EPB']
fieldnames = reader.fieldnames
print ("Input QB name")
qbName = input()

def test (readable, qb):
    for line in readable:
        desc = line ['Detail']
        if qb in desc:
            print (line ['Detail'])


def initFilter (readable, qb):
    with open ('tidy.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        prevRow = '' #to deal with dastardly challenges

        for row in readable:
            if prevRow != '':
                preEmpt = row ['Detail']
                desc = prevRow ['Detail']
                if 'overturned' in preEmpt:
                    newDesc = preEmpt[(preEmpt.find('overturned') + 12):]
                    print (newDesc)
                    prevRow['Detail'] = newDesc
                    writer.writerow(prevRow)
                elif (qb in desc) and ("kneels" not in desc) and ('spike' not in desc) and ('overturned' not in desc):
                    if ("Penalty" in desc) and ("Declined" not in desc):
                        if ("Defensive Pass Interference" in desc) or ("Grounding" in desc) or ('no play' not in desc):
                            writer.writerow( prevRow )
                    else:
                        writer.writerow( prevRow )

            prevRow = row

#initFilter (reader, "Mayfield")
initFilter (reader, qbName)

readerTidy = csv.DictReader (open ('tidy.csv', 'rU') )
#test (readerTidy, "Mayfield")

def findDigs (str):
    newstring = ''
    foundDigs = False

    end = str.find("yard")
    for char in str:
        if char.isdigit():
            foundDigs = True
            newstring += char
        elif foundDigs:
            newStrInd = str.find(newstring)
            if (str[newStrInd - 1] == '-'):
                oldstring = newstring
                newstring = '-' + newstring
            return newstring

    return newstring

print (findDigs ("weast-124weast1"))

def newData (readable, qb):
    with open ('new.csv', 'w') as csvfile:
        #newNames = ['Detail', 'CLE', 'CIN', 'Down', 'ToGo', 'Location', 'Time', 'Quarter', 'EPA', 'EPB', 'Result', 'Gain', 'Depth', 'Area']
        names = readerTidy.fieldnames
        print (readerTidy.fieldnames)
        newNames = names + ['Type', 'Result', 'Gain', 'Depth', 'Area', 'Success']
        writer = csv.DictWriter(csvfile, fieldnames=newNames)
        writer.writeheader()

        for row in readable:
            desc = row ['Detail']

            awayTeamKey = names [6]
            homeTeamKey = names [7]

            awayTeam = row [awayTeamKey]
            homeTeam = row [homeTeamKey]
            q = row ['Quarter']
            down = row ['Down']
            togo = row ['ToGo']
            loc = row ['Location']
            time = row ['Time']
            epa = row ['EPA']
            epb = row ['EPB']

            type = ''
            res = ''
            gain = ''
            dep = ''
            area = ''
            succ = ''

            qbNameInd = desc.find(qbName) #for WR passes and stuff like that
            twoPointInd = desc.find('Two Point Attempt') #to handle the bug that now comes with 2pt conversions

            if 'touchdown' in desc:
                res = 'touchdown'
                if ' pass ' in desc:
                    type = 'pass'
                else:
                    type = 'run'
            elif 'intercepted' in desc:
                res = 'interception'
                type = 'pass'
            elif 'incomplete' in desc:
                res = 'incomplete'
                type = 'pass'
            elif 'complete' in desc:
                res = 'complete'
                type = 'pass'
            elif ' sack' in desc:
                res = 'sack'
                type = 'sack'
            else:
                res = 'run'
                type = 'run'

            if ' short' in desc:
                dep = 'short'
            elif ' deep' in desc:
                dep = 'deep'
            else:
                dep = 'n/a'

            if ' left' in desc:
                area = 'left'
            elif ' middle' in desc:
                area = 'middle'
            elif ' right' in desc:
                area = 'right'
            else:
                area = 'n/a'

            if ('intercepted' in desc) or ('incomplete' in desc) or ('no gain' in desc):
                gain = '0'
            else:
                gain = findDigs (desc)

            if 'Defensive Pass Interference' in desc:
                res = 'DPI'
                type = 'penalty'
            if 'Grounding' in desc:
                res = 'grounding'
                type = 'penalty'
                newGain = gain
                gain = '-' + newGain
            #if 'sack' in desc:
            #    newGain = gain
            #    gain = '-' + newGain

            if 'Two Point Attempt' in desc:
                togo = '2'
                if ' succeeds' in desc:
                    gain = '2'
                else:
                    gain = '0'

            ### Now, the important part of figuring out success or failure:
            numGain = float (gain)
            numTogo = float (togo)

            if down == '1':
                if numGain >= (numTogo / 3):
                    succ = 'success'
                else:
                    succ = 'failure'
            elif down == '2':
                if numGain >= (numTogo / 2):
                    succ = 'success'
                else:
                    succ = 'failure'
            else:
                if numGain >= numTogo:
                    succ = 'success'
                else:
                    succ = 'failure'

            if 'Two Point Attempt' in desc:
                if 'succeeds' in desc:
                    succ = 'success'
                else:
                    succ = 'failure'
            if 'Defensive Pass Interference' in desc:
                succ = 'success'

            ### In the special case of WR passes
            if (qbNameInd != 0) and (qbNameInd != 19):
                type = 'rec'
                if 'touchdown' in desc:
                    res = 'touchdown'
                    succ = 'success'
                elif 'complete' in desc:
                    res = 'rec'
                else:
                    res = 'rec'
                    succ = 'failure'

            writer.writerow({'Detail': desc, awayTeamKey: awayTeam, homeTeamKey: homeTeam, 'Down': down, 'ToGo': togo, 'Location': loc, 'Time': time, 'Quarter': q, 'EPA': epa, 'EPB': epb,
            'Type': type, 'Result': res, 'Gain': gain, 'Depth': dep, 'Area': area, 'Success': succ})

#newData (readerTidy, "Mayfield")
newData (readerTidy, qbName)

readerNew = csv.DictReader (open ('new.csv', 'rU') )

print ("Week?")
week = input()
print ("Opponent?")
opponent = input()
print ("Did this QB start the game?")
starter = input()
print ("Which file are we adding to?")
fileToAdd = input()
print ("Is this file to which we are adding presently empty (T/F)?")
isEmptyFile = input()

def analyze (readable, qb):
    with open (fileToAdd, 'a') as csvfile:
        regFields = ['Week', 'Opponent','Start', 'SuccPlays', 'PI', 'FailPlays', 'TotPlays', 'SuccRate', 'SuccYards',
        'FailYards', 'TotYards', 'SYardsPerP', 'FYardsPerP', 'YardsPerP']
        passFields = ['PassSuccPlays', 'PassFailPlays', 'PassTotPlays', 'PassSuccYards', 'PassFailYards', 'PassTotYards',
        'PassSuccRate', 'PSuccYPP', 'PFailYPP', 'PYPP']
        fieldnames = regFields + passFields
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if isEmptyFile:
            writer.writeheader()

        succPlays = 0.0
        piPlays = 0.0 #Need to distinguish PI from completions
        failPlays = 0.0

        succYards = 0.0
        failYards = 0.0

        ### Categories specific to passing

        passSuccPlays = 0.0
        passFailPlays = 0.0
        passTotPlays = 0.0

        passSuccYards = 0.0
        passFailYards = 0.0
        passTotYards = 0.0

        ### Categories such as area of field and depth of throw
        ### Left, Middle, Right

        leftSuccPlays = 0.0
        leftFailPlays = 0.0
        leftTotPlays = 0.0

        leftSuccYards = 0.0
        leftFailYards = 0.0
        leftTotYards = 0.0

        rightSuccPlays = 0.0
        rightFailPlays = 0.0
        rightTotPlays = 0.0

        rightSuccYards = 0.0
        rightFailYards = 0.0
        rightTotYards = 0.0

        midSuccPlays = 0.0
        midFailPlays = 0.0
        midTotPlays = 0.0

        midSuccYards = 0.0
        midFailYards = 0.0
        midTotYards = 0.0

        shortSuccPlays = 0.0
        shortFailPlays = 0.0
        shortTotPlays = 0.0

        shortSuccYards = 0.0
        shortFailYards = 0.0
        shortTotYards = 0.0

        deepSuccPlays = 0.0
        deepFailPlays = 0.0
        deepTotPlays = 0.0

        deepSuccYards = 0.0
        deepFailYards = 0.0
        deepTotYards = 0.0

        ###

        for row in readable:
            type = row['Type']
            result = row['Result']
            succ = row['Success']
            gain = float (row['Gain'])

            if result == 'DPI':
                piPlays += 1
            else:
                if succ == 'success':
                    succPlays += 1
                    succYards += gain
                    if type == 'pass':
                        passSuccPlays += 1
                        passSuccYards += gain
                elif succ == 'failure':
                    failPlays += 1
                    failYards += gain
                    if type == 'pass':
                        passFailPlays += 1
                        passFailYards += gain

        totPlays = succPlays + failPlays
        totYards = succYards + failYards

        succRate = (succPlays + piPlays) / (totPlays + piPlays)

        sYardsPerP = succYards / totPlays
        fYardsPerP = failYards / totPlays
        yardsPerP = totYards / totPlays

        ### Categories specific to passing

        passTotPlays = passSuccPlays + passFailPlays
        passTotYards = passSuccYards + passFailYards

        passSuccRate = passSuccPlays / passTotPlays

        psYPP = passSuccYards / passTotPlays
        pfYPP = passFailYards / passTotPlays
        pYPP = passTotYards / passTotPlays

        ###

        writer.writerow({'Week': week, 'Opponent': opponent, 'Start': starter, 'SuccPlays': succPlays, 'PI': piPlays,'FailPlays': failPlays, 'TotPlays': totPlays,
        'SuccRate': succRate, 'SuccYards': succYards, 'FailYards': failYards, 'TotYards': totYards,
        'SYardsPerP': sYardsPerP, 'FYardsPerP': fYardsPerP, 'YardsPerP': yardsPerP,
        'PassSuccPlays': passSuccPlays, 'PassFailPlays': passFailPlays, 'PassTotPlays': passTotPlays,
        'PassSuccYards': passSuccYards, 'PassFailYards': passFailYards, 'PassTotYards': passTotYards,
        'PassSuccRate': passSuccRate, 'PSuccYPP': psYPP, 'PFailYPP': pfYPP, 'PYPP': pYPP})


analyze (readerNew, qbName)
#readerAn = csv.DictReader (open ('addtoqb.csv', 'rU') )
