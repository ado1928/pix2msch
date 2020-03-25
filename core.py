try:
    import struct, zlib, os, base64, pyperclip
    from PIL import Image
except Exception as e:
    print("You're missing a package!")
    print()
    print(e)
    input()
    
colorarray = [
    217, 157, 115,
    140, 127, 169,
    235, 238, 245,
    178, 198, 210,
    247, 203, 164,
    39, 39, 39,
    141, 161, 227,
    249, 163, 199,
    119, 119, 119,
    83, 86, 92,
    203,217, 127,
    244,186, 110,
    243, 233, 121,
    116, 87, 206,
    255, 121, 94,
    255, 170, 95
    ]

#convert array of ints into a list of tuples, then into a palette
tuple_array = [tuple(colorarray[t*3:t*3+3]) for t in range(len(colorarray)//3)]
palette = Image.new("P", (16, 16))
palette.putpalette(colorarray*16)
palette.load()

def quantize(img, dither, transparency_treshold):
    #invalid input checking
    try:
        img = Image.open(img)
        transparency_treshold = int(transparency_treshold)
    except AttributeError:
        raise Exception("No image selected")
    except ValueError:
        raise Exception("Transparency Treshold must be a number")
    
    if transparency_treshold > 255:
        raise Exception("Transparency Treshold must not exceed 255")
    elif transparency_treshold < 0:
        raise Exception("Transparency Treshold most not be negative")
    
    #sphagetti
    img = img.convert("RGBA") # image 
    imgq = img.convert("RGB") # fully opaque image
    imgq = imgq._new(imgq.im.convert("P", 1 if dither else 0, palette.im)) #where the actual quantization happens

    imgA = Image.new("RGBA", img.size)
    pixels = imgA.load()
    imgq = imgq.convert("RGB")
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if img.getpixel((x, y))[3] >= transparency_treshold: #transparency treshold
                pixels[x, y] = imgq.getpixel((x, y))
            else:
                pixels[x, y] = (0, 0, 0, 0)

    print("Quantization complete")

    return imgA


# imgfile - Path to the image
# name - Name of the schematic
# save_location - Save location, i guess
# dither - Whether to use dithering (True or False, 1 or 0)
# transparency_treshold - Below which alpha level to stop displaying (0-255), where 0 is show everything and 255 is show only fully opaque
# mode - Either "path" or "clipboard". Whether to save the schematic as .msch or to copy it into clipboard

def pix2msch(imgfile               = None,
             name                  = "schematic",
             save_location         = None,
             dither                = True,
             transparency_treshold = 127,
             mode                  = "path"
             ): #sad face
    
    tiles = []
    
    #input checking
    if mode == "path":
        if not(os.path.isdir(os.path.expandvars(save_location))):
            raise Exception("Invalid path")
        
    if name == "":
        raise Exception("Please enter a name")
    
    img = quantize(imgfile, dither, transparency_treshold)
    
    img = img.rotate(-90, expand=True)
    #img = img.rotate(-90, expand=True)
    
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if img.getpixel((x, y))[3] > 1:
                tiles.append((x, y, tuple_array.index(img.getpixel((x, y))[0:3])))

    print("Converted pixels into an array of tiles")

    class ByteBuffer(): #so desparate i had to write my own byte buffer
        def __init__(self, data=bytearray()):
            self.data = data
            
        def writeShort(self, int):
            self.data += struct.pack(">H", int)

        def writeUTF(self, str):
            self.writeShort(len(str))
            self.data += bytes(str.encode("UTF"))
            
        def writeByte(self, int):
            self.data += struct.pack("b", int)
            
        def writeInt(self, int):
            self.data += struct.pack(">i", int)
            
    #write header and all of that stuff
    data = ByteBuffer()

    data.writeShort(width)
    data.writeShort(height)

    data.writeByte(1)

    data.writeUTF("name")
    data.writeUTF(name)

    data.writeByte(1)

    data.writeUTF("sorter")
    data.writeInt(len(tiles))

    print("Header written")

    for tile in tiles: #write tiles
        data.writeByte(0)
        data.writeShort(tile[1])
        data.writeShort(tile[0])
        data.writeInt(tile[2])
        data.writeByte(0)

    print("Tile data written")
    
    
    if mode == "path":
        os.chdir(os.path.expandvars(save_location))
        file = open(name + ".msch", "wb")
        file.write(b"msch\x00"+zlib.compress(data.data))
        file.close()

        print("Successfully saved {0} ".format(name + ".msch"))
        
    else:
        pyperclip.copy(base64.standard_b64encode(b"msch\x00"+zlib.compress(data.data)).decode())
        print("Schematic converted to base64, and put into clipboard")
        
