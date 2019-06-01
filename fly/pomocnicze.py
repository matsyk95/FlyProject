import requests
def new_date(date,days):
    date = str(date)
    month = date[5:7]  # good printuje np 03
    day = int(date[8:10]) + days
    next_day = days
    if (day < 10):
        nextdate = date[0:9] + str(day)
        return nextdate
    elif (int(date[5:7]) % 2 == 1 and int(date[5:7]) <= 12):
        # miesiace nieparzyste -> 31 dni
        if (day > 31):
            next_month = int(month) + 1  # good printuje np 4 (bez 0)
            # czy jelsi tu bedzie "day" to mi sie nadpisze ?
            day2 = int(date[8:10])
            diff = 31 - day2
            next_day = days - diff
            if (int(month) < 9):
                nextdate = date[0:6] + str(next_month) + "-0" + str(next_day)
                return nextdate
            else:
                nextdate = date[0:5] + str(next_month) + "-0" + str(next_day)
                return nextdate
        else:
            nextdate = date[0:8] + str(day)
            return nextdate
    elif (int(date[5:7]) % 2 == 0 and int(date[5:7]) <= 12):
        if (day > 31):
            next_month = int(month) + 1  # good printuje np 4 (bez 0)
            day2 = int(date[8:10])
            diff = 31 - day2
            next_day = days - diff
            if (int(month) < 9):
                nextdate = date[0:6] + str(next_month) + "-0" + str(next_day)
                return nextdate
            else:
                nextdate = date[0:5] + str(next_month) + "-0" + str(next_day)
                return nextdate
        else:
            nextdate = date[0:8] + str(day)
            return nextdate
    else:
        nextdate = date
        return nextdate

def create_airports(place2):
    s = requests.Session()
    s.headers.update({"X-RapidAPI-Key": "a1b3e35e10msh006c21e5b5f6617p1a0708jsn1dd2d3f443b5"})
    place1_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + place2
    a = s.get(place1_url).json()
    airports = []
    places_place1 = a["Places"]
    for x in places_place1:
        if 'PlaceId' in x:
            airports.append(x['PlaceId'])
    return airports

counter=0
days=1
start="2019-05-07"
fstart = "2019-05-07"
end="2019-05-12"
start_day = int(start[8:10])
end_day = int(end[8:10])
interval=end_day - start_day
start_places= ['WAW-sky', 'WMI-sky']
place2 ="Russia"
airports=create_airports(place2)
print("iloas lotnisk w place2 to : -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")
print(airports)
print(len(airports))


airportsWarsawFranceURL =[]
airportsWarsawFrance = []
s = requests.Session()
s.headers.update({"X-RapidAPI-Key": "7e1987716emshd8e087e4d068a79p1b259ejsna8f84b8ca1e1"})
for x in start_places:
    for y in airports:
         for z in range(0,6):
            url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/PL/PLN/en-US/" + x + "/" + y + "/" + start
            start = new_date(start, days)
            counter +=1
            a = s.get(url).json()
            try:
                quote = a["Quotes"]
                airportsWarsawFranceURL.append(url)
                all_place=a["Places"]
                len_places = len(all_place)
                qutboundLeg = quote[0]["OutboundLeg"]
                destinationId = qutboundLeg["DestinationId"]
            except IndexError:
                print("nie ma takiego lotu ")
            if start == end:
                start = fstart

for x in airportsWarsawFranceURL:
    a = s.get(x).json()
    try:
        quote = a["Quotes"]
        all_place = a["Places"]
        len_places = len(all_place)
        qutboundLeg = quote[0]["OutboundLeg"]
        destinationId = qutboundLeg["DestinationId"]
        for x in range(len_places):
            place = a['Places'][x]['PlaceId']
            if place == destinationId:
                originPlace = a["Places"][x]['SkyscannerCode']
                airportsWarsawFrance.append(originPlace+"-sky")
    except IndexError:
        print("nie ma takiego lotu ")


print("podsumowanie : ")
print("lista wszystkich lotnisk w place 2")
print(airports)
print(len(airports))
print("URL:")
print(airportsWarsawFranceURL)
print(set(airportsWarsawFranceURL))
print(counter)
print("Miejsca do ktorych lecim i te nie powtarzajace sie: ")
print(airportsWarsawFrance)
print(set(airportsWarsawFrance))


