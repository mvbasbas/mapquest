import tkinter 
from tkinter import *
from PIL import ImageTk, Image
import urllib.parse
import requests
import webbrowser
from tkinter import messagebox

main_api = "https://www.mapquestapi.com/directions/v2/route?"
finmap1 = "http://mapq.st/map?q="
finmap2 = "80202&maptype=map"
key = "b4eOrBzps7qO2qrKvbeN32RK8f0qtAns"

#added GUI

canvas = Tk()

canvas.title("Devnet Project")

#added background color #bb6c5d
canvas.config(background = "white")


#inserting image
path = "pic.png"

mapquest_image = Image.open(path)
mapquest_resizemage = mapquest_image.resize((1100,260))
mapquest_finimage = ImageTk.PhotoImage(mapquest_resizemage)
mapquest_image_label = tkinter.Label(canvas, image = mapquest_finimage,)
mapquest_image_label.pack(side = "top", fill = "x", expand = "no")
# mapquest_image = ImageTk.PhotoImage(Image.open(path))
# mapquest_image_label = tkinter.Label(canvas, image = mapquest_image, height = 200, width = 100)
# mapquest_image_label.pack(side = "top", fill = "none", expand = "no")




# img = ImageTk.PhotoImage(mapquest_resizemage)
# label1 = tkinter.Label(canvas, image=img)
# label1.image = img
# label1.pack()



#title
intro = Label(
            canvas,
            text = "WELCOME TO MAPQUEST",
            bg ="#bb6c5d",
            fg ="white",
            font ='Raleway 40 bold')
intro.pack(ipady = 25)


#canvas resolution/size
canvas.geometry('1950x1100')

middleframe1 = Frame(
                    canvas,
                    bg = "#bb6c5d")
middleframe1.pack()

middleframe2 = Frame(
                    canvas,
                    bg = "#bb6c5d")
middleframe2.pack()

middleframe3 = Frame(
                    canvas,
                    bg = "#bb6c5d")
middleframe3.pack()

#input textbox for starting location 
inputLabelLoc= Label(middleframe1,
                  text = 'Starting Location: ',
                  bg = '#bb6c5d',
                  fg = 'white',
                  font = 'Raleway 15 bold')
inputLabelLoc.pack(side = LEFT)

textLoc = StringVar()
inputTextLoc = Entry(middleframe1,
                  textvariable = textLoc,
                  bd = 2,
                  
                  width = 30,
                  font = 'Raleway 12')
inputTextLoc.pack(side = LEFT, ipady=5)

#input textbox for destination location 
inputLabelDest= Label(middleframe2,
                  text = 'Destination: ',
                  bg = '#bb6c5d',
                  fg = 'white',
                  font = 'Raleway 15 bold')
inputLabelDest.pack(side = LEFT, ipadx=7, pady=8)

textDest = StringVar()
inputTextDest = Entry(middleframe2,
                  textvariable = textDest,
                  bd = 2,
                  width = 35,
                  font = 'Raleway 12')
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
    outputURL = Label(canvas,
                text= "\n URL: " + url,
                bg = '#bb6c5d',
                fg = 'white',
                font = 'Raleway 12')
    outputURL.pack(pady = 5)  
    
    global json_status
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    global line1
    line1 = Canvas(canvas, width=1700, height=3)
    line1.create_rectangle(0, 0, 1700, 3, fill="white", outline = 'white')
    line1.pack()

    
    listDist = []
    if json_status == 0:
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            listDist.append((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))

        printdistance = str(listDist).replace("{","").replace("}", "").replace("'", "").replace("[", "").replace("]", "").replace(",", "\n")

        global outputDistanceRoute
        outputDistanceRoute = Label(canvas,
                    text = "Route Directions",
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Raleway 14 bold')
        outputDistanceRoute.pack(pady = 5) 

        global outputDistance
        outputDistance = Label(canvas,
                    text = printdistance,
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Raleway 12 italic')
        outputDistance.pack(pady = 5) 


        global line2
        line2 = Canvas(canvas, width=1700, height=3)
        line2.create_rectangle(0, 0, 1700, 3, fill="white", outline = 'white')
        line2.pack()

        global outputStatus
        outputStatus = Label(canvas,
                    text = "API Status: " + str(json_status) + " = A successful route call.",
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Raleway 12')
        outputStatus.pack(pady = 5) 

        global line3
        line3 = Canvas(canvas, width=1700, height=3)
        line3.create_rectangle(0, 0, 1700, 3, fill="white", outline = 'white')
        line3.pack()

        global outputTrip
        outputTrip = Label(canvas,
                    text = "Directions from " + (orig) + " to " + (dest),
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Raleway 12')
        outputTrip.pack(pady = 5) 

        Duration = "Trip Duration: " + (json_data["route"]["formattedTime"])
        Kilometers = "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61))
        Fuel = "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))

        global outputDuration
        outputDuration = Label(canvas,
                    text = Duration + "\n" + Kilometers + "\n" +Fuel,
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Raleway 12')
        outputDuration.pack(pady = 5) 

        Tunnel = 'Tunnel: ' + str(json_data["route"]["hasTunnel"])
        Highway = 'Highway: ' + str(json_data["route"]["hasHighway"])

        global outputRoute
        outputRoute = Label(canvas,
                    text = Tunnel + "\n" + Highway,
                    bg = '#bb6c5d',
                    fg = 'white',
                    font = 'Raleway 12')
        outputRoute.pack(pady = 5) 
    
    elif json_status == 402:
        messagebox.showerror("Error","Status Code: " + str(json_status) + "\n Invalid user inputs for one or both locations.")
    
    elif json_status == 611:
        messagebox.showerror("Error","Status Code: " + str(json_status) + "\n Missing an entry for one or both locations.")

    else:
        messagebox.showerror("Error","For Status Code: " + str(json_status) + "\n Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes")

def openMap():
    webbrowser.open(finmap1 + orig + ' ' + dest + finmap2)

        
#submit button
submitBtn = Button(middleframe3,
            text = "SUBMIT",
            width = 20,
            activebackground = '#741519',
            activeforeground = 'white',
            font = 'Raleway',
            command = outputData)
submitBtn.pack(side = LEFT, padx = 5)

#reset button
clearBtn = Button(
                  middleframe3,
                  text = 'RESET',
                  width = 20,
                  activebackground = '#741519',
                  activeforeground = 'white',
                  font = 'Raleway',
                  command=clearData)
clearBtn.pack(side = LEFT, padx = 5)

#map button
openMapBtn = Button(
                  middleframe3,
                  text = 'MAP',
                  width = 20,
                  activebackground = '#741519',
                  activeforeground = 'white',
                  font = 'Raleway',
                  command=openMap)
openMapBtn.pack(padx = 5)


canvas.mainloop()
