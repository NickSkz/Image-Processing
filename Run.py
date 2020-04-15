from eMedia import *

from tkinter import *

class PNG_GUI:
    #Parameters of the window
    HEIGHT = 500
    WIDTH = 950
    #Initialize the Herz of the programm
    reader = ChunkReader()

    #Initialize Tkinter window, another buttons, stuff like that
    def __init__(self, master):
        canvas = Canvas(master, height=self.HEIGHT, width=self.WIDTH)
        canvas.pack()


        displayFrame = Frame(master)
        displayFrame.place(relx=0.5, rely=0.2, relheight=0.8, relwidth=0.5)

        self.textVar = StringVar()
        self.displayLabel=Label(displayFrame, textvariable=self.textVar, bg='white')
        self.displayLabel.pack(side='top', fill='both', expand='true')

        self.textVar.set("Hey!")



        frame = Frame(master)
        frame.place(relx=0, rely=0.2, relheight=0.8, relwidth=0.5)


        #Main buttons - assign functions as lambda to buttons
        self.displayImage = Button(frame, text="Display Image", command=lambda: self.printImage())
        self.displayImage.pack(side='top', fill='both', expand='true')

        self.displayCriticalButton = Button(frame, text="Display info from Critical Chunks", command=lambda: self.printCritical())
        self.displayCriticalButton.pack(side='top', fill='both', expand='true')

        self.BufferFrame = Frame(frame)
        self.BufferFrame.pack(side='top', fill='both', expand='true')

        self.displayAncillaryButton = Button(self.BufferFrame, text="Display info from Ancillary Chunks (tEXt, zTXt, iTXt)", command=lambda: self.printAncillary())
        self.displayAncillaryButton.pack(side='left', fill='both', expand='true')

        self.displayPalette = Button(self.BufferFrame, text="Display Palette (Indexed Images)", command=lambda: self.printPalette())
        self.displayPalette.pack(side='right', fill='both', expand='true')

        self.fourierButton = Button(frame, text="Perform Fourier transform of the image", command=lambda: self.performFourier())
        self.fourierButton.pack(side='top', fill='both', expand='true')

        self.annonimizationButton = Button(frame, text="Annonimize Image (creates new image)", command=lambda: self.performAnnonization())
        self.annonimizationButton.pack(side='top', fill='both', expand='true')


        #Collect user input, output to the window
        entryFrame = Frame(master)
        entryFrame.place(relx=0, rely=0, relheight=0.2, relwidth=1)

        self.welcomeLabel = Label(entryFrame, bg='gray', text='Enter PNG Image name below!', font=70)
        self.welcomeLabel.pack(side='top', fill='both', expand='true')

        self.entry = Entry(entryFrame, font=2, bg='yellow')
        self.entry.pack(side='left', fill='x', expand='true')

        self.findImageButton = Button(entryFrame, text="Analyze Image!", command=lambda: self.startProcessing(self.entry.get()))
        self.findImageButton.pack(side='left', fill='x', expand='true')


    #-_______________________________________________________-
    def printMessage(self):
        self.textVar.set("-_______-")

    #read the file, collect chunks info
    def startProcessing(self, name):
        try:
            self.reader.readPNG(name)
        except FileNotFoundError:
            print('Given file doesnt exist!')

    #print image with open cv
    def printImage(self):
        try:
            self.reader.printImg()
        except FileNotFoundError:
            print("File not found!")

    #show pallete if indexed img with matplotlib
    def printPalette(self):
        if self.reader.palleteInfo.numberColors != None:
            self.reader.palleteInfo.showPalette()

    #print info bout critical chunks
    def printCritical(self):
        self.textVar.set("*******************************************IHDR*******************************************\n" +
        str(self.reader.headInfo) +
        "\n*******************************************PLTE*******************************************\n" +
        str(self.reader.palleteInfo) +
        "\n******************************************IDAT*******************************************\n" +
        str(self.reader.dataInfo)) 

    #print info bout ancillary
    def printAncillary(self):
        self.textVar.set("*******************************************tEXt*******************************************\n" +
        str(self.reader.textInfo) +
        "\n*******************************************zTXt*******************************************\n" +
        str(self.reader.ztextInfo) +
        "\n*******************************************iTXt*******************************************\n" +
        str(self.reader.itextInfo))
    
    #perform fourier
    def performFourier(self):
        self.reader.performFourier()


    #delete not necessary chunks
    def performAnnonization(self):
        self.reader.createAnnonymousImg()

#go with it 
root = Tk()
b = PNG_GUI(root)
root.mainloop()
