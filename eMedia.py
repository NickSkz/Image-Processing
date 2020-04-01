from enum import IntEnum

from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt

import AncillaryChunks as AC
import CriticalChunks as CC


class HexTypes(IntEnum):
    #PNG SIGNATURE CONSTANT
    PNG_FILE = 0x89504E470D0A1A0A

    #PNG CHUNK TYPES CONSTANTS (4 CHARACTERS, CODED IN HEX EG. IHDR -> 0x49484452)
    PNG_IHDR = 0x49484452
    PNG_PLTE = 0x504C5445
    PNG_IDAT = 0x49444154
    PNG_END = 0x49454E44
    
    PNG_TEXT = 0x74455874
    PNG_EXIF = 0x65584966

        
class ChunkReader:

    name = ""

    headInfo = CC.HeaderChunk()
    palleteInfo = CC.PaletteChunk()

    textInfo = AC.TextMeta()


    def readPNG(self, name):

        self.name = name
        self.f = open(self.name, "rb")
        self.img = cv2.imread(self.name)

        self.headInfo.clear()
        self.palleteInfo.clear()

        self.textInfo.clear()

        if int.from_bytes(self.f.read(8), byteorder='big') == HexTypes.PNG_FILE:

            while True:
                datalen = int.from_bytes(self.f.read(4), byteorder='big')
                print("Incoming chunk's length: " + str(datalen))
                chunkType = self.f.read(4)

                if int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IHDR:
                    print("IHDR")
                    self.headInfo.readChunk(self.f, datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PLTE:
                    print("IPLTE")
                    self.palleteInfo.readChunk(self.f, datalen)
                    
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IDAT:
                    print("IDAT")
                    self.readTillEnd(datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_END:
                    print("IEND")
                    break
                
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_EXIF:
                    print("EXIF")
                    self.readTillEnd(datalen)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TEXT:
                    self.textInfo.readChunk(self.f, datalen)

                else:
                    self.readTillEnd(datalen)

                print()
        else:
            print("That's not even a PNG file!")
        self.f.close()


    def readTillEnd(self, datalen):
        for _ in range(datalen+4):
            self.f.read(1)

    
    def printImg(self):
        cv2.imshow('Analyzed Image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def performFourier(self):
        grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        f = np.fft.fft2(grayImg)
        fshift = np.fft.fftshift(f)

        mag, ang = cv2.cartToPolar(fshift.real, fshift.imag)
        mag = 20*np.log(np.abs(mag))
        ang = 20*np.log(np.abs(ang))

        plt.subplot(121), plt.imshow(mag, cmap='gray')
        plt.title('Magnitude of Fourier Transform'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(ang, cmap='gray')
        plt.title('Phase of Fourier Transform'), plt.xticks([]), plt.yticks([])
        plt.show()
        