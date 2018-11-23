"""
10.10.2018 MGT
Pokus o napodobeni hry OpenTyrian
aktuálně snaha o přepis funkcí pro načtení a zobrazení grafiky Tyrianu
"""

#from wand.image import Image
#from wand.display import display

import pygame
import numpy
import os

def nacti_palety(soubor):
    f=open(soubor,'rb')
    PALETTE_COUNT = 23
    paletteCount = f.seek(0,2) / (256*3)
    f.seek(0,0)
    if PALETTE_COUNT != paletteCount:
        f.close()
        raise RuntimeError("Chybna velikost souboru "+os.path.basename(soubor))
    palettes = []
    for p in range(PALETTE_COUNT):
        palette = []
        for i in range(256):
            r = ord(f.read(1)) << 2
            g = ord(f.read(1)) << 2
            b = ord(f.read(1)) << 2
            palette.append((r, g, b))
        palettes.append(palette)
    f.close()
    return palettes

def nacti_pics(soubor,zoom = 1):
    pics=[]
    #pcx_pal = [ 0, 7, 5, 8, 10, 5, 18, 19, 19, 20, 21, 22, 5 ] #kde ve zdrojaku Tyrianu tyhle cisla jsou?
    with open(soubor,'rb') as fin:
        numOfPics = int.from_bytes(fin.read(2), byteorder='little', signed=False)
        pic_offsets = []
        for i in range(numOfPics):
            pic_offsets.append(int.from_bytes(fin.read(4),byteorder='little', signed=False))
        for n in range(numOfPics):
            fin.seek(pic_offsets[n],0)
            if n == numOfPics-1:
                raw_pic_data=bytes(fin.read())
            else:
                raw_pic_data=bytes(fin.read(pic_offsets[n+1]-pic_offsets[n]))
            # i, p = 0, 0
            # while i<320*200:
            #     if raw_pic_data[p] & 0xC0 == 0xC0:
            #         for m in range(raw_pic_data[p] & 0x3F):
            #             pic_data.append(raw_pic_data[p+1])
            #             i += 1
            #         p += 2
            #     else:
            #         pic_data.append(raw_pic_data[p])
            #         p += 1
            #         i += 1
            pic_data=numpy.zeros((320*zoom,200*zoom))
            pixel = get_pic_pixeldata(raw_pic_data)
            for r in range(200):
                for s in range(320):
                    pic_data[s*zoom:s*zoom+zoom,r*zoom:r*zoom+zoom] = pixel.__next__()
            pics.append(pic_data)
    return pics

def get_pic_pixeldata(raw_pic_data):
#generator, ktery vraci hodnotu jednoho pixelu
    i, p = 0, 0
    while i<320*200:
        if raw_pic_data[p] & 0xC0 == 0xC0:
            for m in range(raw_pic_data[p] & 0x3F):
                yield raw_pic_data[p+1]
                i += 1
            p += 2
        else:
            yield raw_pic_data[p]
            p += 1
            i += 1

def show_pic(picture):
    pygame.surfarray.blit_array(screen, pics[picture])
    screen.set_palette(palety[pcx_pal[picture]])
    pygame.display.flip()

filePalety = r'c:\DEV\Projects\C\opentyrian\data\palette.dat'
filePics = r'c:\DEV\Projects\C\opentyrian\data\tyrian.pic'
pcx_pal = [ 0, 7, 5, 8, 10, 5, 18, 19, 19, 20, 21, 22, 5 ] #kde ve zdrojaku Tyrianu tyhle cisla jsou?
zoom = 4

palety=nacti_palety(filePalety)
pics=nacti_pics(filePics, zoom)

pygame.init()
screen = pygame.display.set_mode((320*zoom, 200*zoom), 0, 8)

# temp = pygame.surfarray.array2d(screen)
# print("Delka pole:",len(temp))
# print("Sirka pole:",len(temp[0]))
# exit(0)

picture = 0
while True:
    event = pygame.event.poll().type
    if  event == pygame.QUIT:
        break
    elif event in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
        if picture == len(pics):
            break
            #picture = 0
        show_pic(picture)
        picture += 1

pygame.quit()

# import os
#
# PALETTE_COUNT = 23
#
# class RGB:
#     """Trida pro ulozeni barev RGB, r, g, b."""
#     def __init__(self):
#         self.r = 0
#         self.g = 0
#         self.b = 0
#     def __init__(self, r:int, g:int, b:int):
#         self.r = r
#         self.g = g
#         self.b = b
#
# dataDir = r'c:\DEV\Projects\C\opentyrian\data'
#
# def JE_loadPals():
#     """Nahraje paletu barev ze souboru 'pallete.dat'
#     Vrací pole RGB hodnot palettes[cislo_palety][index_barvy]"""
#     try:
#         file = open(os.path.join(dataDir,"palette.dat"),'rb')
#     except Exception as exc:
#         raise RuntimeError("Nepodarilo se otevrit soubor 'palette.dat'!") from exc
#
#     paletteCount = file.seek(0,2) / (256 * 3)
#     assert paletteCount == PALETTE_COUNT, "Nesouhlasi velikost palety!"
#     palettes = []
#     paleta = []
#     for p in range(paletteCount):
#         for i in range(256):
#             color = RGB()
#             color.r = file.read(1) << 2
#             color.g = file.read(1) << 2
#             color.b = file.read(1) << 2
#             paleta.append(color)
#         palettes.append(paleta)
#     file.close()
#     return palettes


