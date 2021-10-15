import urllib.parse
import requests
import webbrowser

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "b4eOrBzps7qO2qrKvbeN32RK8f0qtAns"

#map_api = "https://www.mapquestapi.com/staticmap/v4/getmap?size=400,300&pois=default,37.819722,-122.478611|default,37.799,-122.4664&key=KEY"
finmap1 = "http://mapq.st/map?q="
finmap2 = "80202&maptype=map"

while True:
    #user is asked to input starting location
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    #user is asked to input destination location
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    #outputs information about the directions for the trip
    if json_status == 0:
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print((each["narrative"]) + " (" +
            str("{:.2f}".format((each["distance"])*1.61) + " km)"))
            print("=============================================\n")

        openmap = input('Do you want to open the map?')
        if openmap == "yes" or openmap == "y":
            webbrowser.open(finmap1 + orig + ' ' + dest + finmap2)  # Go to example.com
        
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from " + (orig) + " to " + (dest))
        print("Trip Duration: " + (json_data["route"]["formattedTime"]))

        print('Tunnel: ' + str(json_data["route"]["hasTunnel"]))
        print('Highway: ' + str(json_data["route"]["hasHighway"]))
        
        print("Kilometers: " +
        str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        print("Fuel Used (Ltr): " +
        str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))

        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
            print("=============================================\n")
    
    #error handling
    elif json_status == 402:
            print("**********************************************")
            print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
            print("**********************************************\n")
    elif json_status == 611:
            print("**********************************************")
            print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
            print("**********************************************\n")
    else:
            print("************************************************************************")
            print("For Staus Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            print("************************************************************************\n")



       