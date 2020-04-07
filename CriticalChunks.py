class HeaderChunk:
    width = None
    height = None
    bitDepth = None
    colorType = None
    compressionMethod = None
    filterMethod = None
    interlaceMethod = None

    def readChunk(self, f, datalen):
        self.width = int.from_bytes(f.read(4), byteorder='big')
        self.height = int.from_bytes(f.read(4), byteorder='big')
        self.bitDepth = int.from_bytes(f.read(1), byteorder='big') 
        self.colorType = int.from_bytes(f.read(1), byteorder='big') 
        self.compressionMethod = int.from_bytes(f.read(1), byteorder='big') 
        self.filterMethod = int.from_bytes(f.read(1), byteorder='big') 
        self.interlaceMethod = int.from_bytes(f.read(1), byteorder='big')
        f.read(4)  

    def switchColorType(self, num):
        switcher = {
            0: "Grayscale",
            2: "TrueColor",
            3: "Indexed",
            4: "Grayscale + Alpha",
            6: "Truecolor + Alpha",
        }
        return switcher.get(num, "Unknown value.")

    def switchInterlaceMethod(self, num):
        switcher = {
            0: "No interlace",
            1: "Adam7 interlace",
        }
        return switcher.get(num, "Unknown value.")

    def __str__(self):
        return ("Width: " + str(self.width) + " -----> " + "Width: " + str(self.width) + "px" + "\n"
                "Height: " + str(self.height) + " -----> " + "Height: " + str(self.height) + "px" + "\n"
                "Bit Depth: " + str(self.bitDepth) + " -----> " + "Number of bits per sample: " + str(self.bitDepth) + "\n"
                "Color Type: " + str(self.colorType) + " -----> " + "Color type of the image: " + self.switchColorType(self.colorType) + "\n"
                "Compression Method: " + str(self.compressionMethod) + " -----> " + "Deflate/inflate compression with a 32K sliding window" + "\n"
                "Filter Method: " + str(self.filterMethod) + " -----> " + "Filter method used: " + "Adaptive filtering with five basic filter types" + "\n"
                "Interlace Method: " + str(self.interlaceMethod) + " -----> " + "Interlace method used: " + self.switchInterlaceMethod(self.interlaceMethod) + "\n")

    def clear(self):
        self.width = None
        self.height = None
        self.bitDepth = None
        self.colorType = None
        self.compressionMethod = None
        self.filterMethod = None
        self.interlaceMethod = None        

class PaletteChunk:
    numberColors = None

    def readChunk(self, f, datalen):
        if datalen % 3 == 0:
            self.numberColors = datalen // 3
            f.read(datalen + 4)
        else:
            raise Exception("Erarror: number of bytes not divisible by 3.")

    def __str__(self):
        return "Number of colors in palette: " + str(self.numberColors) + "\n"

    def clear(self):
        self.numberColors = None
        