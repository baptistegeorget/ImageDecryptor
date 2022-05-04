from PIL import Image
from random import randint
from tkinter import *

class ImageManipulation:
    
    def __init__(self, screen_width, screen_height):
        
        self.__root = Tk(className="1ARIT")
        self.__root.geometry(str(screen_width)+"x"+str(screen_height))
        self.__root.attributes('-fullscreen', True)
        
        self.__canvas = Canvas(self.__root, width=screen_width, height=screen_height, highlightthickness=0, bg="red")
        self.__canvas.place(x=screen_width/2, y=screen_height/2, anchor="center")
        
        self.__button_chiffrement_image = Button(self.__root, text="Chiffrement image", width=20, pady=50, padx=75, highlightbackground="black", font=("Helvetica", 30, "bold"))
        self.__button_chiffrement_image.place(x=screen_width*0.5, y=screen_height*0.25, anchor="center")
        
        self.__button_masquage_image = Button(self.__root, text="Masquage image", width=20, pady=50, padx=75, highlightbackground="black", font=("Helvetica", 30, "bold"))
        self.__button_masquage_image.place(x=screen_width*0.5, y=screen_height*0.50, anchor="center")
        
        self.__button_masquage_texte = Button(self.__root, text="Masquage texte", width=20, pady=50, padx=75, highlightbackground="black", font=("Helvetica", 30, "bold"))
        self.__button_masquage_texte.place(x=screen_width*0.5, y=screen_height*0.75, anchor="center")
        
        self.__root.mainloop()
    
    def chiffrer_dechiffrer_image(self, image=str(), key_image=str(), name_save=str()):
        image = "images/"+image+".bmp"
        key_image = "images/"+key_image+".bmp"
        image_open = Image.open(image)
        key_image_open = Image.open(key_image)
        width_image = image_open.width
        height_image = image_open.height
        width_key_image = key_image_open.width
        height_key_image = key_image_open.height
        if width_image == width_key_image and height_image == height_key_image:
            new_image = Image.new(mode="RGB", size=(width_image, height_image))
            new_image_load = new_image.load()
            pixel_count = 0
            for x in range(width_image):
                for y in range(height_image):
                    r1, g1, b1 = image_open.getpixel((x, y))
                    r2, g2, b2 = key_image_open.getpixel((x, y))
                    r3, g3, b3 = r1^r2, g1^g2, b1^b2
                    new_image_load[x, y] = (r3, g3, b3)
                    pixel_count += 1
                    print("Chargement: ("+str(pixel_count)+"/"+str(width_image*height_image)+")")
            new_image.save("images/"+name_save+".bmp")
                
    def create_key_image(self, width=int(), height=int(), name_save=str()):
        width, height = abs(width), abs(height)
        new_image = Image.new(mode="RGB", size=(width, height))
        new_image_load = new_image.load()
        pixel_count = 0
        for x in range(width):
            for y in range(height):
                new_image_load[x, y] = (randint(0, 255), randint(0, 255), randint(0, 255))
                pixel_count += 1
                print("Chargement: ("+str(pixel_count)+"/"+str(width*height)+")")
        new_image.save("images/"+name_save+".bmp")
    
    def masquer_demasquer_image(self, image=str(), key_image=str(), key=int(), action=str(), name_save=str()):
        key = abs(key)
        image = "images/"+image+".bmp"
        key_image = "images/"+key_image+".bmp"
        image_open = Image.open(image)
        key_image_open = Image.open(key_image)
        width_image = image_open.width
        height_image = image_open.height
        width_key_image = key_image_open.width
        height_key_image = key_image_open.height
        if width_image == width_key_image and height_image == height_key_image:
            new_image = Image.new(mode="RGB", size=(width_image, height_image))
            new_image_load = new_image.load()
            pixel_count = 0
            for x in range(width_image):
                for y in range(height_image):
                    r1, g1, b1 = image_open.getpixel((x, y))
                    r2, g2, b2 = key_image_open.getpixel((x, y))
                    r3, g3, b3 = self.algo(action, r1, r2, key), self.algo(action, g1, g2, key), self.algo(action, b1, b2, key)
                    new_image_load[x, y] = (r3, g3, b3)
                    pixel_count+=1
                    print("Chargement: ("+str(pixel_count)+"/"+str(width_image*height_image)+")")
            new_image.save("images/"+name_save+".bmp")
    
    def algo(self, action=str(), val1=int(), val2=int(), key=int()):
        if action == "chiffrer":
            val3 = round(val2+1/key*val1)
            if val3 > 255:
                val3 = 255
        elif action == "dechiffrer":
            val3 = key*(val1-val2)
        return val3
    
    def masquer_texte(self, image=str(), texte=str(), name_save=str()):
        chain_bin = ""
        i = 0
        image = "images/"+image+".bmp"
        image_open = Image.open(image)
        image_load = image_open.load()
        height = image_open.height
        width = image_open.width
        for caractere in range(len(texte)):
            chain_bin += self.str_to_bin(texte[caractere])
        if len(chain_bin) < (width*height*3):
            for y in range(height):
                if i < len(chain_bin):
                    for x in range(width):
                        if i < len(chain_bin):
                            rgb = list(image_open.getpixel((x, y)))
                            if rgb[0] == 255:
                                rgb[0] = 254
                            if rgb[1] == 255:
                                rgb[1] = 254
                            if rgb[2] == 255:
                                rgb[2] = 254
                            for z in range(len(rgb)):
                                if i < len(chain_bin):
                                    rgb[z] += int(self.str_to_bin(chr(rgb[z]))[-1])^int(chain_bin[i])
                                i += 1
                                print("Chargement: ("+str(i)+"/"+str(len(chain_bin))+")")
                            image_load[x, y] = tuple(rgb)
            image_open.save("images/"+name_save+".bmp")
                
    def str_to_bin(self, string=str()):
        nb = ord(string)
        chain_bin = str(bin(nb))
        chain_bin = chain_bin[2:]
        while len(chain_bin) != 8:
            chain_bin = "0"+chain_bin
        return chain_bin
        
    def demasquer_texte(self, image=str()):
        image = "images/"+image+".bmp"
        image_open = Image.open(image)
        width = image_open.width
        height = image_open.height
        chain_bin = ""
        for y in range(height):
            for x in range(width):
                r, g, b = image_open.getpixel((x, y))
                rgb = [r, g, b]
                for z in range(len(rgb)):
                    if rgb[z]%2 == 1:
                        chain_bin += "1"
                    else:
                        chain_bin += "0"
                    print("Chargement: ("+str(len(chain_bin))+"/"+str(height*width*3)+")")
        print(self.bin_to_str(chain_bin))
                        
    def bin_to_str(self, chain_bin=str()):
        x, y = 0, 8
        texte = ""
        while y <= len(chain_bin) and len(texte) < 100:
            byte = chain_bin[x:y]
            mult = 1
            nb = 0
            for i in range(7, -1, -1):
                if byte[i] == "1":
                    nb = nb+(1*mult)
                mult *= 2
            texte += chr(nb)
            x += 8
            y += 8
        return texte
    
ImageManipulation(1440, 900)