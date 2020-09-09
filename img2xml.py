from PIL import Image
from PIL import ImageColor
import numpy as np
import sys
import os
import csv
import lxml.etree
import lxml.builder
import difflib
from scipy import spatial
import random
from bisect import bisect_left
avorion_colors = [ "ff000080", "ff00008b", "ff0000cd", "ff0000ee", "ff0000ff", "ff006400", "ff00688b", "ff00868b", "ff008b00", "ff008b45", "ff008b8b", "ff009acd", "ff00b2ee", "ff00bfff", "ff00c5cd", "ff00cd00", "ff00cd66", "ff00cdcd", "ff00ced1", "ff00e5ee", "ff00ee00", "ff00ee76", "ff00eeee", "ff00f5ff", "ff00fa9a", "ff00ff00", "ff00ff7f", "ff00ffff", "ff104e8b", "ff141414", "ff1874cd", "ff191970", "ff1c86ee", "ff1e1e1e", "ff1e90ff", "ff20b2aa", "ff228b22", "ff27408b", "ff2e8b57", "ff2f4f4f", "ff32cd32", "ff36648b", "ff366cb3", "ff36b336", "ff3a5fcd", "ff3cb371", "ff40e0d0", "ff4169e1", "ff436eee", "ff43cd80", "ff458b00", "ff458b74", "ff464646", "ff4682b4", "ff473c8b", "ff483d8b", "ff4876ff", "ff48d1cc", "ff4a708b", "ff4d99ff", "ff4dff4d", "ff4eee94", "ff4f94cd", "ff528b8b", "ff53868b", "ff548b54", "ff54ff9f", "ff551a8b", "ff556b2f", "ff5cacee", "ff5d478b", "ff5f9ea0", "ff607b8b", "ff63b8ff", "ff6495ed", "ff668b8b", "ff66cd00", "ff66cdaa", "ff68228b", "ff68838b", "ff6959cd", "ff696969", "ff698b22", "ff698b69", "ff6a5acd", "ff6b8e23", "ff6c7b8b", "ff6ca6cd", "ff6e7b8b", "ff6e8b3d", "ff708090", "ff76ee00", "ff76eec6", "ff778899", "ff79cdcd", "ff7a378b", "ff7a67ee", "ff7a8b8b", "ff7ac5cd", "ff7b68ee", "ff7ccd7c", "ff7cfc00", "ff7d26cd", "ff7ec0ee", "ff7fff00", "ff7fffd4", "ff836fff", "ff838b83", "ff838b8b", "ff8470ff", "ff87ceeb", "ff87cefa", "ff87ceff", "ff8968cd", "ff8a2be2", "ff8b0000", "ff8b008b", "ff8b0a50", "ff8b1a1a", "ff8b1c62", "ff8b2252", "ff8b2323", "ff8b2500", "ff8b3626", "ff8b3a3a", "ff8b3a62", "ff8b3e2f", "ff8b4500", "ff8b4513", "ff8b4726", "ff8b475d", "ff8b4789", "ff8b4c39", "ff8b5742", "ff8b5a00", "ff8b5a2b", "ff8b5f65", "ff8b636c", "ff8b6508", "ff8b668b", "ff8b6914", "ff8b6969", "ff8b7355", "ff8b7500", "ff8b7765", "ff8b795e", "ff8b7b8b", "ff8b7d6b", "ff8b7d7b", "ff8b7e66", "ff8b814c", "ff8b8378", "ff8b8386", "ff8b864e", "ff8b8682", "ff8b8878", "ff8b8970", "ff8b8989", "ff8b8b00", "ff8b8b7a", "ff8b8b83", "ff8db6cd", "ff8deeee", "ff8ee5ee", "ff8fbc8f", "ff90ee90", "ff912cee", "ff9370db", "ff9400d3", "ff96cdcd", "ff97ffff", "ff98f5ff", "ff98fb98", "ff9932cc", "ff9a32cd", "ff9ac0cd", "ff9acd32", "ff9aff9a", "ff9b30ff", "ff9bcd9b", "ff9f79ee", "ff9fb6cd", "ffa020f0", "ffa0522d", "ffa2b5cd", "ffa2cd5a", "ffa3afbf", "ffa3bfa3", "ffa4d3ee", "ffa52a2a", "ffaaaaaa", "ffab82ff", "ffadd8e6", "ffadff2f", "ffae1a1a", "ffaeeeee", "ffafeeee", "ffb03060", "ffb0c4de", "ffb0e0e6", "ffb0e2ff", "ffb22222", "ffb23aee", "ffb2dfee", "ffb35824", "ffb37d5a", "ffb3b336", "ffb3b3b3", "ffb3ee3a", "ffb452cd", "ffb4cdcd", "ffb4eeb4", "ffb8860b", "ffb9d3ee", "ffba55d3", "ffbbffff", "ffbc8f8f", "ffbc9f9f", "ffbcd2ee", "ffbcee68", "ffbdb76b", "ffbf3eff", "ffbfada3", "ffbfaea3", "ffbfbfa3", "ffbfefff", "ffc0ff3e", "ffc1cdc1", "ffc1cdcd", "ffc1ffc1", "ffc6e2ff", "ffc71585", "ffcae1ff", "ffcaff70", "ffcd0000", "ffcd00cd", "ffcd1076", "ffcd2626", "ffcd2990", "ffcd3278", "ffcd3333", "ffcd3700", "ffcd4f39", "ffcd5555", "ffcd5b45", "ffcd5c5c", "ffcd6090", "ffcd6600", "ffcd661d", "ffcd6839", "ffcd6889", "ffcd69c9", "ffcd7054", "ffcd8162", "ffcd8500", "ffcd853f", "ffcd8c95", "ffcd919e", "ffcd950c", "ffcd96cd", "ffcd9b1d", "ffcd9b9b", "ffcdaa7d", "ffcdad00", "ffcdaf95", "ffcdb38b", "ffcdb5cd", "ffcdb79e", "ffcdb7b5", "ffcdba96", "ffcdbe70", "ffcdc0b0", "ffcdc1c5", "ffcdc5bf", "ffcdc673", "ffcdc8b1", "ffcdc9a5", "ffcdc9c9", "ffcdcd00", "ffcdcdb4", "ffcdcdc1", "ffd02090", "ffd15fee", "ffd1eeee", "ffd2691e", "ffd2b48c", "ffd3d3d3", "ffd70751", "ffd8bfd8", "ffda70d6", "ffdaa520", "ffdb7093", "ffdcdcdc", "ffdda0dd", "ffdeb887", "ffe066ff", "ffe0eee0", "ffe0eeee", "ffe0ffff", "ffe6e6fa", "ffe9967a", "ffee0000", "ffee00ee", "ffee1289", "ffee2c2c", "ffee30a7", "ffee3a8c", "ffee3b3b", "ffee4000", "ffee5c42", "ffee6363", "ffee6a50", "ffee6aa7", "ffee7600", "ffee7621", "ffee7942", "ffee799f", "ffee7ae9", "ffee8262", "ffee82ee", "ffee9572", "ffee9a00", "ffee9a49", "ffeea2ad", "ffeea9b8", "ffeead0e", "ffeeaeee", "ffeeb422", "ffeeb4b4", "ffeec591", "ffeec900", "ffeecbad", "ffeecfa1", "ffeed2ee", "ffeed5b7", "ffeed5d2", "ffeed8ae", "ffeedc82", "ffeedd82", "ffeedfcc", "ffeee0e5", "ffeee5de", "ffeee685", "ffeee8aa", "ffeee8cd", "ffeee9bf", "ffeee9e9", "ffeeee00", "ffeeeed1", "ffeeeee0", "fff08080", "fff0e68c", "fff0f8ff", "fff0fff0", "fff0ffff", "fff4a460", "fff5deb3", "fff5f5dc", "fff5f5f5", "fff5fffa", "fff8f8ff", "fffa2626", "fffa8072", "fffaebd7", "fffaf0e6", "fffafad2", "fffdf5e6", "ffff0000", "ffff00ff", "ffff1493", "ffff3030", "ffff34b3", "ffff3e96", "ffff4040", "ffff4500", "ffff6347", "ffff69b4", "ffff6a6a", "ffff6eb4", "ffff7256", "ffff7f00", "ffff7f24", "ffff7f50", "ffff8033", "ffff8247", "ffff82ab", "ffff83fa", "ffff8c00", "ffff8c69", "ffffa07a", "ffffa500", "ffffa54f", "ffffaeb9", "ffffb380", "ffffb5c5", "ffffb6c1", "ffffb90f", "ffffbbff", "ffffc0cb", "ffffc125", "ffffc1c1", "ffffd39b", "ffffd700", "ffffdab9", "ffffdead", "ffffe1ff", "ffffe4b5", "ffffe4c4", "ffffe4e1", "ffffe7ba", "ffffebcd", "ffffec8b", "ffffefd5", "ffffefdb", "fffff0f5", "fffff5ee", "fffff68f", "fffff8dc", "fffffacd", "fffffaf0", "fffffafa", "ffffff00", "ffffff4d", "ffffffe0", "fffffff0", "ffffffff"]  

