import datetime

'''
placesTracker: Function to track usage of Google Places API independently from the programming environment. It reads a 'PlacesTracker.txt' file which is a log file containing dates and the corresponding number of requests made to Google Places API. If the last date on the file it is the same as the system date, the number will be incremented. Otherwise, a new entry with a new date will be added. A

                 -------Sample of a PlacesTracker file--------------------------------
                        Date	Count

                        20180306	479
                        20180311	1662
                        20180312	27581
                        20180313	35001
                 ---------------------------------------------------------------------

-Inputs-
<null>

-Returns-
status <bool> : Indicator whether the number of requests to Google Places API has exceeded 150,000

'''
def placesTracker():
    file = 'PlacesTracker.txt'
    lastDate = 0
    lastCount = 0
    newDay = False
    with open(file, 'r') as f: 
        header = f.readline()
        lines = f.readlines()
        if len(lines) > 1:
            lastDate, lastCount = lines[-1][:-1].split('\t')

    now = datetime.datetime.now()
    if lastDate == now.strftime("%Y%m%d"):#Same day
        lastCount = int(lastCount) + 1
        lines = lines[:-1]
        lines.append(str(lastDate) + '\t' +str(lastCount) +'\n')
    else: 
        lastDate = now.strftime("%Y%m%d")
        lastCount = 1
        lines.append(str(lastDate) + '\t' +str(lastCount) +'\n')

    if lastCount < 150000: 
        status = True
        print('%i/%i' %(lastCount,150000))
    else:
        status = False
        print('Places query exceeded error: %i/%i' %(lastCount,150000))
    
    with open(file, 'w') as f: 
        f.write(header)
        for l in lines:
            f.write(l)
        
    return status
