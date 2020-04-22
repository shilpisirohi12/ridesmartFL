import requests
import pprint
#Google API key
google_api_key='AIzaSyCsLWxyNUgQgw10TDoSyiIy4n7sjAeEIrk'
countyName = [
  "Charlotte",
  "Citrus",
  "Collier",
  "Desoto",
  "Glades",
  "Hardee",
  "Hendry",
  "Hernando",
  "Highlands",
  "Hillsborough",
  "Lake",
  "Lee",
  "Manatee",
  "Pasco",
  "Pinellas",
  "Polk",
  "Sarasota",
  "Sumter",
  "Alachua",
  "Baker",
  "Bradford",
  "Columbia",
  "Dixie",
  "Gilchrist",
  "Hamilton",
  "Lafayette",
  "Levy",
  "Madison",
  "Marion",
  "Suwannee",
  "Taylor",
  "Union",
  "Bay",
  "Calhoun",
  "Escambia",
  "Franklin",
  "Gadsden",
  "Gulf",
  "Holmes",
  "Jackson",
  "Jefferson",
  "Leon",
  "Liberty",
  "Okaloosa",
  "Santa Rosa",
  "Wakulla",
  "Walton",
  "Washington",
  "Brevard",
  "Clay",
  "Duval",
  "Flagler",
  "Nassau",
  "Orange",
  "Putnam",
  "Seminole",
  "St Johns",
  "Volusia",
  "Broward",
  "Miami-Dade",
  "Indian River",
  "Martin",
  "Monroe",
  "Okeechobee",
  "Osceola",
  "Palm Beach",
  "St Lucie",
]

geoCounty=[]
for dt in countyName:
    address=dt+",Florida";
    url = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}'.format(google_api_key, address)
    data=requests.get(url).json()
    latlng=data['results'][0]["geometry"]["location"]
    dictObj={}
    dictObj["county"] =dt
    dictObj['latitude']=latlng['lat']
    dictObj['longitude']=latlng['lng']
    print(dictObj)
    geoCounty.append(dictObj)
print(geoCounty)