class boundingbox:
    lx = 0
    ly = 0
    lz = 0
    ux = 0
    uy = 0
    uz = 0

class coordinates:
    x = 0
    y = 0
    z = 0
    
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def fuck_you_give_me_the_goddamn_color(colorlist,ivg, avorion_colors):
    return difflib.get_close_matches(colorlist[ivg], avorion_colors, n=1, cutoff=0)




def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 2))

def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)



#Useful function
def createFileList(myDir, format='.png'):
    fileList = []
    print(myDir)
    for root, dirs, files in os.walk(myDir, topdown=False):
        for name in files:
            if name.endswith(format):
                fullName = os.path.join(root, name)
                fileList.append(fullName)
    return fileList

# load the original image ### Change this path, or not. I'm not your dad
myFileList = createFileList('C:/Users/wayde/Desktop/pythonshit')

for file in myFileList:
    #print(file)
    img_file = Image.open(file)
    # img_file.show()

    # get original image parameters...
    width, height = img_file.size
    format = img_file.format
    mode = img_file.mode

    # Make image Greyscale
    img_grey = img_file.convert('L')
    #img_grey.save('result.png')
    #img_grey.show()

    # Save Greyscale values
    value = np.asarray(img_grey.getdata(), dtype=np.int).reshape((img_grey.size[1], img_grey.size[0]))
    #value = value.flatten()
    #print(value)
    pixels = list(img_file.convert('RGBA').getdata())
    colorlist = []

    for r, g, b, a in pixels: # just ignore the alpha channel
       colorlist.append(rgb2hex(r, g, b))
        
    avorion_rgb = []
    colors_rgb = []

    for value1 in colorlist:
        colors_rgb.append(hex_to_rgb(value1))
    for value2 in avorion_colors:

        avorion_rgb.append(hex_to_rgb(value2))
    print(avorion_rgb)
