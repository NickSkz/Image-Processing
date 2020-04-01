from eMedia import *

from tkinter import *

class PNG_GUI:

    HEIGHT = 500
    WIDTH = 600

    reader = ChunkReader()

    def __init__(self, master):
        canvas = Canvas(master, height=self.HEIGHT, width=self.WIDTH)
        canvas.pack()


        displayFrame = Frame(master)
        displayFrame.place(relx=0.5, rely=0.2, relheight=0.8, relwidth=0.5)

        self.textVar = StringVar()
        self.displayLabel=Label(displayFrame, textvariable=self.textVar, bg='white')
        self.displayLabel.pack(side='top', fill='both', expand='true')

        self.textVar.set("Hey Bitch!")



        frame = Frame(master)
        frame.place(relx=0, rely=0.2, relheight=0.8, relwidth=0.5)

        self.displayImage = Button(frame, text="Display Image", command=lambda: self.printImage())
        self.displayImage.pack(side='top', fill='both', expand='true')

        self.displayCriticalButton = Button(frame, text="Display info from Critical Chunks", command=lambda: self.printCritical())
        self.displayCriticalButton.pack(side='top', fill='both', expand='true')

        self.displayAncillaryButton = Button(frame, text="Display info from Ancillary Chunks (iTEXT, eXIF, SMTH)", command=lambda: self.printAncillary())
        self.displayAncillaryButton.pack(side='top', fill='both', expand='true')

        self.fourierButton = Button(frame, text="Perform Fourier transform of the image", command=lambda: self.performFourier())
        self.fourierButton.pack(side='top', fill='both', expand='true')

        self.inverseFourierButton = Button(frame, text="Perform inverse fourier transform of an image", command=self.printMessage)
        self.inverseFourierButton.pack(side='top', fill='both', expand='true')

        self.annonimizationButton = Button(frame, text="Annonimize Image (creates new image)", command=self.printMessage)
        self.annonimizationButton.pack(side='top', fill='both', expand='true')


        
        entryFrame = Frame(master)
        entryFrame.place(relx=0, rely=0, relheight=0.2, relwidth=1)

        self.welcomeLabel = Label(entryFrame, bg='gray', text='Enter PNG Image name below!', font=70)
        self.welcomeLabel.pack(side='top', fill='both', expand='true')

        self.entry = Entry(entryFrame, font=2, bg='yellow')
        self.entry.pack(side='left', fill='x', expand='true')

        self.findImageButton = Button(entryFrame, text="Analyze Image!", command=lambda: self.startProcessing(self.entry.get()))
        self.findImageButton.pack(side='left', fill='x', expand='true')



    def printMessage(self):
        self.textVar.set("This is it Bitch!")


    def startProcessing(self, name):
        try:
            self.reader.readPNG(name)
        except FileNotFoundError:
            print('Given file doesnt exist!')


    def printImage(self):
        try:
            self.reader.printImg()
        except FileNotFoundError:
            print("File not found!")


    def printCritical(self):
        self.textVar.set(str(self.reader.headInfo) + str(self.reader.palleteInfo))


    def printAncillary(self):
        self.textVar.set(str(self.reader.textInfo))

    def performFourier(self):
        self.reader.performFourier()


root = Tk()
b = PNG_GUI(root)
root.mainloop()
