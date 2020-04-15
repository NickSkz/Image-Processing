import zlib

#tEXt
class TextMeta:
    #map of keys-values
    infos = {}
    
    def readChunk(self, f, datalen):
        metaType = ""

        character = f.read(1)
        extrabytes = 1

        #get what type of message
        while int.from_bytes(character, byteorder='big') != 0x00:
            metaType += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        what = ""
        #get what is tha message
        for _ in range (datalen - extrabytes):
            what += f.read(1).decode('latin-1')

        f.read(4)
        #update map
        self.infos.update({metaType : what})


    #show in nice form
    def __str__(self):
        niceDisplayableInfo = ""
        for(key, value) in self.infos.items():
            niceDisplayableInfo += key + " :: " + value + "\n"

        return niceDisplayableInfo

    def clear(self):
        self.infos.clear()
        

#zTXt - similar to tEXt but compressed value
class ZTextMeta:
    #map with info
    infos = {}
    
    def readChunk(self, f, datalen):
        metaType = ""

        character = f.read(1)
        extrabytes = 1
        #check key
        while int.from_bytes(character, byteorder='big') != 0x00:
            metaType += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        what = ""

        f.read(1)
        #extrabytes cuz, we want to finish at last byte
        extrabytes += 1

        #decompress with zlib what inside and add it as value
        what = zlib.decompress(f.read(datalen-extrabytes)).decode('latin-1')
        #update it
        self.infos.update({metaType : what})

        f.read(4)

    #show in nice form
    def __str__(self):
        niceDisplayableInfo = ""
        for(key, value) in self.infos.items():
            niceDisplayableInfo += key + " :: " + value + "\n"

        return niceDisplayableInfo

    def clear(self):
        self.infos.clear()
        

#iTXt - similar to above - but coded in Unicode + compression + multilanguage 
class ITextMeta:
    infos = {}
    
    def readChunk(self, f, datalen):
        metaType = ""

        character = f.read(1)
        extrabytes = 1

        #read what
        while int.from_bytes(character, byteorder='big') != 0x00:
            metaType += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        what = ""

        #is it compressed?
        compressionFlag = int.from_bytes(f.read(1), byteorder='big')
        extrabytes += 1

        f.read(1)
        extrabytes += 1

        languageTag = ""
        character = f.read(1)
        extrabytes += 1
        
        #check what language message is coded in
        while int.from_bytes(character, byteorder='big') != 0x00:
            languageTag += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        translatedTag = ""
        character = f.read(1)
        extrabytes += 1
        #check whats the translated value of the key
        while int.from_bytes(character, byteorder='big') != 0x00:
            translatedTag += chr(int.from_bytes(character, byteorder='big'))
            character = f.read(1)
            extrabytes += 1

        #according to existing compression decode message
        if compressionFlag == 1:
            what = zlib.decompress(f.read(datalen-extrabytes)).decode('utf-8')
        if compressionFlag == 0:
            what = f.read(datalen-extrabytes).decode('utf-8')

        #concatenate it and to the map
        keyWord = metaType + " (" + languageTag + ", " + translatedTag + ")"

        self.infos.update({keyWord : what})

        f.read(4)


    #show in nice form
    def __str__(self):
        niceDisplayableInfo = ""
        for(key, value) in self.infos.items():
            niceDisplayableInfo += key + " :: " + value + "\n"

        return niceDisplayableInfo

    def clear(self):
        self.infos.clear()
        