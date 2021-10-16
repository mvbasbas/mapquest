import tkinter
from tkinter import *
import urllib.parse
import requests
import webbrowser
from tkinter import messagebox

main_api = "https://www.mapquestapi.com/directions/v2/route?"
finmap1 = "http://mapq.st/map?q="
finmap2 = "80202&maptype=map"
key = "b4eOrBzps7qO2qrKvbeN32RK8f0qtAns"

window = Tk()


window.title("Devnet Project")
window.config(background = "#bb6c5d")

intro = Label(
            window,
            text = "WELCOME TO MAPQUEST",
            bg ="#bb6c5d",
            fg ="white",
            font ='Arial 40 bold')
intro.pack(ipady = 25)

window.geometry('1950x1100')

middleframe1 = Frame(
                    window,
                    bg = "#bb6c5d")
middleframe1.pack()

middleframe2 = Frame(
                    window,
                    bg = "#bb6c5d")
middleframe2.pack()

middleframe3 = Frame(
                    window,
                    bg = "#bb6c5d")
middleframe3.pack()


inputLabelLoc= Label(middleframe1,
                  text = 'Starting Location: ',
                  bg = '#bb6c5d',
                  fg = 'white',
                  font = 'Arial 15 bold')
inputLabelLoc.pack(side = LEFT)

textLoc = StringVar()
inputTextLoc = Entry(middleframe1,
                  textvariable = textLoc,
                  bd = 2,
                  width = 30,
                  font = 'Arial 12')
inputTextLoc.pack(side = LEFT, ipady=5)

inputLabelDest= Label(middleframe2,
                  text = 'Destination: ',
                  bg = '#bb6c5d',
                  fg = 'white',
                  font = 'Arial 15 bold')
inputLabelDest.pack(side = LEFT, ipadx=7, pady=8)

textDest = StringVar()
inputTextDest = Entry(middleframe2,
                  textvariable = textDest,
                  bd = 2,
                  width = 35,
                  font = 'Arial 12')
inputTextDest.pack(side = LEFT, ipady=5, pady=8)

def clearData():
    
    inputTextDest.delete(0, 'end')
    inputTextLoc.delete(0, 'end')
    outputURL.destroy()
    line1.destroy()

    if json_status == 0:
        outputDistance.destroy()
        outputDistanceRoute.destroy()
        outputRoute.destroy()
        line2.destroy()
        outputStatus.destroy()
        outputTrip.destroy()
        line3.destroy()
        outputDuration.destroy()

def outputData():
    global orig
    global dest
    orig = inputTextLoc.get()
    dest = inputTextDest.get()
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    
    global outputURL
    outputURL = Label(window,
                text= "\n URL: " + url,
                bg = '#bb6c5d',
                fg = 'white',
                font = 'Arial 12')
    outputURL.pack(pady = 5)  
    
    global json_status
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    global line1
    line1 = Canvas(window, width=1700, height=3)
    line1.create_rectangle(0, 0, 1700, 3, fill="white", outline = 'white')
    line1.pack()

    
    listDist = []
    if json_status == 0:
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            listDist.append((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))

        printdistance = str(listDist).replace("{","").replace("}", "").replace("'", "").replace("[", "").replace("]", "").replace(",", "\n")

        global outputDistanceRoute
        outputDistanceRoute = Label(window,
                    text = "Route Directions",
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Arial 14 bold')
        outputDistanceRoute.pack(pady = 5) 

        global outputDistance
        outputDistance = Label(window,
                    text = printdistance,
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Arial 12 italic')
        outputDistance.pack(pady = 5) 


        global line2
        line2 = Canvas(window, width=1700, height=3)
        line2.create_rectangle(0, 0, 1700, 3, fill="white", outline = 'white')
        line2.pack()

        global outputStatus
        outputStatus = Label(window,
                    text = "API Status: " + str(json_status) + " = A successful route call.",
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Arial 12')
        outputStatus.pack(pady = 5) 

        global line3
        line3 = Canvas(window, width=1700, height=3)
        line3.create_rectangle(0, 0, 1700, 3, fill="white", outline = 'white')
        line3.pack()

        global outputTrip
        outputTrip = Label(window,
                    text = "Directions from " + (orig) + " to " + (dest),
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Arial 12')
        outputTrip.pack(pady = 5) 

        Duration = "Trip Duration: " + (json_data["route"]["formattedTime"])
        Kilometers = "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61))
        Fuel = "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))

        global outputDuration
        outputDuration = Label(window,
                    text = Duration + "\n" + Kilometers + "\n" +Fuel,
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Arial 12')
        outputDuration.pack(pady = 5) 

        Tunnel = 'Tunnel: ' + str(json_data["route"]["hasTunnel"])
        Highway = 'Highway: ' + str(json_data["route"]["hasHighway"])

        global outputRoute
        outputRoute = Label(window,
                    text = Tunnel + "\n" + Highway,
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Arial 12')
        outputRoute.pack(pady = 5) 
    
    elif json_status == 402:
        messagebox.showerror("Error","Status Code: " + str(json_status) + "\n Invalid user inputs for one or both locations.")
    
    elif json_status == 611:
        messagebox.showerror("Error","Status Code: " + str(json_status) + "\n Missing an entry for one or both locations.")

    else:
        messagebox.showerror("Error","For Status Code: " + str(json_status) + "\n Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes")

def openMap():
    webbrowser.open(finmap1 + orig + ' ' + dest + finmap2)

        

submitBtn = Button(middleframe3,
            text = "SUBMIT",
            width = 20,
            activebackground = '#741519',
            activeforeground = 'white',
            font = 'Arial',
            command = outputData)
submitBtn.pack(side = LEFT, padx = 5)

clearBtn = Button(
                  middleframe3,
                  text = 'RESET',
                  width = 20,
                  activebackground = '#741519',
                  activeforeground = 'white',
                  font = 'Arial',
                  command=clearData)
clearBtn.pack(side = LEFT, padx = 5)

openMapBtn = Button(
                  middleframe3,
                  text = 'MAP',
                  width = 20,
                  activebackground = '#741519',
                  activeforeground = 'white',
                  font = 'Arial',
                  command=openMap)
openMapBtn.pack(padx = 5)

window.mainloop()
