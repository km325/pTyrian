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
import struct

TILE_H = 28
TILE_W = 24
MAX_TILES = 600

class Sprite:
    def __init__(self, width = 0, height = 0, data = []):
        self.width = width
        self.height = height
        self.data = data.copy()

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

def load_level(soubor, episode=0):
    # MAP_BUF_LEN = 15 * 600
    fh = open(soubor, 'rb')
    # delka = fh.seek(0, 2)
    fh.seek(0, 0)

    offsPosNum=struct.unpack('H',fh.read(2))[0]
    offsety = struct.unpack(str(offsPosNum)+'L',fh.read(37*4))

    numEpisodes = (offsPosNum-1)//2
    episode = episode % numEpisodes

    fh.seek(offsety[episode*2+1],0) # offsety jsou po dvojicich 1-start episody 2-start mapShape dane epizody - aspon doufam :-)
    mapSh=[]
    mapSh.append(struct.unpack('>128H',fh.read(128*2)))
    mapSh.append(struct.unpack('>128H',fh.read(128*2)))
    mapSh.append(struct.unpack('>128H',fh.read(128*2)))
    map=[]
    map.append(bytes(fh.read(14*300)))
    map.append(bytes(fh.read(14*600)))
    map.append(bytes(fh.read(15*600)))

    fh.close()
    return map, mapSh

def load_shapes(soubor, transparency=True, skipEmpty=True):
    fh = open(soubor, 'rb')
    delka = fh.seek(0, 2)
    fh.seek(0, 0)
    tiles=[]
    for i in range(MAX_TILES):
        tiles.append(pygame.Surface((TILE_W, TILE_H), flags=pygame.SRCALPHA, depth=32))
    i = 0
    d = 0
    while i < MAX_TILES and i < delka:
        temp = ord(fh.read(1))
        if temp == 0:
            # nacte 24x28 byte dlazdice/tile
            for y in range(TILE_H):
                for x in range(TILE_W):
                    colIndex = ord(fh.read(1))
                    col = palety[5][colIndex]
                    if transparency:
                        tiles[d].set_at((x, y),  (0, 0, 0, 0) if colIndex==0 else (col[0], col[1], col[2], 255))
                    else:
                        tiles[d].set_at((x, y), (col[0], col[1], col[2]))
                    # shapes[i].set_at((x, y),  (0, 0, 0, 0) if colIndex==0 else (col[0], col[1], col[2], 255))

            i += 1
            d += 1
        else:
            i += temp
            if not skipEmpty:
                d += 1
    fh.close()
    return tiles

def show_shapes(surf, dimension=(0,0), bgcolor=(30,30,100)):
    surf.fill(bgcolor)
    # pokud nulova size pak nacti podle rozmeru surface
    sx = dimension[0]
    sy = dimension[1]
    if sx + sy == 0:
        sx = surf.get_width() // TILE_W
        sy = surf.get_height() // TILE_H

    for yt in range(sy):
        for xt in range(sx):
            surf.blit(shapes[yt*sx+xt], (xt * TILE_W, yt * TILE_H))

def show_level(surf, layer=0, row=0, dimension=(0,0), bgcolor=(30,30,100)):
    rows = [300, 600, 600]
    cols = [14, 14, 15]
    surf.fill(bgcolor)
    # pokud nulova size pak nacti podle rozmeru surface
    sx = dimension[0] # kolik tiles zobrazit na sirku
    sy = dimension[1] # kolik tiles zobrazit na vysku

    i = row * sx
    for yt in range(sy):
        for xt in range(sx):
            surf.blit(shapes[lMapSh[layer][lMap[layer][i]]-1], (xt * TILE_W, yt * TILE_H))
            i += 1


filePalety = r'c:\DEV\Projects\C\opentyrian\data\palette.dat'
fileLevel = r'c:\DEV\Projects\C\opentyrian\data\tyrian1.lvl'
fileShapes = r'c:\DEV\Projects\C\opentyrian\data\shapesz.dat'

palety = nacti_palety(filePalety)
shapes = load_shapes(fileShapes, True, False)
lMap, lMapSh = load_level(fileLevel)

TILES_XV = 14 # pocet tiles na sirku
TILES_XH = 30 # pocet tiles na vysku

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((TILE_W * TILES_XV, TILE_H * TILES_XH), 0, 32)

row = 0
layer = 0
episode = 0
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    keys =  pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        row += 1
    elif keys[pygame.K_UP]:
        row -= 1
        if row < 0:
            row = 0
    elif keys[pygame.K_l]:
        layer += 1
        layer = layer % 3
    elif keys[pygame.K_e]:
        episode += 1
        row = 0
        layer = 0
        lMap, lMapSh = load_level(fileLevel, episode)
    elif keys[pygame.K_ESCAPE]:
        break

    clock.tick(15)
    #show_shapes(screen, (TILES_XV, TILES_XH))
    show_level(screen, layer, row, (TILES_XV, TILES_XH))
    pygame.display.flip()


pygame.quit()
