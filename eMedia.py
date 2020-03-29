from enum import IntEnum
import png

import AncillaryChunks as AC
import CriticalChunks as CC


def readTillEnd(datalen):
    for _ in range(datalen+4):
        f.read(1)



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

        

name = "aa.png"
f = open(name, "rb")


textInfo = AC.TextMeta()
headInfo = CC.HeaderChunk()
palleteInfo = CC.PaletteChunk()

if int.from_bytes(f.read(8), byteorder='big') == HexTypes.PNG_FILE:

    while True:
        datalen = int.from_bytes(f.read(4), byteorder='big')
        print("Incoming chunk's length: " + str(datalen))
        chunkType = f.read(4)

        if int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IHDR:
            print("IHDR")
            headInfo.readChunk(f, datalen)

        elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PLTE:
            print("IPLTE")
            palleteInfo.readChunk(f, datalen)
            
        elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IDAT:
            print("IDAT")
            readTillEnd(datalen)

        elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_END:
            print("IEND")
            break
        
        elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_EXIF:
            print("EXIF")
            readTillEnd(datalen)

        elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TEXT:
            textInfo.readChunk(f, datalen)

        else:
            readTillEnd(datalen)

        print()
else:
    print("That's not even a PNG file!")
f.close()

print()
print()

print(headInfo)
print(palleteInfo)
print(textInfo)
