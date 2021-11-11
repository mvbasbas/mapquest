import tkinter 
from tkinter import *
from tkinter import ttk
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
root = Tk()
root.title("Devnet Project")

#added background color #bb6c5d
root.config(background = "#fff5f3")

#window resolution/size
root.geometry('1950x1100')
#Create a main frame
main = Frame (root)
main.pack(fill = BOTH, expand =1)
main.config(background = "#fff5f3")

#Create a canvas
canvas1 = Canvas(main)
canvas1.pack(side=LEFT, fill = BOTH, expand=1)
canvas1.config(background = "#fff5f3")

#add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(main, orient = VERTICAL, command=canvas1.yview)
scrollbar.pack(side=RIGHT, fill=Y)

#configure the canvas
canvas1.configure(yscrollcommand = scrollbar.set)
canvas1.bind('<Configure>', lambda e: canvas1.configure(scrollregion = canvas1.bbox("all")) )

#create another frame inside the canvas 
second_frame = Frame(canvas1)
second_frame.config(background = "#fff5f3")

#add that new frame to a window in the canvas
canvas1.create_window((0,0), window = second_frame, anchor="nw")

#inserting image
path = "pic.png"
mapquest_image = Image.open(path)
mapquest_resizemage = mapquest_image.resize((1900,450)) #1100, 260
mapquest_finimage = ImageTk.PhotoImage(mapquest_resizemage)
mapquest_image_label = tkinter.Label(second_frame , image = mapquest_finimage,)
mapquest_image_label.pack(side = "top", fill = "x", expand = "no")



middleframe1 = Frame(
                    second_frame ,
                    bg = "#fff5f3",
                    )
middleframe1.pack()

middleframe2 = Frame(
                    second_frame ,
                     bg = "#fff5f3",)
middleframe2.pack()

middleframe3 = Frame(
                    second_frame ,
                     bg = "#fff5f3",)
middleframe3.pack()

#input textbox for starting location 
inputLabelLoc= Label(middleframe1,
                  text = 'Enter the Starting Location: ',
                  fg = '#d25525',
                  bg = "#fff5f3",
                  font = 'Raleway 20 bold',
                  padx= 20,
                  pady = 20)
inputLabelLoc.pack(side = LEFT)

textLoc = StringVar()
inputTextLoc = Entry(middleframe1,
                  highlightthickness=2,
                  textvariable = textLoc,
                  bd = 2,
                  bg = "#fff5f3",
                  width = 35,
                  font = 'Raleway 15',
                 )
inputTextLoc.pack(side = LEFT, ipady=9)
inputTextLoc.config(highlightbackground= '#d25525')

#input textbox for destination location 
inputLabelDest= Label(middleframe2,
                  text = 'Enter Desired Destination: ',
                  fg = '#d25525',
                  bg = "#fff5f3",
                  font = 'Raleway 20 bold',
                  padx=20,
                  pady=20)
inputLabelDest.pack(side = LEFT, ipadx=7, pady=8)

textDest = StringVar()
inputTextDest = Entry(middleframe2,
                  highlightthickness=2,
                  textvariable = textDest,
                  bd = 2,
                  bg = "#fff5f3",
                  width = 35,
                  font = 'Raleway 15')
inputTextDest.pack(side = LEFT, ipady=9, pady=9)
inputTextDest.config(highlightbackground= '#d25525')

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
    outputURL = Label(second_frame,
                text= "\n URL: " + url,
                bg = '#fff5f3',
                fg = '#d25525',
                font = 'Raleway 12')
    outputURL.pack(pady = 5)  
    
    global json_status
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    global line1
    line1 = Canvas(second_frame, width=1700, height=3)
    line1.create_rectangle(0, 0, 1700, 3, fill="#d25525", outline = '#d25525')
    line1.pack()

    
    listDist = []
    if json_status == 0:
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            listDist.append((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))

        printdistance = str(listDist).replace("{","").replace("}", "").replace("'", "").replace("[", "").replace("]", "").replace(",", "\n")

        global outputDistanceRoute
        outputDistanceRoute = Label(second_frame,
                    text = "Route Directions",
                    bg = '#fff5f3',
                    fg = '#d25525',
                    font = 'Raleway 14 bold')
        outputDistanceRoute.pack(pady = 5) 

        global outputDistance
        outputDistance = Label(second_frame ,
                    text = printdistance,
                    bg = '#fff5f3',
                    fg = '#d25525',
                    font = 'Raleway 12 italic')
        outputDistance.pack(pady = 5) 


        global line2
        line2 = Canvas(second_frame , width=1700, height=3)
        line2.create_rectangle(0, 0, 1700, 3, fill="#d25525", outline = '#d25525')
        line2.pack()

        global outputStatus
        outputStatus = Label(second_frame,
                    text = "API Status: " + str(json_status) + " = A successful route call.",
                    bg = '#fff5f3',
                    fg = '#d25525',
                    font = 'Raleway 12')
        outputStatus.pack(pady = 5) 

        global line3
        line3 = Canvas(second_frame, width=1700, height=3)
        line3.create_rectangle(0, 0, 1700, 3, fill="#d25525", outline = '#d25525')
        line3.pack()

        global outputTrip
        outputTrip = Label(second_frame ,
                    text = "Directions from " + (orig) + " to " + (dest),
                    bg = '#fff5f3',
                    fg = '#d25525',
                    font = 'Raleway 12')
        outputTrip.pack(pady = 5) 

        Duration = "Trip Duration: " + (json_data["route"]["formattedTime"])
        Kilometers = "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61))
        Fuel = "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))

        global outputDuration
        outputDuration = Label(second_frame ,
                    text = Duration + "\n" + Kilometers + "\n" +Fuel,
                    bg = '#fff5f3',
                    fg = '#d25525',
                    font = 'Raleway 12')
        outputDuration.pack(pady = 5) 

        Tunnel = 'Tunnel: ' + str(json_data["route"]["hasTunnel"])
        Highway = 'Highway: ' + str(json_data["route"]["hasHighway"])

        global outputRoute
        outputRoute = Label(second_frame ,
                    text = Tunnel + "\n" + Highway,
                    bg = '#fff5f3',
                    fg = '#d25525',
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
                highlightthickness=3,
                text = "SUBMIT",
                width = 20,
                height = 2,
                activebackground = '#62bb3c',
                activeforeground = 'white',
                font = 'Raleway 15 bold',
                command = outputData)
submitBtn.pack(side = LEFT, padx = 5)
submitBtn.config(foreground='#62bb3c')
submitBtn.config(highlightbackground= '#62bb3c')
#reset button
clearBtn = Button(middleframe3,
                  highlightthickness=3,
                  text = 'RESET',
                  width = 20,
                  height = 2,
                  activebackground = '#a6a6a6',
                  activeforeground = 'white',
                  font = 'Raleway 15 bold',
                  command = clearData)
clearBtn.pack(side = LEFT, padx = 5)
clearBtn.config(foreground='#a6a6a6')
clearBtn.config(highlightbackground= '#a6a6a6')

#map button
openMapBtn = Button(middleframe3 ,
                    highlightthickness=3,
                    text = 'MAP',
                    width = 20,
                    height = 2,
                    activebackground = '#e28317',
                    activeforeground = 'white',
                    font = 'Raleway 15 bold',
                    command = openMap)
openMapBtn.pack(padx = 5)
openMapBtn.config(foreground='#e28317')
openMapBtn.config(highlightbackground= '#e28317')


root.mainloop()