#    colors_rgb = [colors_rgb[i:i + 3]  
#        for i in range(len(colors_rgb) - 2)]
    
#    avorion_rgb = [avorion_rgb[i:i + 3]  
#        for i in range(len(avorion_rgb) - 2)]
    #print(avorion_rgb)
    trees = spatial.KDTree(avorion_rgb)
    
    E = lxml.builder.ElementMaker()
    ship_design = E.ship_design
    plan = E.plan


    the_doc = ship_design(
            plan({'accumulateHealth':'true','convex':'false'},

                )   
            )   
    
    #print lxml.etree.tostring(the_doc, pretty_print=True)
    
    fileout = lxml.etree.tostring(the_doc, pretty_print=True)
    xml_file = open("output.xml", "w")
    n = xml_file.write(fileout.decode(sys.stdout.encoding))
    xml_file.close()

    
    parser = lxml.etree.XMLParser(remove_blank_text=True)
    tree = lxml.etree.parse('output.xml',parser)
    condition_elem = tree.find("plan")
    
    
    #lx="1" ly="-0.5" lz="-0.5" ux="2" uy="0.5" uz="0.5" index="7" material="0" look="1" up="3" color="ffbfaea3"



    
    material= 0
    look= 1
    up= 3
    #color = "ffbfaea3"
    bounding_box = boundingbox()
    coordinates = coordinates()
    i = 0  #index
    ix = 0 # previous index
    ivg = 0 # color data pointer
    for column in value:
        coordinates.x += 1
        
        for row in column:
            #print(colordata[ivg])
            ix = i - 1
            coordinates.z = (row / 2) / 200
            coordinates.y += 1

            bounding_box.lx = coordinates.x / 10
            bounding_box.ux = bounding_box.lx - 1 / 10

            bounding_box.ly = coordinates.y / 10
            bounding_box.uy = bounding_box.ly - 1 / 10

            bounding_box.lz = coordinates.z 
            bounding_box.uz = coordinates.z * - 1

            if row == 255:
                ivg += 1
                continue
            #print(colors_rgb[ivg])
            colorindex = trees.query(colors_rgb[ivg])
            #print(colorindex)
            #print(avorion_colors[colorindex[1]])
            color = avorion_colors[colorindex[1]]
            


            item = lxml.etree.SubElement(condition_elem, "item")
            item.set('parent',str(ix))
            item.set('index',str(i))
            block = lxml.etree.SubElement(item, "block")
            block.set('lx',str(bounding_box.lx))
            block.set('ly',str(bounding_box.ly))
            block.set('lz',str(bounding_box.lz))
            block.set('ux',str(bounding_box.ux))
            block.set('uy',str(bounding_box.uy))
            block.set('uz',str(bounding_box.uz))
            block.set('index',str(random.randint(3,30)))
            block.set('material',str(0))
            block.set('look',str(1))
            block.set('up',str(3))
            
            block.set('color',str(color))

            i += 1
            ivg += 1
        coordinates.y = 0
        

        
    tree.write( 'output.xml', encoding='utf-8', xml_declaration=True, pretty_print=True)


