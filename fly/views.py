from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.views.generic import ListView
from pandas.io.formats import console
from pip._vendor.distlib.compat import raw_input
from django.contrib.auth import authenticate, login
from .forms import FlyForm, UserForm
from django.views.generic.edit import CreateView
from .models import Fly, Country
import requests
from django.views import generic
import random
from django.contrib.auth import logout

# def index(request):
#     return render(request, 'fly/fly.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        # returns User object if credenticals are correct
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'fly/fly.html')
    context = {
        "form": form,
    }
    return render(request, 'fly/registration_form.html', context)

def login_user(request):
    if request.POST == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'fly/fly.html')
            else:
                return render(request, 'fly/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'fly/login.html', {'error_message': 'Invalid login'})
    return render(request, 'fly/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'fly/login.html', context)

def detail(request):
    fly_list = Fly.objects.all()
    return render(request,'fly/detail.html', {'fly_list': fly_list})



def index(request):
    form = FlyForm(request.POST or None)
    if form.is_valid():
        fly = form.save(commit=False)
        fly.save()
    contex = {
        'form': form,
    }

    if request.POST:
        fly_id = str(Fly.objects.latest('id').id)
        return redirect(f'/fly/{fly_id}')
    else:
        return render(request, 'fly/fly.html', contex)

def removeWrongElement(airports):
    list = ['IT-sky', 'FR-sky', 'MILA-sky']

    for x in range(0, len(list)):
        try:
            print(airports.index(list[x]))
            airports.remove(list[x])
        except ValueError:
            print("Fajnie nie ma tego w mojej liscie ")
    print(airports)
    return airports

def results(request, fly_id):
    fly = get_object_or_404(Fly, pk=fly_id)
    return render(request, 'fly/results.html', {'fly': fly})

# def all(request):
#     all_fly=Fly.objects.all()
#     return render(request, 'fly/all.html', {'all_fly': all_fly})

#
# class IndexView(generic.ListView):
#     template_name='fly/create_airport.html'
#     context_object_name = 'all_country'
#     def get_queryset(self):
#         return Country.objects.all()

def new_date2(date,days):
    print("wejscie do f-cji zmiany daty new_date2")
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
            next_date = date[0:8] + str(day)
            return next_date
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

def new_date(date,days):
    print("wejscie do f-cji zmiany daty new_date")
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

def choose_airlines(airline):
    print("wejscie do f-cji choose_airlines")
    list_airlines = ['Ryanair',"Wizz Air", "LOT", "airBaltic", "Air France", "Vueling Airlines", "Eurostar", "easyJet", "eurowings", "Iberia", "Volotea", "British Airways","Alitalia"]
    if(airline in list_airlines):
        indeks = list_airlines.index(airline)
        if indeks ==0:
            carrier = "https://www.ryanair.com/pl/pl/"
            return carrier
        elif indeks==1:
            carrier = "https://wizzair.com/pl-pl"
            return carrier
        elif indeks==2:
            carrier = "https://www.lot.com/pl/pl/"
            return carrier
        elif indeks==3:
            carrier = "https://www.airbaltic.com/lv-LV/index"
            return carrier
        elif indeks==4:
            carrier = "https://www.airfrance.com/indexCom_en.html"
            return carrier
        elif indeks==5:
            carrier = "https://www.vueling.com/es"
            return carrier
        elif indeks==6:
            carrier = "https://www.eurostar.com/rw-en"
            return carrier
        elif indeks==7:
            carrier = "https://www.easyjet.com/pl"
            return carrier
        elif indeks==8:
            carrier = "https://www.eurowings.com/en.html"
            return carrier
        elif indeks==9:
            carrier = "https://www.iberia.com/us/"
            return carrier
        elif indeks==10:
            carrier = "https://www.volotea.com/en/"
            return carrier
        elif indeks==11:
            carrier = "https://www.britishairways.com/travel/home/public/pl_pl"
            return carrier
        elif indeks==12:
            carrier = "https://www.alitalia.com/pl_pl/"
            return carrier

    else:
        carrier = "https://www.skyscanner.pl/"
        return carrier

def informationOrgin(url):
    print("wejscie do f-cji  informationOrgin")
    s = requests.Session()
    s.headers.update({"X-RapidAPI-Key": "7e1987716emshd8e087e4d068a79p1b259ejsna8f84b8ca1e1"})
    a = s.get(url).json()
    all_place = a['Places']
    len_places = len(all_place)
    quote = a["Quotes"]
    qutboundLeg = quote[0]["OutboundLeg"]
    destinationId = qutboundLeg["DestinationId"]
    destinationPlace = []
    departureDate = qutboundLeg["DepartureDate"]
    originId = qutboundLeg["OriginId"]
    for x in range(len_places):
        place = a['Places'][x]['PlaceId']
        if place == originId:
            originPlace = a["Places"][x]['SkyscannerCode']
            nameOrginplace = a["Places"][x]['Name']
            countryOrginplace = a["Places"][x]["CountryName"]
            return originPlace, nameOrginplace, countryOrginplace
        else:
            print("")
    return [None] * 3

def informationDestination(url):
    print("wejsce do f-cji informationDestinatnon, url badany w tej funkcji to ")
    print(url)

    s = requests.Session()
    s.headers.update({"X-RapidAPI-Key": "ce73a19681msha746ea42b125d79p1cd6e0jsnd9992a78258a"})
    a = s.get(url).json()
    all_place = a['Places']
    len_places = len(all_place)
    all_carriers = a['Carriers']
    len_carriers = len(all_carriers)
    quote = a["Quotes"]
    qutboundLeg = quote[0]["OutboundLeg"]
    destinationId = qutboundLeg["DestinationId"]
    destinationPlace = []
    departureDate = qutboundLeg["DepartureDate"]
    numberCarrierIds_list = qutboundLeg["CarrierIds"]
    numberCarrierIds = int("".join(map(str,numberCarrierIds_list))) #zmieniam liste na inta
    min_price = quote[0]['MinPrice']
    for x in range(len_places):
        place = a['Places'][x]['PlaceId']
        if place == destinationId:
            destinationPlace = a["Places"][x]['SkyscannerCode']
            nameDestinationplace = a["Places"][x]["Name"]
            countryDestination = a["Places"][x]["CountryName"]

            for x in range(len_carriers):
                carriers = a['Carriers'][x]['CarrierId']
                if numberCarrierIds == carriers:
                    airline = a['Carriers'][x]['Name']
                    carrier = choose_airlines(airline)
                    print("fcja informationDestination zakonczona sukcesem ! !  ! ! ! ")
                    return departureDate, nameDestinationplace, countryDestination, destinationPlace, carrier, airline, min_price
                else:
                    print("nie ma informacji o danym locie , id korego szukam to ")
                    # print(numberCarrierIds)
                    # print("a dostaje")
                    # print(carriers)
                    # carrier = "https://www.skyscanner.pl/"
                    # print("coś sie nue udało , numery się nie zgadzają w api ...... :( :( :( ")
                    # print(carrier)
                    # airline = a['Carriers'][1]['Name']
                    # return departureDate, nameDestinationplace, countryDestination, destinationPlace, carrier, airline
        else:
            print("place nie pasuej do destinationId ")
    return [None] * 4

def create_airports(place2,place3,place4):
    s = requests.Session()
    s.headers.update({"X-RapidAPI-Key": "a1b3e35e10msh006c21e5b5f6617p1a0708jsn1dd2d3f443b5"})
    print(place2)
    print(type(place4))
    print(place3)
    print(place4)

    if(place2 == None):

        airports = ['WAW-sky', 'WMI-sky', 'LHR-sky', 'LGW-sky', 'LTN-sky', 'STN-sky', 'LCY-sky',
                         'SEN-sky', 'YXU-sky', 'ELS-sky', 'LDY-sky', 'DUB-sky', 'LUZ-sky', 'PARI-sky', 'ORY-sky',
                         'OTP-sky', 'MOL-sky', 'CLJ-sky', 'RMI-sky']
        return airports
    elif(place2 != "" and place3 == ""):

        place1_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + place2
        a = s.get(place1_url).json()
        list_place1 = []
        places_place1 = a["Places"]
        for x in places_place1:
            if 'PlaceId' in x:
                list_place1.append(x['PlaceId'])
        airports = list_place1
        return airports
    elif(place3 != "" and place4 == ""):

        place1_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + place2
        place2_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + place3
        a = s.get(place1_url).json()
        aa = s.get(place2_url).json()
        list_place1 = []
        list_place2 = []
        places_place1 = a["Places"]
        places_place2 = aa["Places"]
        for x in places_place1:
            if 'PlaceId' in x:
                list_place1.append(x['PlaceId'])
        for x in places_place2:
            if 'PlaceId' in x:
                list_place2.append(x['PlaceId'])
        airports = list_place1 + list_place2
        return airports
    elif(place2 != "" and place4 != ""):

        place1_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + place2
        place2_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + place3
        place3_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + place4
        a = s.get(place1_url).json()
        aa = s.get(place2_url).json()
        aaa = s.get(place3_url).json()
        list_place1 = []
        list_place2 = []
        list_place3 = []
        places_place1 = a["Places"]
        places_place2 = aa["Places"]
        places_place3 = aaa["Places"]
        for x in places_place1:
            if 'PlaceId' in x:
                list_place1.append(x['PlaceId'])
        for x in places_place2:
            if 'PlaceId' in x:
                list_place2.append(x['PlaceId'])
        for x in places_place3:
            if 'PlaceId' in x:
                list_place3.append(x['PlaceId'])
        airports = list_place3+list_place2+list_place1
        return airports
    else:
        return [None]

def search_origin_and_destination(originplace,destinationplace):
    popular_places = ["France", "Poland", "England", "Italy", "Greece", "Spain","Portugal","Belgium", "Austria", "Ukraine" , "Russia", "Sweden", "Norway"]
    warsawFrance = ['LGW-sky', 'LHR-sky', 'STN-sky', 'LTN-sky']
    warsawEngland = ['LGW-sky', 'MAN-sky', 'SEN-sky', 'STN-sky', 'LCY-sky', 'LPL-sky', 'BHX-sky', 'LHR-sky', 'LTN-sky']
    warsawPoland = ['LUZ-sky', 'GDN-sky', 'KRK-sky', 'SZZ-sky', 'WRO-sky', 'POZ-sky', 'RZE-sky', 'KTW-sky']
    warsawItaly = ['FCO-sky', 'BLQ-sky', 'BDS-sky', 'LIN-sky', 'MXP-sky', 'CIA-sky', 'BGY-sky', 'NAP-sky', 'AOI-sky']
    warsawGreece = ['JMK-sky', 'ATH-sky', 'HER-sky', 'SKG-sky', 'RHO-sky', 'CFU-sky', 'AOK-sky', 'JTR-sky', 'ZTH-sky']
    warsawSpain = ['PMI-sky', 'MAD-sky', 'VLC-sky', 'BCN-sky', 'AGP-sky', 'BIO-sky', 'TFN-sky', 'TFS-sky', 'SVQ-sky', 'ALC-sky', 'ACE-sky']
    warsawPortugal = ['LIS-sky', 'FAO-sky', 'TER-sky', 'PDL-sky', 'OPO-sky', 'FNC-sky']
    warsawBelgium = ['BRU-sky', 'OST-sky', 'CRL-sky', 'ANR-sky']
    warsawAustria = ['LNZ-sky', 'SZG-sky', 'KLU-sky', 'VIE-sky', 'MEL-sky', 'SYD-sky', 'AVV-sky', 'GRZ-sky', 'BNE-sky', 'PER-sky', 'INN-sky', 'OOL-sky']
    warsawUkraine = ['CWC-sky', 'DNK-sky', 'HRK-sky', 'ODS-sky', 'KBP-sky', 'LWO-sky', 'KHE-sky', 'IEV-sky', 'OZH-sky']
    warsawRussia = ['RU-sky', 'LED-sky', 'KGD-sky', 'MOSC-sky', 'SVO-sky', 'DME-sky', 'VKO-sky', 'ZIA-sky', 'IKT-sky', 'ROV-sky']
    warsawSweden = ['MMX-sky', 'BMA-sky', 'NYO-sky', 'GOT-sky', 'ARN-sky', 'VST-sky']
    warsawNorway = ['TRF-sky', 'BGO-sky', 'SVG-sky', 'AES-sky', 'OSL-sky', 'KSU-sky', 'TRD-sky', 'TOS-sky']
    if(originplace == "Warsaw" and destinationplace in popular_places ):
        list_airport_orgiplace = ["WAW-sky","WMI-sky"]
        indeks = popular_places.index(destinationplace)
        if indeks == 0:
            list_airport_destinatonplace = warsawFrance
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 1:
            list_airport_destinatonplace = warsawPoland
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 2:
            list_airport_destinatonplace = warsawEngland
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 3:
            list_airport_destinatonplace = warsawItaly
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 4:
            list_airport_destinatonplace = warsawGreece
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 5:
            list_airport_destinatonplace = warsawSpain
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 6:
            list_airport_destinatonplace = warsawPortugal
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 7:
            list_airport_destinatonplace = warsawBelgium
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 8:
            list_airport_destinatonplace = warsawAustria
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 9:
            list_airport_destinatonplace = warsawUkraine
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 10:
            list_airport_destinatonplace = warsawRussia
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 11:
            list_airport_destinatonplace = warsawSweden
            return list_airport_orgiplace, list_airport_destinatonplace
        elif index == 12:
            list_airport_destinatonplace = warsawNorway
            return list_airport_orgiplace, list_airport_destinatonplace
    else:
        originplace_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + originplace
        destinationplace_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/PL/GBP/en-GB/?query=" + destinationplace
        list_airport_orgiplace = []
        list_airport_destinatonplace = []
        s = requests.Session()
        s.headers.update({"X-RapidAPI-Key": "a1b3e35e10msh006c21e5b5f6617p1a0708jsn1dd2d3f443b5"})
        a = s.get(originplace_url).json()
        aa = s.get(destinationplace_url).json()
        places_originplace = a["Places"]
        places_destinationplace = aa["Places"]

        for x in places_originplace:
            if 'PlaceId' in x:
                list_airport_orgiplace.append(x['PlaceId'])

        for x in places_destinationplace:
            if 'PlaceId' in x:
                list_airport_destinatonplace.append(x['PlaceId'])
        return list_airport_orgiplace, list_airport_destinatonplace

def search_fly_originAndDestination(list_airport_orgiplace,list_airport_destinatonplace,currency,date):
    print("wejscie do fcji search fly origin and destinationplace ")
    price={}
    s = requests.Session()
    s.headers.update({"X-RapidAPI-Key": "a1b3e35e10msh006c21e5b5f6617p1a0708jsn1dd2d3f443b5"})
    for x in list_airport_orgiplace:
        for y in list_airport_destinatonplace:
            url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/" + currency + "/en-US/" + x + "/" + y + "/" + str(date)
            a = s.get(url).json()
            print(url)
            try:
                quote = a["Quotes"]
                pricequote = quote[0]['MinPrice']
                price.update({pricequote: url})
            except IndexError:
                print("nie ma takiego lotu ")

    first_cheapper_price = (sorted(price.items())[0][0])
    first_cheapper_url = (sorted(price.items())[0][1])
    print("koniec f-cj wyszukiwania polaczenia, najtanszy lot to : ")
    print(first_cheapper_url)
    print(first_cheapper_price)
    return first_cheapper_url, first_cheapper_price

def searchXandDestination(destinationPlace, list_airport, currency,date):
    print("wejscie do petli search fly X and destination")
    price = {}
    s = requests.Session()
    s.headers.update({"X-RapidAPI-Key": "a1b3e35e10msh006c21e5b5f6617p1a0708jsn1dd2d3f443b5"})
    for x in list_airport:
        url= "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/"+currency+"/en-US/" + destinationPlace + "-sky/" + x + "/" + str(date)
        a=s.get(url).json()
        print(url)
        try:
            quote = a["Quotes"]
            pricequote = quote[0]['MinPrice']
            price.update({pricequote: url})
        except IndexError:
            print("nie ma takiego lotu ")

    first_cheapper_price = (sorted(price.items())[0][0])
    first_cheapper_url = (sorted(price.items())[0][1])
    print("koniec petli fly x i destinatiponplace ,cena i url najtanszego lotu to "":: ")
    print(first_cheapper_price)
    print(first_cheapper_url)
    return first_cheapper_url, first_cheapper_price

def search(request, fly_id):
    fly = get_object_or_404(Fly, pk=fly_id)
    s = requests.Session()
    s.headers.update({"X-RapidAPI-Key": "a1b3e35e10msh006c21e5b5f6617p1a0708jsn1dd2d3f443b5"})

    date = fly.date
    days = fly.day
    originplace = fly.orginplace
    destinationplace = fly.descinationplace
    currency = fly.currency
    endDate=fly.endDate
    price = {}

    list_airport_orgiplace=search_origin_and_destination(originplace, destinationplace)[0]
    list_airport_destinatonplace = search_origin_and_destination(originplace, destinationplace)[1]
    print(list_airport_orgiplace)
    print(list_airport_destinatonplace)
    print("wypisałem miasta teraz wchodzę do wlasciwej petli ")

            #szukamy bezposreniego najtanszego lotu ! dane to: originplace, destinationplace, currency, date
    if (fly.number_city==0 and fly.price ==0 and fly.endDate ==None):
        first_fly = search_fly_originAndDestination(list_airport_orgiplace,list_airport_destinatonplace,currency,date)
        first_cheapper_url = first_fly[0]
        first_cheapper_price = first_fly[1]

        infoDestination = informationDestination(first_cheapper_url)
        departureDate = infoDestination[0]
        nameDestinationplace = infoDestination[1]
        countryDestination = infoDestination[2]
        carrier =infoDestination[4]
        airline_namie = infoDestination[5]
        infoOrigin = informationOrgin(first_cheapper_url)
        originPlace= infoOrigin[0]
        nameOrginplace = infoOrigin[1]
        countryOrginplace = infoOrigin[2]
        return render(request, 'fly/results1.html', {
            'first_cheapper_price': first_cheapper_price,
            'first_cheapper_url': first_cheapper_url,
            'departureDate': departureDate,
            'nameDestinationplace': nameDestinationplace,
            'countryDestination': countryDestination,
            'originPlace': originPlace,
            'nameOrginplace': nameOrginplace,
            'countryOrginplace': countryOrginplace,
            'carrier':carrier,
            'airline_name':airline_namie,
            'currency': currency,
        })
#wyszukiwanie najtańszego lotu do jednego miasta, dane to: originplace, destinationplace, number city, currency, date
    elif(fly.number_city == 1 and fly.day != 0 and fly.endDate ==None):
        print("wyszukiwanie najtańszego lotu do jednego miasta, dane to: originplace, destinationplace, number city, currency, date")
        all_airports = create_airports(fly.airports.name2, fly.airports.name3, fly.airports.name4)
        airports = removeWrongElement(all_airports)
        print(airports)
        nextdate = new_date(date, days)
        first_fly= search_fly_originAndDestination(list_airport_orgiplace,airports,currency,date)
        first_cheapper_price = first_fly[1]
        first_cheapper_url = first_fly[0]
        destinationPlace = informationDestination(first_cheapper_url)[3]
        print(destinationPlace)
        print(type(destinationPlace))
        second_fly= searchXandDestination(destinationPlace,list_airport_destinatonplace,currency,nextdate)
        second_cheapper_url = second_fly[0]
        second_cheapper_price = second_fly[1]
        final_price = second_cheapper_price + first_cheapper_price

        infoDestination = informationDestination(first_cheapper_url)
        departureDate = infoDestination[0]
        nameDestinationplace = infoDestination[1]
        countryDestination = infoDestination[2]
        carrier =infoDestination[4]
        airline_namie = infoDestination[5]

        infoOrigin = informationOrgin(first_cheapper_url)
        originPlace= infoOrigin[0]
        nameOrginplace = infoOrigin[1]
        countryOrginplace = infoOrigin[2]

        infoOrigin2= informationOrgin(second_cheapper_url)
        nameOrginplace2 = infoOrigin2[1]
        countryOrginplace2 = infoOrigin2[2]

        infoDestination2 = informationDestination(second_cheapper_url)
        departureDate2 = infoDestination2[0]
        nameDestinationplace2 = infoDestination2[1]
        countryDestination2 = infoDestination2[2]
        carrier2 =infoDestination2[4]
        airline_namie2 = infoDestination2[5]

        return render(request, 'fly/results2.html', {
            'second_cheapper_price': second_cheapper_price,
            'first_cheapper_price': first_cheapper_price,
            'first_cheapper_url': first_cheapper_url,
            'destinationPlace': destinationPlace,
            'final_price': final_price,
            'nextdate': nextdate,
            'departureDate': departureDate,
            'nameDestinationplace': nameDestinationplace,
            'countryDestination': countryDestination,
            'originPlace': originPlace,
            'nameOrginplace': nameOrginplace,
            'countryOrginplace': countryOrginplace,
            'nameOrginplace2': nameOrginplace2,
            'countryOrginplace2': countryOrginplace2,
            'departureDate2': departureDate2,
            'nameDestinationplace2': nameDestinationplace2,
            'countryDestination2':countryDestination2,
            'carrier': carrier,
            'airline_name': airline_namie,
            'carrier2': carrier2,
            'airline_name2': airline_namie2,
        })
    elif(fly.number_city==2 and fly.day != 0 ):
        print("Petla gdzie odwiedzamy dwa miasta")

        all_airports = create_airports(fly.airports.name2, fly.airports.name3, fly.airports.name4)
        airports = removeWrongElement(all_airports)
        print(airports)
        first_fly = search_fly_originAndDestination(list_airport_orgiplace, airports, currency, date)
        first_cheapper_price = first_fly[1]
        first_cheapper_url = first_fly[0]
        print(first_cheapper_url)

        infoDestination = informationDestination(first_cheapper_url)
        departureDate = infoDestination[0]
        nameDestinationplace = infoDestination[1]
        countryDestination =infoDestination[2]
        carrier =infoDestination[4]
        airline_namie = infoDestination[5]
        destinationPlace = infoDestination[3]
        destinationPlaceName = destinationPlace + "-sky"
        print(destinationPlaceName)
        print(type(destinationPlaceName))
        print(airports)
        airports.remove(destinationPlaceName)

        nextdate = new_date(date, days)
        second_fly = searchXandDestination(destinationPlace, airports,currency,nextdate)

        second_cheapper_url = second_fly[0]
        second_cheapper_price = second_fly[1]

        infoDestination2 = informationDestination(second_cheapper_url)
        departureDate2 = infoDestination2[0]
        nameDestinationplace2 = infoDestination2[1]
        countryDestination2 = infoDestination2[2]
        carrier2 =infoDestination2[4]
        airline_namie2 = infoDestination2[5]
        destinationPlace2= infoDestination2[3]
        nextdate2 = new_date(nextdate, days)

        third_fly = searchXandDestination(destinationPlace2, list_airport_destinatonplace,currency,nextdate2)
        third_cheapper_pice = third_fly[1]
        third_cheapper_url = third_fly[0]

        final_price= first_cheapper_price + second_cheapper_price + third_cheapper_pice


        infoOrigin = informationOrgin(first_cheapper_url)
        originPlace= infoOrigin[0]
        nameOrginplace = infoOrigin[1]
        countryOrginplace = infoOrigin[2]

        infoOrigin2 = informationOrgin(second_cheapper_url)
        nameOrginplace2 = infoOrigin2[1]
        countryOrginplace2 = infoOrigin2[2]

        infoOrigin3 = informationOrgin(third_cheapper_url)
        nameOrginplace3 = infoOrigin3[1]
        countryOrginplace3 = infoOrigin3[2]

        infoDestination3 = informationDestination(third_cheapper_url)
        departureDate3 = infoDestination3[0]
        nameDestinationplace3 = infoDestination3[1]
        countryDestination3 = infoDestination3[2]
        carrier3 =infoDestination3[4]
        airline_namie3= infoDestination3[5]

        return render(request, 'fly/results3.html', {
            'destinationPlace': destinationPlace,
            'destinationPlace2': destinationPlace2,
            'final_price': final_price,
            'nextdate': nextdate,
            'nextdate2':nextdate2,
            'departureDate': departureDate,
            'nameDestinationplace': nameDestinationplace,
            'countryDestination': countryDestination,
            'originPlace': originPlace,
            'nameOrginplace': nameOrginplace,
            'countryOrginplace': countryOrginplace,
            'nameOrginplace2': nameOrginplace2,
            'countryOrginplace2': countryOrginplace2,
            'departureDate2': departureDate2,
            'nameDestinationplace2': nameDestinationplace2,
            'countryDestination2': countryDestination2,
            'nameOrginplace3':nameOrginplace3,
            'countryOrginplace3':countryOrginplace3,
            'departureDate3':departureDate3,
            'nameDestinationplace3':nameDestinationplace3,
            'countryDestination3':countryDestination3,
            'third_cheapper_pice': third_cheapper_pice,
            'carrier': carrier,
            'airline_name': airline_namie,
            'carrier2': carrier2,
            'airline_name2': airline_namie2,
            'carrier3': carrier3,
            'airline_name3': airline_namie3,
            'second_cheapper_price': second_cheapper_price,
            'first_cheapper_price':first_cheapper_price,
            'currency': currency,
        })
    elif ( fly.number_city ==3 and fly.day != 0):
        print("petla w ktorej odwiedzmy trzy miasta")
        all_airports = create_airports(fly.airports.name2, fly.airports.name3, fly.airports.name4)
        airports = removeWrongElement(all_airports)
        first_fly = search_fly_originAndDestination(list_airport_orgiplace, airports, currency, date)
        first_cheapper_price = first_fly[1]
        first_cheapper_url = first_fly[0]

        infoDestination = informationDestination(first_cheapper_url)
        departureDate = infoDestination[0]
        nameDestinationplace = infoDestination[1]
        countryDestination = infoDestination[2]
        destinationPlace = infoDestination[3]
        carrier =infoDestination[4]
        airline_namie = infoDestination[5]

        nextdate = new_date(date,days)
        destinationPlaceName = destinationPlace + "-sky"
        print(destinationPlaceName)
        print(type(destinationPlaceName))
        print(airports)
        airports.remove(destinationPlaceName)

        second_fly = searchXandDestination(destinationPlace, airports, currency, nextdate)
        second_cheapper_url = second_fly[0]
        second_cheapper_price = second_fly[1]

        infoDestination2 = informationDestination(second_cheapper_url)
        departureDate2 = infoDestination2[0]
        nameDestinationplace2 = infoDestination2[1]
        countryDestination2 = infoDestination2[2]
        destinationPlace2 = infoDestination2[3]
        carrier2 =infoDestination2[4]
        airline_namie2 = infoDestination2[5]

        nextdate2 = new_date(nextdate,days)
        destinationPlace2Name = destinationPlace2 + "-sky"
        print("asldkaslkdslakdlskdlskdlskdlskldksldklskdls")
        print(second_cheapper_url)
        print(airports)
        print(destinationPlace2Name)
        airports.remove(destinationPlace2Name)

        third_fly = searchXandDestination(destinationPlace2, airports, currency, nextdate2)
        third_cheapper_url = third_fly[0]
        third_cheapper_pice = third_fly[1]

        infoDestination3 = informationDestination(third_cheapper_url)
        departureDate3 = infoDestination3[0]
        nameDestinationplace3 = infoDestination3[1]
        countryDestination3 = infoDestination3[2]
        destinationPlace3 = infoDestination3[3]
        carrier3 =infoDestination3[4]
        airline_namie3 = infoDestination3[5]

        nextdate3 =new_date(nextdate2,days)
        destinationPlace3Name = destinationPlace3 + "-sky"
        airports.remove(destinationPlace3Name)

        fourth_fly = searchXandDestination(destinationPlace3,list_airport_destinatonplace,currency,nextdate3)
        fourth_cheapper_url= fourth_fly[0]
        fourth_cheapper_pice = fourth_fly[1]

        final_price= first_cheapper_price + second_cheapper_price + third_cheapper_pice+fourth_cheapper_pice



        infoOrigin = informationOrgin(first_cheapper_url)
        originPlace= infoOrigin[0]
        nameOrginplace = infoOrigin[1]
        countryOrginplace = infoOrigin[2]

        infoOrigin2 = informationOrgin(second_cheapper_url)
        nameOrginplace2 = infoOrigin2[1]
        countryOrginplace2 = infoOrigin2[2]


        infoOrigin3 = informationOrgin(third_cheapper_url)
        nameOrginplace3 = infoOrigin3[1]
        countryOrginplace3 = infoOrigin3[2]

        infoOrigin4 = informationOrgin(fourth_cheapper_url)
        nameOrginplace4 = infoOrigin4[1]
        countryOrginplace4 = infoOrigin4[2]

        infoDestination4 = informationDestination(fourth_cheapper_url)
        departureDate4 = infoDestination4[0]
        nameDestinationplace4 = infoDestination4[1]
        countryDestination4 = infoDestination4[2]
        carrier4 =infoDestination4[4]
        airline_namie4 = infoDestination4[5]
        return render(request, 'fly/results.html', {
            'destinationPlace': destinationPlace,
            'destinationPlace2': destinationPlace2,
            'final_price': final_price,
            'nextdate': nextdate,
            'nextdate2': nextdate2,
            'nextdate3': nextdate3,
            'departureDate': departureDate,
            'nameDestinationplace': nameDestinationplace,
            'countryDestination': countryDestination,
            'originPlace': originPlace,
            'nameOrginplace': nameOrginplace,
            'countryOrginplace': countryOrginplace,
            'nameOrginplace2': nameOrginplace2,
            'countryOrginplace2': countryOrginplace2,
            'departureDate2': departureDate2,
            'nameDestinationplace2': nameDestinationplace2,
            'countryDestination2': countryDestination2,
            'nameOrginplace3': nameOrginplace3,
            'countryOrginplace3': countryOrginplace3,
            'departureDate3': departureDate3,
            'nameDestinationplace3': nameDestinationplace3,
            'countryDestination3': countryDestination3,
            'third_cheapper_pice': third_cheapper_pice,
            'nameOrginplace4':nameOrginplace4,
            'countryOrginplace4':countryOrginplace4,
            'departureDate4':departureDate4,
            'nameDestinationplace4':nameDestinationplace4,
            'countryDestination4':countryDestination4,
            'fourth_cheaper_price':fourth_cheapper_pice,
            'carrier': carrier,
            'airline_name': airline_namie,
            'carrier2': carrier2,
            'airline_name2': airline_namie2,
            'carrier3': carrier3,
            'airline_name3': airline_namie3,
            'carrier4': carrier4,
            'airline_name4': airline_namie4,
            'second_cheapper_price': second_cheapper_price,
            'first_cheapper_price': first_cheapper_price,
            'currency': currency,
        })
    elif(fly.price != 0 and fly.number_city == 0 and fly.day !=0 and fly.endDate == None):

        print("petla gdze jest podana cena i ile dni chcemy zwiedzac ale bez koncowej daty ")
        all_airports = create_airports(fly.airports.name2, fly.airports.name3, fly.airports.name4)
        print(all_airports)
        airports = removeWrongElement(all_airports)
        city = []
        print("lotniska w fcji : ")
        print(airports)
        first_fly = search_fly_originAndDestination(list_airport_orgiplace,airports,currency,date)
        first_cheapper_url= first_fly[0]
        first_cheapper_price = first_fly[1]
        trip = []
        trip.append(first_cheapper_url)
        final_price = first_cheapper_price

        destinationName = []

        prices = []
        prices.append(first_cheapper_price)
        infoDestination = informationDestination(first_cheapper_url)
        destinationPlaceNN = infoDestination[3]  #to mi zwraca stringa a nie liste gdy uzyje fcji informationDestination
        carrier =infoDestination[4]
        airline_namie = infoDestination[5]

        number = 0
        destinationPlace = destinationPlaceNN.split() #teraz to lista

        nextdate = new_date(date, days)
        print("nextdate przed petla while")
        print(nextdate)

        while (final_price < fly.price):
            toremove = ''.join(map(str, destinationPlace[number])) + "-sky"  # nie działa bo destinatnionPlace to teraz string, juz powinno dzialac
            print("pętla while, numer pętli to ")
            print(number)
            print(toremove)
            airports.remove(toremove)
            print("miasta w petli to ")
            print(airports)

            price_dict = {}
            flyInWhile = searchXandDestination(destinationPlace[number],airports,currency,nextdate)
            next_cheapper_url =flyInWhile[0]
            next_cheapper_price = flyInWhile[1]
            trip.append(next_cheapper_url)
            print("pętla while przed funkcją zmiany daty,   data to ::::")
            print(nextdate)
            nextdate=new_date2(nextdate,days)
            print("pętla while, po zmiane daty nowa data to ::::")
            print(nextdate)
            prices.append(next_cheapper_price)
            number+=1
            final_price +=next_cheapper_price

            nextInformation = informationDestination(next_cheapper_url)
            destinationName.append(nextInformation[1])
            destinationPlace.append(nextInformation[3])
        #departureDate, nameDestinationplace, countryDestination, destinationPlace, carrier, airline

        contexforpodroz =[]
        for url in trip:
            contex = {
                'departureDate_fly': informationDestination(url)[0],
                'nameDestinationplace_fly':informationDestination(url)[1],
                'countryDestination_fly':informationDestination(url)[2],
                'originPlace_fly':informationOrgin(url)[0],
                'nameOrginplace_fly': informationOrgin(url)[1],
                'countryOrginplace_fly':informationOrgin(url)[2],
                'carrier': informationDestination(url)[4],
                'airline_name': informationDestination(url)[5],
                'price': informationDestination(url)[6],
            }
            contexforpodroz.append(contex)


        return render(request, 'fly/results5.html', {'contexforpodroz': contexforpodroz})

    #dobra, nowa f-cj , mamy dwie daty ( jakis zakres czasu ) i szukamy najtanszego polaczenia pomiedzy dwoma miastemi
    elif(endDate != None and fly.price == 0):
        counter = 0
        days=1
        start = str(date)
        fstart = str(date)
        end = str(endDate)
        start_day = int(start[8:10])  # daje mi dzien w int np 7
        end_day = int(end[8:10])
        interval = end_day - start_day
        s = requests.Session()
        s.headers.update({"X-RapidAPI-Key": "7e1987716emshd8e087e4d068a79p1b259ejsna8f84b8ca1e1"})
        for x in list_airport_orgiplace:
            for y in list_airport_destinatonplace:
                for z in range(0, interval):
                    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/" + currency + "/en-US/" + x + "/" + y + "/" + start
                    a = s.get(url).json()
                    print(url)
                    start = new_date(start, days)
                    counter += 1

                    if start == end:
                        start = fstart
                    try:
                        quote = a["Quotes"]
                        pricequote = quote[0]['MinPrice']
                        price.update({pricequote: url})
                    except IndexError:
                        print("nie ma takiego lotu ")
        print("Liczba zapytan to ")
        print(counter)
        first_cheapper_price = (sorted(price.items())[0][0])
        first_cheapper_url = (sorted(price.items())[0][1])
        infoDestination = informationDestination(first_cheapper_url)
        departureDate = infoDestination[0]
        nameDestinationplace = infoDestination[1]
        countryDestination = infoDestination[2]
        carrier =infoDestination[4]
        airline_namie = infoDestination[5]
        infoOrigin = informationOrgin(first_cheapper_url)
        originPlace= infoOrigin[0]
        nameOrginplace = infoOrigin[1]
        countryOrginplace = infoOrigin[2]

        print("posortowane ceny i url'e pierwszego lotu ")
        print(first_cheapper_price)
        print(first_cheapper_url)


        return render(request, 'fly/results6.html',{
            'first_cheapper_price': first_cheapper_price,
            'first_cheapper_url': first_cheapper_url,
            'departureDate': departureDate,
            'nameDestinationplace': nameDestinationplace,
            'countryDestination': countryDestination,
            'originPlace': originPlace,
            'nameOrginplace': nameOrginplace,
            'countryOrginplace': countryOrginplace,
            'carrier':carrier,
            'airline_name':airline_namie,
            'currency':currency
        })
    elif(endDate != None and fly.price != 0):
        fly1_url = []
        fly2_url = []
        fly3_url = []
        prices1 = []
        prices2 = []
        prices3 = []

        originName = []
        originName.append(originplace)
        all_airports = create_airports(fly.airports.name2, fly.airports.name3, fly.airports.name4)
        print(all_airports)
        airports = removeWrongElement(all_airports)
        print(airports)
        counter = 0

        start = str(date)
        fstart = str(date)
        end = str(endDate)

        start_day = int(start[8:10])  # daje mi dzien w int np 7
        end_day = int(end[8:10])
        interval = int((end_day - start_day)/2)    #zakladam ze chce poleciec w pierwszej polowie wyznaczonego prze sb czasu

        if currency =="PLN":
            diff = 180
        else:
            diff= 60

        s = requests.Session()
        s.headers.update({"X-RapidAPI-Key": "a1b3e35e10msh006c21e5b5f6617p1a0708jsn1dd2d3f443b5"})
        for x in list_airport_orgiplace:
            for y in airports:
                for z in range(0, interval):
                    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/" + currency + "/en-US/" + x + "/" + y + "/" + start
                    a = s.get(url).json()
                    print(url)
                    start = new_date(start, days)
                    counter += 1

                    if start == end:
                        start = fstart
                    try:
                        quote = a["Quotes"]
                        pricequote = quote[0]['MinPrice']
                        price.update({pricequote: url})
                    except IndexError:
                        print("nie ma takiego lotu ")
        fly1_first_cheapper_price = (sorted(price.items())[0][0])
        fly1_first_cheapper_url = (sorted(price.items())[0][1])
        fly2_first_cheapper_price = (sorted(price.items())[1][0])
        fly2_first_cheapper_url = (sorted(price.items())[1][1])
        fly3_first_cheapper_price = (sorted(price.items())[2][0])
        fly3_first_cheapper_url = (sorted(price.items())[2][1])

        # wyciaganie daty z URL
        fly_1_date1 = fly1_first_cheapper_url[len(fly1_first_cheapper_url)-10: len(fly1_first_cheapper_url)]
        fly_2_date1 = fly2_first_cheapper_url[len(fly2_first_cheapper_url)-10: len(fly2_first_cheapper_url)]
        fly_3_date1 = fly3_first_cheapper_url[len(fly3_first_cheapper_url)-10: len(fly3_first_cheapper_url)]

        destinationPlace_1s = informationDestination(fly1_first_cheapper_url)[3]
        destinationPlace_1 = destinationPlace_1s.split()
        destinationPlace_2s = informationDestination(fly2_first_cheapper_url)[3]
        destinationPlace_2 = destinationPlace_2s.split()
        destinationPlace_3s = informationDestination(fly3_first_cheapper_url)[3]
        destinationPlace_3 = destinationPlace_3s.split()

#final prices mi jest potrzebne do zobaczniea kiedy petla ma sie skończyć a prices do przypisania konkratych cen
        final_price_1 = fly1_first_cheapper_price
        final_price_2 = fly2_first_cheapper_price
        final_price_3 = fly3_first_cheapper_price
        #listy pices i fly url ?
        prices1.append(fly1_first_cheapper_price)
        prices2.append(fly2_first_cheapper_price)
        prices3.append(fly3_first_cheapper_price)
        fly1_url.append(fly1_first_cheapper_url)
        fly2_url.append(fly2_first_cheapper_url)
        fly3_url.append(fly3_first_cheapper_url)
        number=0
        nextdate1= new_date(fly_1_date1,days)
        nextdate2= new_date(fly_2_date1,days)
        nextdate3= new_date(fly_3_date1, days)

    #dobra zajmujemy się na początku pierwszym lotem
        #apka nie musi byc dokładna zakładam ze na lot powrotny przeznaczam np kolo 200 zl lub 50 dolcow
        print("Informacje przed wejsciem do while !------------------------------!!")
        print(fly1_first_cheapper_price)
        print(fly1_first_cheapper_url)
        print(fly_1_date1)
        print(destinationPlace_1)
        print(final_price_1)

        while(final_price_1 < (fly.price - diff)):
            toremove = ''.join(map(str, destinationPlace_1[number])) + "-sky"  # nie działa bo destinatnionPlace to teraz string
            print(toremove)
            airports.remove(toremove)
            print("miasta w petli to ")
            print(airports)

            nextFly = searchXandDestination(destinationPlace_1[number],airports,currency,nextdate1)
            next_cheapper_url = nextFly[0]
            next_cheapper_price = nextFly[1]
            print("kolejny najtanszy lot i cena to : ------------------------------")
            print(next_cheapper_price)
            print(next_cheapper_url)
            nextdate1 = new_date2(nextdate1, days)

            prices1.append(next_cheapper_price)
            print("Lista kolejnych cen to ----------------")
            print(prices1)

            number += 1
            final_price_1 += next_cheapper_price
            print("cena koncowa ----------------------------- :")
            print(final_price_1)
            fly1_url.append(next_cheapper_url)
            print("zapisane URL kolejnych miast to ")
            print(fly1_url)

            nextInformation = informationDestination(next_cheapper_url)
            destinationPlace_1.append(nextInformation[3])

        #liczenie lotu powrotnego :)
        returnFly = searchXandDestination(destinationPlace_1[number],list_airport_destinatonplace,currency,nextdate1)
        last_cheapper_url = returnFly[0]
        last_cheapper_price = returnFly[1]
        print("Lot powrotny !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(last_cheapper_price)
        print(last_cheapper_url)
        final_price_1 += last_cheapper_price
        fly1_url.append(last_cheapper_url)
        prices1.append(last_cheapper_price)

        number=0
        all_airports = create_airports(fly.airports.name2, fly.airports.name3, fly.airports.name4)
        airports = removeWrongElement(all_airports)
        print(airports)
        print("pierwszy url drugiego lotu to        to ")
        print(destinationPlace_2)

        while(final_price_2 < (fly.price-diff)):
            toremove = ''.join(map(str, destinationPlace_2[number])) + "-sky"  # nie działa bo destinatnionPlace to teraz string
            airports.remove(toremove)

            nextFly = searchXandDestination(destinationPlace_2[number],airports,currency,nextdate2)
            next_cheapper_url = nextFly[0]
            next_cheapper_price = nextFly[1]
            print("kolejny najtanszy lot i cena to : ------------------------------")
            print(next_cheapper_price)
            print(next_cheapper_url)
            nextdate2 = new_date2(nextdate2, days)

            prices2.append(next_cheapper_price)
            number += 1
            final_price_2 += next_cheapper_price
            fly2_url.append(next_cheapper_url)

            nextInformation = informationDestination(next_cheapper_url)
            destinationPlace_2.append(nextInformation[3])
        #liczenie lotu powrotnego :)
        returnFly = searchXandDestination(destinationPlace_2[number],list_airport_destinatonplace,currency,nextdate2)
        last_cheapper_url2 = returnFly[0]
        last_cheapper_price2 = returnFly[1]
        print("Lot powrotny !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(last_cheapper_price2)
        print(last_cheapper_url2)
        final_price_2 += last_cheapper_price2
        fly2_url.append(last_cheapper_url)
        prices2.append(last_cheapper_price)

        number=0
        all_airports = create_airports(fly.airports.name2, fly.airports.name3, fly.airports.name4)
        airports = removeWrongElement(all_airports)
        print(airports)
        print("Informacje przed wejsciem do trzeciej petli while !------------------------------!!")
        print(fly3_first_cheapper_price)
        print(fly3_first_cheapper_url)
        print(fly_3_date1)
        print(destinationPlace_3)
        print(final_price_3)
        print(destinationPlace_3[number])
        while(final_price_3 < (fly.price-diff)):
            print("wchodizmy do 3 while ------------------>>_>_>_>_>_>_>_>_>_>_>_>_>_>_>_>_>_>_>_>_>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("miasta przed remove")
            print(airports)
            toremove = ''.join(map(str, destinationPlace_3[number])) + "-sky"  # nie działa bo destinatnionPlace to teraz string
            print(toremove)
            airports.remove(toremove)

            nextFly = searchXandDestination(destinationPlace_3[number],airports,currency,nextdate3)
            next_cheapper_url = nextFly[0]
            next_cheapper_price = nextFly[1]
            print("kolejny najtanszy lot i cena to : ------------------------------")
            print(next_cheapper_price)
            print(next_cheapper_url)
            nextdate3 = new_date2(nextdate3, days)

            prices3.append(next_cheapper_price)

            number += 1
            final_price_3 += next_cheapper_price
            print("cena koncowa ----------------------------- :")
            print(final_price_3)
            fly3_url.append(next_cheapper_url)

            nextInformation = informationDestination(next_cheapper_url)
            destinationPlace_3.append(nextInformation[3])
        #liczenie lotu powrotnego :)
        returnFly = searchXandDestination(destinationPlace_3[number], list_airport_destinatonplace, currency, nextdate2)
        last_cheapper_url3 = returnFly[0]
        last_cheapper_price3 = returnFly[1]
        print("Lot powrotny !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(last_cheapper_price3)
        print(last_cheapper_url3)
        final_price_3 += last_cheapper_price3
        fly3_url.append(last_cheapper_url)
        prices3.append(last_cheapper_price)

        print("koniecccc<!,,<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,")
        context_array = []
        # fly1_url = ['https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/PLN/en-US/CIA-sky/IT-sky/2019-04-03']
        #fly2_url =['https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/PLN/en-US/CIA-sky/IT-sky/2019-04-19','https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/PLN/en-US/CIA-sky/BGY-sky/2019-04-20']
        #fly3_url =['https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/PLN/en-US/CIA-sky/NAP-sky/2019-04-20']
        for podorz in (fly1_url, fly2_url, fly3_url):
            contexforpodroz =[]
            for url in podorz:
                contex = {
                    'departureDate_fly': informationDestination(url)[0],
                    'nameDestinationplace_fly':informationDestination(url)[1],
                    'countryDestination_fly':informationDestination(url)[2],
                    'originPlace_fly':informationOrgin(url)[0],
                    'nameOrginplace_fly': informationOrgin(url)[1],
                    'countryOrginplace_fly':informationOrgin(url)[2],
                    'carrier': informationDestination(url)[4],
                    'airline_name': informationDestination(url)[5],
                    'price': informationDestination(url)[6],
                }
                contexforpodroz.append(contex)
            context_array.append(contexforpodroz)


        return render(request, 'fly/results7.html', {'context_array': context_array})
    else:
        return render(request, 'fly/wrong_results.html')



