from enum import IntEnum

from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt

import AncillaryChunks as AC
import CriticalChunks as CC

#Assign hex to the most popular chunks header names
class HexTypes(IntEnum):
    #PNG SIGNATURE CONSTANT
    PNG_FILE = 0x89504E470D0A1A0A

    #PNG CHUNK TYPES CONSTANTS (4 CHARACTERS, CODED IN HEX EG. IHDR -> 0x49484452)
    PNG_IHDR = 0x49484452
    PNG_PLTE = 0x504C5445
    PNG_IDAT = 0x49444154
    PNG_IEND = 0x49454E44
    
    PNG_TEXT = 0x74455874
    PNG_EXIF = 0x65584966
    PNG_TRNS = 0x74524E53
    PNG_GAMA = 0x67414D41
    PNG_CHRM = 0x6348524D
    PNG_SRGB = 0x73524742
    PNG_ICCP = 0x69434350
    PNG_ZTXT = 0x7A545874
    PNG_ITXT = 0x69545874
    PNG_BKGD = 0x624B4744
    PNG_PHYS = 0x70485973
    PNG_SBIT = 0x73424954
    PNG_SPLT = 0x73504C54
    PNG_HIST = 0x68495354
    PNG_TIME = 0x74494D45

        
class ChunkReader:
    #name of the file
    name = ""
    #3 objects connected to critical chunks
    headInfo = CC.HeaderChunk()
    palleteInfo = CC.PaletteChunk()
    dataInfo = CC.DataChunk()
    #3 objects connected to ancillary chunks
    textInfo = AC.TextMeta()
    ztextInfo = AC.ZTextMeta()
    itextInfo = AC.ITextMeta()

    #read image - most important function
    def readPNG(self, name):
        # assign name of the file, file handler, as well read this with cv2
        self.name = name
        self.f = open(self.name, "rb")
        self.img = cv2.imread(self.name)

        #clear all the garbage
        self.headInfo.clear()
        self.palleteInfo.clear()
        self.dataInfo.clear()

        self.textInfo.clear()
        self.ztextInfo.clear()
        self.itextInfo.clear()

        #check if png
        if int.from_bytes(self.f.read(8), byteorder='big') == HexTypes.PNG_FILE:
            #until IEND occurs
            while True:
                #get chunk length
                datalen = int.from_bytes(self.f.read(4), byteorder='big')
                print("Incoming chunk's length: " + str(datalen))
                #get chunk type
                chunkType = self.f.read(4)

# Critical Chunks

                #check what chunk, peform appropriate action defined in certain chunk class
                if int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IHDR:
                    print("Incoming chunk's name: IHDR")
                    self.headInfo.readChunk(self.f, datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PLTE:
                    print("Incoming chunk's name: PLTE")
                    self.palleteInfo.readChunk(self.f, datalen)
                    
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IDAT:
                    print("Incoming chunk's name: IDAT")
                    self.dataInfo.readChunk(self.f, datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IEND:
                    print("Incoming chunk's name: IEND")
                    self.readTillEnd(datalen)
                    break
                
# Ancillary Chunks

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_EXIF:
                    print("Incoming chunk's name: eXIf")
                    self.readTillEnd(datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TEXT:
                    print("Incoming chunk's name: tEXt")
                    self.textInfo.readChunk(self.f, datalen)
                    
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TRNS:
                    print("Incoming chunk's name: tRNS")
                    self.readTillEnd(datalen)
                
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_GAMA:
                    print("Incoming chunk's name: gAMA")
                    self.readTillEnd(datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_CHRM:
                    print("Incoming chunk's name: cHRM")
                    self.readTillEnd(datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_SRGB:
                    print("Incoming chunk's name: sRGB")
                    self.readTillEnd(datalen)   

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_ICCP:
                    print("Incoming chunk's name: iCCP")
                    self.readTillEnd(datalen)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_ZTXT:
                    print("Incoming chunk's name: zTXt")
                    self.ztextInfo.readChunk(self.f, datalen) 

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_ITXT:
                    print("Incoming chunk's name: iTXt")
                    self.itextInfo.readChunk(self.f, datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_BKGD:
                    print("Incoming chunk's name: bkGD")
                    self.readTillEnd(datalen)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PHYS:
                    print("Incoming chunk's name: pHYs")
                    self.readTillEnd(datalen)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_SBIT:
                    print("Incoming chunk's name: sBIT")
                    self.readTillEnd(datalen)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_SPLT:
                    print("Incoming chunk's name: sPLT")
                    self.readTillEnd(datalen)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_HIST:
                    print("Incoming chunk's name: hIST")
                    self.readTillEnd(datalen)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TIME:
                    print("Incoming chunk's name: tIME")
                    self.readTillEnd(datalen)  

                else:
                    self.readTillEnd(datalen)

                print()
        else:
            print("That's not even a PNG file!")
        self.f.close()


    #read all whats left to go to next chunk
    def readTillEnd(self, datalen):
        for _ in range(datalen+4):
            self.f.read(1)

    #print it with cv2
    def printImg(self):
        cv2.imshow('Analyzed Image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #perform fourier - mag and phase
    def performFourier(self):
        #to gray
        grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        self.grayImg = grayImg

        #give freq transform and shift (cuz zero freq is in the cornern - we want it in the middle)
        f = np.fft.fft2(grayImg)
        fshift = np.fft.fftshift(f)

        self.fshift = fshift

        #give magnitude and phase
        mag, ang = cv2.cartToPolar(fshift.real, fshift.imag)

        self.mag = mag
        self.ang = ang

        #display it
        plt.subplot(221), plt.imshow(grayImg, cmap='gray')
        plt.title('Original Grayscale Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(223), plt.imshow(20*np.log(np.abs(mag)), cmap='gray')
        plt.title('Magnitude of Fourier Transform'), plt.xticks([]), plt.yticks([])
        plt.subplot(224), plt.imshow(20*np.log(ang), cmap='gray')
        plt.title('Phase of Fourier Transform'), plt.xticks([]), plt.yticks([])
        plt.show()


    #annonymize image
    def createAnnonymousImg(self):
        #open folder ares/
        fwrite = open("a" + self.name, "wb+")
        f = open (self.name, "rb")

        #write png sig
        fwrite.write(f.read(8))

        #while IEND
        while(True):
                #write datalen, chunktype 
                datalenBytes = f.read(4)
                datalen = int.from_bytes(datalenBytes, byteorder='big')

                chunkTypeBytes = f.read(4)
                chunkType = chunkTypeBytes

# Critical Chunks

                #only if critical write it to the file - len, name, whats inside
                if int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IHDR:
                    print("Incoming chunk's name: IHDR")
                    fwrite.write(datalenBytes)
                    fwrite.write(chunkTypeBytes)
                    fwrite.write(f.read(datalen+4))

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PLTE:
                    print("Incoming chunk's name: PLTE")
                    fwrite.write(datalenBytes)
                    fwrite.write(chunkTypeBytes)
                    fwrite.write(f.read(datalen+4))
                    
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IDAT:
                    print("Incoming chunk's name: IDAT")
                    fwrite.write(datalenBytes)
                    fwrite.write(chunkTypeBytes)
                    fwrite.write(f.read(datalen+4))

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IEND:
                    print("Incoming chunk's name: IEND")
                    fwrite.write(datalenBytes)
                    fwrite.write(chunkTypeBytes)
                    fwrite.write(f.read(datalen+4))
                    break
                else:
                    #read all whats not critical
                    f.read(datalen + 4)

        fwrite.close()
        f.close()                    
