"""
10.10.2018 MGT
Pokus o napodobeni hry OpenTyrian
aktuálně snaha o přepis funkcí pro načtení a zobrazení grafiky Tyrianu

ToDO: Sprity - pruhledna barva
"""

#from wand.image import Image
#from wand.display import display

import pygame
import numpy
import os

class Sprite():
    def __init__(self, width = 0, height = 0, data = []):
        self.width = width
        self.height = height
        self.data = data.copy()

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

def show_pics(pics):
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

def nacti_shp(soubor):
    with open(soubor,'rb') as fin:
        shape_count = int.from_bytes(fin.read(2),byteorder='little', signed=False)
        shape_offsets = []
        for i in range(shape_count):
            shape_offsets.append(int.from_bytes(fin.read(4),byteorder='little', signed=False))
#
#   dump_coin_sprites(shape_offsets, f)
#   dump_weapon_sprites(shape_offsets, f)
#   dump_planet_sprites(shape_offsets, f)
#   dump_tiny_font_sprites(shape_offsets, f)
#   dump_small_font_sprites(shape_offsets, f)
#   dump_font_sprites(shape_offsets, f)
#   dump_option_sprites(shape_offsets, f)
        dump_player_ship_sprites(shape_offsets, fin)
#   dump_player_shot_sprites(shape_offsets, f)
#   dump_powerup_sprites(shape_offsets, f)
# end

def dump_player_ship_sprites(offsets, f):
    start_offset = offsets[8]
    end_offset = offsets[9]
    size = end_offset - start_offset
    f.seek(start_offset,0)
    data = f.read(size)
    sprites = [122, 120, 118, 116, 114, 78, 76, 196, 154, 152, 156, 158, 160, 194, 198, 234, 236, 84, 192, 232, 82, 190, 230, 228, 80] #map {|x| x+1}
    for sprite_num in sprites:
        decode_sprite2x2(data,sprite_num,0)

def decode_sprite2x2(data_string, index, palette=0):
    ul = decode_sprite2(data_string, index, palette)
    ur = decode_sprite2(data_string, index+1, palette)
    ll = decode_sprite2(data_string, index+19, palette)
    lr = decode_sprite2(data_string, index+20, palette)

    # shipSurface = pygame.Surface((ul.width,ul.height),flags = 0, depth = 8)
    # pygame.surfarray.blit_array(shipSurface,ul.data)
    # screen.blit(shipSurface,(0,0))
    #
    # shipSurface = pygame.Surface((ur.width,ur.height),flags = 0, depth = 8)
    # pygame.surfarray.blit_array(shipSurface,ur.data)
    # screen.blit(shipSurface,(14,0))
    #
    # shipSurface = pygame.Surface((ll.width,ll.height),flags = 0, depth = 8)
    # pygame.surfarray.blit_array(shipSurface,ll.data)
    # screen.blit(shipSurface,(0,16))
    #
    # shipSurface = pygame.Surface((lr.width,lr.height),flags = 0, depth = 8)
    # pygame.surfarray.blit_array(shipSurface,lr.data)
    # screen.blit(shipSurface,(14,16))

    sprite = create_sprite_2x2(ul, ur, ll, lr)
    shipSurface = pygame.Surface((sprite.width,sprite.height),flags = 0, depth = 8)
    pygame.surfarray.blit_array(shipSurface,sprite.data)
    screen.blit(shipSurface,(0,0))
    pygame.display.flip()
    paleta = 0
    while True:
        event = pygame.event.poll().type
        if event == pygame.QUIT:
            break
        elif event == pygame.MOUSEBUTTONDOWN:
            break
        elif event == pygame.KEYDOWN:
            paleta += 1
            if paleta == len(palety):
                paleta = 0
            screen.set_palette(palety[paleta])


