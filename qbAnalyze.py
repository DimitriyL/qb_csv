import csv

print ('Input read-in filename')
readIn = input()
reader = csv.DictReader (open (readIn, 'rU') )

print ('Input qb name')
qbName = input()
print ('Input qb team')
team = input()

def test (readable, qb):
    for line in readable:
        desc = line ['Detail']
        if qb in desc:
            print (line ['Detail'])

print ('Input write-to filename')
inFile = input()
print ('Is file empty?')
isFileEmpty = input()

def analyze (readable, qb):
    with open (inFile, 'a') as csvfile:
        regFields = ['Name', 'Team', 'Games', 'Starts', 'SuccPlays', 'PI', 'FailPlays', 'TotPlays', 'SuccRate', 'SuccYards',
        'FailYards', 'TotYards', 'SYardsPerP', 'FYardsPerP', 'YardsPerP']
        passFields = ['PassSuccPlays', 'PassFailPlays', 'PassTotPlays', 'PassSuccYards', 'PassFailYards', 'PassTotYards',
        'PassSuccRate', 'PSuccYPP', 'PFailYPP', 'PYPP']
        fieldnames = regFields + passFields
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if isFileEmpty:
            writer.writeheader()

        games = 0.0
        starts = 0.0

        succPlays = 0.0
        piPlays = 0.0
        failPlays = 0.0
        totPlays = 0.0

        succYards = 0.0
        failYards = 0.0
        totYards = 0.0

        passSuccPlays = 0.0
        passFailPlays = 0.0
        passTotPlays = 0.0

        passSuccYards = 0.0
        passFailYards = 0.0
        passTotYards = 0.0

        for row in readable:
            games += 1
            if (row['Start'] == 'Yes'):
                starts += 1

            succPlays += float (row['SuccPlays'])
            piPlays += float (row['PI'])
            failPlays += float (row['FailPlays'])

            succYards += float (row['SuccYards'])
            failYards += float (row['FailYards'])

            passSuccPlays += float (row['PassSuccPlays'])
            passFailPlays += float (row['PassFailPlays'])

            passSuccYards += float (row ['PassSuccYards'])
            passFailYards += float (row ['PassFailYards'])

        totPlays = succPlays + failPlays
        totYards = succYards + failYards

        passTotPlays = passSuccPlays + passFailPlays
        passTotYards = passSuccYards + passFailYards

        succRate = (succPlays + piPlays) / (totPlays + piPlays)

        sYardsPerP = succYards / totPlays
        fYardsPerP = failYards / totPlays
        yardsPerP = totYards / totPlays


        passSuccRate = passSuccPlays / passTotPlays

        psYPP = passSuccYards / passTotPlays
        pfYPP = passFailYards / passTotPlays
        pYPP = passTotYards / passTotPlays

        writer.writerow({'Name': qb, 'Team': team, 'Games': games, 'Starts': starts,
        'SuccPlays': succPlays, 'PI': piPlays,'FailPlays': failPlays, 'TotPlays': (totPlays + piPlays),
        'SuccRate': succRate, 'SuccYards': succYards, 'FailYards': failYards, 'TotYards': totYards,
        'SYardsPerP': sYardsPerP, 'FYardsPerP': fYardsPerP, 'YardsPerP': yardsPerP,
        'PassSuccPlays': passSuccPlays, 'PassFailPlays': passFailPlays, 'PassTotPlays': passTotPlays,
        'PassSuccYards': passSuccYards, 'PassFailYards': passFailYards, 'PassTotYards': passTotYards,
        'PassSuccRate': passSuccRate, 'PSuccYPP': psYPP, 'PFailYPP': pfYPP, 'PYPP': pYPP})

analyze (reader, qbName)
