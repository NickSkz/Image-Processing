import zlib

class TextMeta:
    infos = {}
    
    def readChunk(self, f, datalen):
        metaType = ""

        character = f.read(1)
        extrabytes = 1

        while int.from_bytes(character, byteorder='big') != 0x00:
            metaType += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        what = ""

        for _ in range (datalen - extrabytes):
            what += f.read(1).decode('latin-1')

        f.read(4)

        self.infos.update({metaType : what})



    def __str__(self):
        niceDisplayableInfo = ""
        for(key, value) in self.infos.items():
            niceDisplayableInfo += key + " :: " + value + "\n"

        return niceDisplayableInfo

    def clear(self):
        self.infos.clear()
        


class ZTextMeta:
    infos = {}
    
    def readChunk(self, f, datalen):
        metaType = ""

        character = f.read(1)
        extrabytes = 1

        while int.from_bytes(character, byteorder='big') != 0x00:
            metaType += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        what = ""

        f.read(1)
        extrabytes += 1

        what = zlib.decompress(f.read(datalen-extrabytes)).decode('latin-1')

        self.infos.update({metaType : what})

        f.read(4)


    def __str__(self):
        niceDisplayableInfo = ""
        for(key, value) in self.infos.items():
            niceDisplayableInfo += key + " :: " + value + "\n"

        return niceDisplayableInfo

    def clear(self):
        self.infos.clear()
        

class ITextMeta:
    infos = {}
    
    def readChunk(self, f, datalen):
        metaType = ""

        character = f.read(1)
        extrabytes = 1

        while int.from_bytes(character, byteorder='big') != 0x00:
            metaType += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        what = ""

        compressionFlag = int.from_bytes(f.read(1), byteorder='big')
        extrabytes += 1

        f.read(1)
        extrabytes += 1

        languageTag = ""
        character = f.read(1)
        extrabytes += 1
        while int.from_bytes(character, byteorder='big') != 0x00:
            languageTag += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        translatedTag = ""
        character = f.read(1)
        extrabytes += 1
        while int.from_bytes(character, byteorder='big') != 0x00:
            translatedTag += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        if compressionFlag == 1:
            what = zlib.decompress(f.read(datalen-extrabytes)).decode('utf-8')
        if compressionFlag == 0:
            what = f.read(datalen-extrabytes).decode('utf-8')

        keyWord = metaType + " (" + languageTag + ", " + translatedTag + ")"

        self.infos.update({keyWord : what})

        f.read(4)


    def __str__(self):
        niceDisplayableInfo = ""
        for(key, value) in self.infos.items():
            niceDisplayableInfo += key + " :: " + value + "\n"

        return niceDisplayableInfo

    def clear(self):
        self.infos.clear()
        