def decode_sprite2(data_string, index, palette=0):
    MAX_SPRITES = 304
    #data = data_string.unpack("C*")
    #offset = data_string.unpack("S#{MAX_SPRITES}")[index]
    offset = int.from_bytes(data_string[index*2:index*2+2],byteorder='little',signed=False) #numpy.fromstring(data_string,'<l',MAX_SPRITES)
    sprite = []
    width = -1
    height = 0
    width_counter = 0

    while data_string[offset] != 0x0f:
        transparent_pixels = data_string[offset] & 0x0f
        opaque_pixels = (data_string[offset] & 0xf0) >> 4

        width_counter += transparent_pixels + opaque_pixels

        for i in range(transparent_pixels):
            sprite.append(-1)

        if opaque_pixels == 0:
            if width == -1:
                width = width_counter
            height += 1
            width_counter = 0

        for i in range(opaque_pixels):
            offset += 1
            sprite.append(data_string[offset])

        offset += 1

    height += 1

    for i in range((width*height) - len(sprite)):
        sprite.append(-1)

    if width == -1:
        width = height = 0

    return Sprite(width, height, sprite)

def create_sprite_2x2(ul, ur, ll, lr):
    width = max(ul.width + ur.width, ll.width + lr.width)
    height = max(ul.height + ll.height, ur.height + lr.height)

    assert width>0 and height>0, "Empty sprite"
    if width == 0 | height == 0:
        return Sprite()

    height = max(ll.height +14, height) #procpak je tu urceni "height" podruhe a konstanta vysky 14?

    #image = Magick::Image.new(width, height) { self.background_color = "transparent" }
    data = numpy.zeros((width,height),numpy.int8)

    # Upper Left
    if ul.width > 0 and ul.height > 0:
        #image.import_pixels 0,0, ul[:width], ul[:height], "RGBA", ul[:data], Magick::ShortPixel
        for w in range(ul.width):
            for h in range(ul.height):
                data[w][h] = ul.data[h * ul.width + w]

    # Upper Right
    if ur.width > 0 and ur.height > 0:
        assert ur.width + 12 <= width, "Too wide" #vychozi rozmery jednosegmentoveho spritu jsou 12 x 14 (width x height) ?
        #image.import_pixels 12,0, ur[:width], ur[:height], "RGBA", ur[:data], Magick::ShortPixel
        for w in range(ur.width):
            for h in range(ur.height):
                data[w+12][h] = ur.data[h * ur.width + w]

    # Lower Left
    if ll.width > 0 and ll.height > 0:
        #image.import_pixels 0,14, ll[:width], ll[:height], "RGBA", ll[:data], Magick::ShortPixel
        for w in range(ll.width):
            for h in range(ll.height):
                data[w][h+14] = ll.data[h * ll.width + w]

    # Lower Right
    if lr.width > 0 and lr.height > 0:
        #image.import_pixels 12,14, lr[:width], lr[:height], "RGBA", lr[:data], Magick::ShortPixel
        for w in range(lr.width):
            for h in range(lr.height):
                data[w+12][h+14] = lr.data[h * lr.width + w]

    return Sprite(width, height, data)

# def dump_sprites2(data, sprites, dirname, palette=0)
#   out_dir = "../assets/temp/#{dirname}"
#   Dir.mkdir out_dir unless File.exists? out_dir
#
#   sprites.each do |i|
#     sprite = decode_sprite2(data, i, palette)
#     if sprite[:width] > 0 && sprite[:height] > 0
#       create_image_from_sprite(sprite).write "PNG32:#{out_dir}/#{i}.png"
#     end
#   end
# end
#

filePalety = r'c:\DEV\Projects\C\opentyrian\data\palette.dat'
filePics = r'c:\DEV\Projects\C\opentyrian\data\tyrian.pic'
fileShapes = r'c:\DEV\Projects\C\opentyrian\data\tyrian.shp'
#cislo palety odpovidajici jednotlivym obrazkum. Kde ve zdrojaku Tyrianu tyhle cisla jsou?
pcx_pal = [ 0, 7, 5, 8, 10, 5, 18, 19, 19, 20, 21, 22, 5 ]
zoom = 1 #obrazky jsou 320x200 - na HD obrazovce jsou krapet mrnave, tak je zvetsuji....

palety=nacti_palety(filePalety)
#pics=nacti_pics(filePics, zoom)

pygame.init()
#obrazovka je 320 sloupcu x 200 radku, nicmene Array se definuje pole2d[radek, sloupec], pixely tedy do nej zapisujeme
#jakoby otocene o 90 stupnu
screen = pygame.display.set_mode((320*zoom, 200*zoom), 0, 8)
screen.set_palette(palety[0])

#show_pics()
nacti_shp(fileShapes)

pygame.quit()
