import pygame
from pathlib import Path
from PIL import Image, ImageDraw
import os
from enum import Enum

'''
   Copyright 2024 Nuclear Pasta

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''



'''
start = 256
s = start // 4

step = s
for i in range(4): print((s + (s * i)) - 1)
'''



def clamp(value, min, max):
    if value < min: return min
    elif value > max: return max
    return value



#if not Path('./output/').exists(): os.mkdir('./output')



DEFAULT_PALETTE = '''4-9
255, 255, 255
191, 191, 191
101, 232, 232
232, 232, 101
232, 101, 232
232, 174, 102
232, 101, 101
101, 101, 232
101, 232, 101
185, 185, 49
49, 185, 185
185, 49, 185
186, 124, 48
145, 145, 20
20, 145, 145
145, 20, 145
128, 99, 64
185, 49, 49
49, 185, 49
49, 49, 185
145, 89, 20
122, 122, 6
6, 122, 122
122, 6, 122
107, 79, 43
122, 70, 6
63, 63, 63
20, 145, 20
145, 20, 20
20, 20, 145
89, 60, 27
122, 6, 6
6, 6, 122
6, 122, 6
69, 36, 14
1, 1, 1'''



def palette_interpreter(palette: str | list[str]):
    if type(palette) == str: palette = palette.split('\n')
    xy = palette.pop(0)
    if xy.count('-') != 1: print('invalid palette dimensions, using default instead'); return palette_interpreter(DEFAULT_PALETTE)
    else:
        xy = xy.split('-')
        if not xy[0].isdigit() or not xy[1].isdigit(): print('invalid palette dimensions, using default instead'); return palette_interpreter(DEFAULT_PALETTE)
    x, y = int(xy[0]), int(xy[1])
    out = {i: {} for i in range(y)}
    cy = 0
    cx = 0
    for line in palette:
        line = line.strip().replace(' ', '')
        l = line.split(',')
        if len(line) < 1 or line.startswith('--'): continue
        if len(line) < 1 or line.count(',') != 2 or len(line) > 11: print(f'invalid line "{line}" in palette, using default instead'); return palette_interpreter(DEFAULT_PALETTE)
        if not l[0].isdigit() or not l[1].isdigit() or not l[2].isdigit(): print(f'invalid line "{line}" in palette, using default instead'); return palette_interpreter(DEFAULT_PALETTE)
        
        r, g, b = int(l[0]), int(l[1]), int(l[2])
        if r > 255 or g > 255 or b > 255: print(f'invalid line "{line}" in palette, using default instead'); return palette_interpreter(DEFAULT_PALETTE)

        if cx > x - 1: cx = 0; cy += 1
        out[cy][cx] = (r, g, b)
        cx += 1

    return out



def load_palette(name):
    with open(name, 'rt') as pal: return palette_interpreter(pal.read())



print('====BEGIN LOAD LOG====')



screenxy = 800, 800
canvassize = 16, 16
pixelscale = 10
gridcolors = (128, 128, 128), (191, 191, 191)
currentpalette = palette_interpreter(DEFAULT_PALETTE)
output = './output'
#print(currentpalette)


def comhelp():
    print('help: prints command help')
    print('screen [screen x] [screen y]: sets the screen size to the given x and y')
    print('(default screen size is 800 by 800)')
    print('scale [scale]: sets the pixel scale')
    print('(default is 10; bigger numbers mean the drawing area is smaller)')
    print('canvas [canvas x] [canvas y]: sets the canvas size to the given x and y')
    print('(default canvas size is 16 by 16)')
    print('run: closes this dialogue and runs the drawer')
    print('to skip is dialogue entirely, put a file named "skipinitconsole.txt" next to the executable/python file')
    print('you can preload settings using this file, for more information, type "sicf"')

def sicfhelp():
    print('settings you can preload:')
    print('screen size(in format "screenxy: [x], [y]")')
    print('pixel scale factor(in format "pixelscale: [scale]")')
    print('canvas size(in format "screensize: [x], [y]")')
    print('output folder(in format "output: [path/to/folder]")')
    #print('grid colors(in format "gridcolors: [r], [g], [b]; [r], [g], [b]")')

cli_running = True

clisettings: dict[str, str] = {}

if Path('./skipinitconsole.txt').exists():
    with open('./skipinitconsole.txt', 'rt') as sf: f = sf.read().split('\n')
    try: clisettings = {l.replace(' ', '').split(':')[0]: l.replace(' ', '').split(':')[1] for l in f}
    except Exception as e: print(e)
    cli_running = False
else:
    if Path('../skipinitconsole.txt').exists():
        with open('../skipinitconsole.txt', 'rt') as sf: f = sf.read().split('\n')
        try: clisettings = {l.replace(' ', '').split(':')[0]: l.replace(' ', '').split(':')[1] for l in f}
        except Exception as e: print(e)
        cli_running = False
    else:
        print('"skipinitconsole.txt" not found, ignoring')

try: sx, sy = clisettings['screenxy'].split(','); sx, sy = int(sx), int(sy); screenxy = sx, sy
except KeyError: print('"screenxy" value not given, using default instead')
except Exception as e: print(e)


try: pixelscale = int(clisettings['startingpixelscale'])
except KeyError: print('"startingpixelscale" value not given, using default instead')
except Exception as e: print(e)


try: sx, sy = clisettings['canvassize'].split(','); sx, sy = int(sx), int(sy); canvassize = sx, sy
except KeyError: print('"canvassize" value not given, using default instead')
except Exception as e: print(e)


try:
    startpal = './palettes/' + clisettings['startingpalette'].removeprefix('.pypal') + '.pypal'
    if not Path(startpal).exists(): print(f'palette "{startpal}" doesn\'t exist, using default instead'); raise KeyError()
    currentpalette = load_palette(startpal)
except KeyError: print('"palette" value not given, using default instead')
except Exception as e: print(e)


try:
    outputconf = Path(clisettings['output'])
    if not Path(outputconf).exists(): print(f'path "{outputconf}" doesn\'t exist, using default instead'); raise KeyError()
    if not Path(outputconf).is_dir(): print(f'path "{outputconf}" isn\'t a folder, using default instead'); raise KeyError()
    output = str(outputconf).removesuffix('/').removesuffix('\\')
except KeyError: print('"output" value not given, using default instead')
except Exception as e: print(e)


if cli_running: comhelp()

while cli_running:
    inp = input('> ').casefold().strip()
    if inp in ('exit', 'quit'): raise SystemExit()
    elif inp == 'help': comhelp()
    elif inp == 'sicf': sicfhelp()
    elif inp.startswith('screen '):
        inp = inp.removeprefix('screen ').split(' ')
        if len(inp) < 2: print('not enough arguments!'); continue
        if not inp[0].isdigit() or len(inp[0].replace('0', '')) < 1: print(f'"{inp[0]}" is not a valid number!'); continue
        if not inp[1].isdigit() or len(inp[1].replace('0', '')) < 1: print(f'"{inp[1]}" is not a valid number!'); continue
        screenxy = int(inp[0]), int(inp[1])
    elif inp.startswith('scale '):
        inp = inp.removeprefix('scale ').strip()
        if len(inp) < 1: print('not enough arguments!'); continue
        if not inp.isdigit() or len(inp.replace('0', '')) < 1: print(f'"{inp}" is not a valid number!'); continue
        pixelscale = int(inp)
        print('scale is now', pixelscale)
    elif inp.startswith('canvas '):
        inp = inp.removeprefix('canvas ').split(' ')
        if len(inp) < 2: print('not enough arguments!'); continue
        if not inp[0].isdigit() or len(inp[0].replace('0', '')) < 1: print(f'"{inp[0]}" is not a valid number!'); continue
        if not inp[1].isdigit() or len(inp[1].replace('0', '')) < 1: print(f'"{inp[1]}" is not a valid number!'); continue
        canvassize = int(inp[0]), int(inp[1])
    elif inp == 'run': print('running Pyxil Art Program...'); cli_running = False; break



class Ignore:'Flagging class'; pass



def is_inside_rect(rect: tuple[int, int, int, int] | tuple[float, float, float, float], x: int | float, y: int | float):
    return (x >= rect[0] and x <= rect[0] + rect[2]) and (y >= rect[1] and y <= rect[1] + rect[3])



# initialize game
pygame.init()

# creating a screen

screen = pygame.display.set_mode(screenxy)  # passing width and height

# title and icon
pygame.display.set_caption('Pyxil Art Program')


try:
    print('attempting to access app icon...')
    icon = pygame.image.load('./pyxil-iconv1.png')
    print('attempt was successful, icon set')
except FileNotFoundError:
    try:
        print('attempt failed, attempting again...')
        icon = pygame.image.load('../pyxil-iconv1.png')
        print('attempt was successful, icon set')
    except FileNotFoundError:
        print('second attempt failed, ignoring')
        icon = Ignore()
if type(icon) != Ignore: pygame.display.set_icon(icon)


clock = pygame.time.Clock()

pygame.font.init() # initiate font
# font getter code(I'm sorry)
ispixelcode = False
try:
    print('attempting to access users...')
    users = [str(f).rsplit('/', 1)[-1] for f in Path('/Users').iterdir()] # get all folders inside the "/Users" root folder
    remove = []
    for u in range(len(users)):
        if users[u].startswith('.') or users[u].casefold() in ('public', 'shared'): remove.append(u) # flag unimportant/system folders for removal
    remove.reverse()
    for rm in remove: del users[rm] # # remove flagged folders
    del remove
    if len(users) > 0: user = users[0]; del users # get first user(for no reason in particular, it's just the easiest)
    else: print('unable to access users'); raise FileNotFoundError() # if there are no users, jump to next try-except
    print(f'users accessed(user "{user}"), attempting to get "PixelCode-Medium.ttf"...')
    mainfont = pygame.font.Font('/Users/' + user + '/Library/Fonts/PixelCode-Medium.ttf', 20) # attempt to get the coolest and best font(MacOS specific path)
    smolfont = pygame.font.Font('/Users/' + user + '/Library/Fonts/PixelCode-Medium.ttf', 5)
    print('succesfully got "PixelCode-Medium.ttf"')
    ispixelcode = True
except FileNotFoundError: # if trying to get the coolest and best font fails, fall back to the second greatest
    print('attempt failed, falling back to "Comic Sans MS.ttf"...')
    try:
        mainfont = pygame.font.Font('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf', 20) # attempt to get the second greatest font(MacOS specific path)
        smolfont = pygame.font.Font('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf', 5) # attempt to get the second greatest font(MacOS specific path)
        print('successfully fell back on "Comic Sans MS.ttf"')
    except FileNotFoundError: # if that fails, fall back to the worst font possible
        print('failed, falling back to boring as heck default font...')
        try:
            mainfont = pygame.font.Font('freesansbold.ttf', 20) # attempt to get the worst font possible
            smolfont = pygame.font.Font('freesansbold.ttf', 5) # attempt to get the worst font possible
            print('successfully fell back on "freesansbold.ttf"(sadly)')
        except Exception as e: # if even THAT fails, screw you
            print('unknown failure occured:')
            print(e)
            print('this application will now quit')
            raise SystemExit()



print('====END LOAD LOG====')



'''
def showtext(x, y):
    text = mainfont.render('Hello world', not ispixelcode, (255, 255, 255))
    screen.blit(text, (x, y))
'''





icolor = [0, 0]

#ccolor = currentpalette[icolor[1]][icolor[0]]

pixindex = [0, 0]

pixelstart = [0, 0]


canvas = {y: {x: (0, 0, 0) for x in range(canvassize[0])} for y in range(canvassize[1])} #{y: {x: (0, 0, 0) for x in range(screenxy[0] // pixelscale)} for y in range(screenxy[1] // pixelscale)}
#print(len(canvas), len(canvas[0]))


def drawcursor(): pygame.draw.rect(screen, (255, 255, 255), ((pixindex[1] * pixelscale) + pixelstart[0], (pixindex[0] * pixelscale) + pixelstart[1], pixelscale, pixelscale), 1)



def shift_by_one_left():
    for y in list(canvas.keys()):
        first = ()
        for x in list(canvas[y].keys()):
            if x == len(canvas[y]) - 1: x == first; continue
            if x == 0: first == canvas[y][x]
            canvas[y][x] = canvas[y][x + 1]

def shift_by_one_right():
    for y in list(canvas.keys()):
        last = ()
        X_AXIS = list(canvas[y].keys()).copy()
        X_AXIS.reverse()
        for x in X_AXIS:
            if x == 0: x == last; #continue
            if x == len(canvas[y]) - 1: last == canvas[y][x]
            canvas[y][x] = canvas[y][x - 1]



def drawcheckergrid():
    for y in list(canvas.keys()):
        for x in list(canvas[y].keys()):
            if y % 2: colorused = gridcolors[1] if not x % 2 else gridcolors[0]
            else: colorused = gridcolors[1] if x % 2 else gridcolors[0]
            pygame.draw.rect(screen, colorused, ((x * pixelscale) + pixelstart[0], (y * pixelscale) + pixelstart[1], pixelscale, pixelscale))



def drawpixels():
    for y in list(canvas.keys()):
        for x in list(canvas[y].keys()):
            if canvas[y][x] == (0, 0, 0): continue
            pygame.draw.rect(screen, canvas[y][x], ((x * pixelscale) + pixelstart[0], (y * pixelscale) + pixelstart[1], pixelscale, pixelscale))



def draw_cpalette(x, y, scale):
    for cpy in list(currentpalette.keys()):
        for cpx in list(currentpalette[cpy].keys()):
            pygame.draw.rect(screen, currentpalette[cpy][cpx], ((cpx * scale) + x, (cpy * scale) + y, scale, scale))
            if icolor[1] == cpy and icolor[0] == cpx:
                r, b, g = currentpalette[cpy][cpx]
                selcolor = (0, 0, 0) if (r + b + g) * 3 > 1151 else (255, 255, 255)
                pygame.draw.rect(screen, selcolor, ((cpx * scale) + x, (cpy * scale) + y, scale, scale), 2)



def drawrgbhitbox():
    pygame.draw.rect(screen, (255, 0, 0), (4, 10, 38, 20))
    pygame.draw.rect(screen, (0, 255, 0), (49, 10, 38, 20))
    pygame.draw.rect(screen, (0, 255, 255), (94, 10, 38, 20))

def showrgb(x, y, color):
    for c in range(len(currentpalette[icolor[1]][icolor[0]])):
        rgb = mainfont.render(str(currentpalette[icolor[1]][icolor[0]][c]), False, color)
        screen.blit(rgb, (x + (45 * c), y))
        if icolor == c:
            cursor = mainfont.render('^', False, color)
            screen.blit(cursor, (x + (45 * c), y + 20))


def showcolor(x, y):
    pygame.draw.rect(screen, currentpalette[icolor[1]][icolor[0]], (x, y, 50, 20))


def drawborderLs():
    #border1 = smolfont.render('boarder', not ispixelcode, (255, 255, 255))
    #border2 = smolfont.render('boarder', not ispixelcode, (255, 255, 255))
    linewidth = 2
    cornerpos = 10
    #screen.blit(border1, (pixelstart[0] - cornerpos, (pixelstart[1] - cornerpos) - 8))
    pygame.draw.line(screen, (255, 255, 255), (pixelstart[0] - cornerpos, pixelstart[0] - linewidth), (pixelstart[0] + (cornerpos * 2), pixelstart[0] - linewidth), linewidth - pixelscale)
    pygame.draw.line(screen, (255, 255, 255), (pixelstart[0] - linewidth, pixelstart[0] - cornerpos), (pixelstart[0] - linewidth, pixelstart[0] + (cornerpos * 2)), linewidth - pixelscale)

    pygame.draw.line(screen, (255, 255, 255), (pixelstart[0] - cornerpos, pixelstart[0] - linewidth), (pixelstart[0] + (cornerpos * 2), pixelstart[0] - linewidth), linewidth - pixelscale)
    pygame.draw.line(screen, (255, 255, 255), (pixelstart[0] - linewidth, pixelstart[0] - cornerpos), (pixelstart[0] - linewidth, pixelstart[0] + (cornerpos * 2)), linewidth - pixelscale)


def showisexporting(x, y):
    text = mainfont.render('Please look at the console', not ispixelcode, (255, 255, 255))
    screen.blit(text, (x, y))



def colorpick(color: tuple[int, int, int]):
    for cpy in list(currentpalette.keys()):
        for cpx in list(currentpalette[cpy].keys()):
            if color == currentpalette[cpy][cpx]: return [cpx, cpy]



mouse_x, mouse_y = 0, 0
m_left, m_middle, m_right = False, False, False
can_use_left, can_use_middle, can_use_right = 0, 0, 0

mousemode = True

holding_control = False
holding_shift = False

# tools
class Tools(Enum):
    PENCIL = 'pencil'
    BUCKET = 'bucket'
    LINE = 'line'
    SHAPETOOL = 'shapetool'

currenttool = Tools.PENCIL

# background
candrawlinegrid = False
candrawcheckergrid = False
whitebackground = False

#canshowrgb = True
#colordisplay = False

selectingpalette = False

isexporting = False

# timers
cp_timer = 0 # current palette timer
ct_timer = 0 # current tool timer



def showcurrenttool(x, y):
    text = mainfont.render(f'current tool is now {currenttool.value}', not ispixelcode, (255, 255, 255))
    screen.blit(text, (x, y))



def export(filename_to_export: str):
    global isexporting
    print('initializing image...')
    img = Image.new('RGBA', (len(canvas[0]), len(canvas)))
    print('beginning write')
    #imgd = ImageDraw.Draw(img)
    for y in list(canvas.keys()):
        for x in list(canvas[y].keys()):
            if canvas[y][x] == (0, 0, 0): rgba = 0, 0, 0, 0
            else: rgba = canvas[y][x]; rgba = list(rgba); rgba.append(255); rgba = tuple(rgba)
            print('writing', x, str(y) + '...          \r', end="")
            img.putpixel((x, y), rgba)
    print('writing complete')
    upscalefactor = input('Do you want to upscale the image?\nif yes, type the amount you want to upscale by(e.g. "2" would be upscale by 2x)\nif not, type anything that isn\'t a number\n')
    if upscalefactor.isdigit():
        print('resizing image...')
        upscalefactor = int(upscalefactor)
        oldsize = img.size
        img_upscaled = img.resize((oldsize[0] * upscalefactor, oldsize[1] * upscalefactor), Image.Resampling.BOX)
        img = img_upscaled
        print('image resized')
    print(f'saving as "{output + "/" + filename_to_export}"...')
    img.save(output + '/' + filename_to_export)
    print('saved')
    isexporting = False
    print('exporting complete')


def saveas():
    global isexporting
    print('save as?')
    #filecontext = ''#'./'
    #cursor = '> '
    print('type "cancel" to exit this dialogue')
    print('type "save [name]" to save the file as that name')
    print('(compatible extensions are: png and jpg because screw you I\'m not doing any others)')
    print('(if no extension is given, the image will default to .png)')
    while True:
        #if filecontext.rsplit('/', 1)[-1]: cursor = filecontext.rsplit('/', 1)[-1] + ' ' + cursor
        inp = input('> ')
        if inp in ('cancel'): isexporting = False; return
        elif inp.startswith('save '):
            inp = inp.removeprefix('save ').strip()
            if len(inp.rsplit('.', 1)) == 2 and inp.rsplit('.', 1)[-1] not in ('png', 'jpg'): print('extension is not valid!'); continue
            if not inp.endswith(('.png', '.jpg')): inp += '.png'
            if Path(output, inp).exists():
                while True:
                    reply = input(f'image "{inp}" already exists, do you want to overwrite it?(y/n)\n')
                    match reply:
                        case 'y': os.remove(output + '/' + inp); break
                        case 'n': return
                        case x: continue
            export(inp)
            break



game_running = True
while game_running:
    icolor[0] = clamp(icolor[0], 0, len(currentpalette[icolor[1]]) - 1)
    icolor[1] = clamp(icolor[1], 0, len(currentpalette) - 1)

    if whitebackground: screen.fill((255, 255, 255))
    else: screen.fill((0, 0, 0))

    if can_use_left > 0: can_use_left -= 1
    if can_use_middle > 0: can_use_middle -= 1
    if can_use_right > 0: can_use_right -= 1

    if cp_timer > 0: cp_timer -= 1

    if isexporting:
        clock.tick(60)
        showisexporting(screenxy[0] - 600, screenxy[1] - 500)
        pygame.display.update()
        saveas()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: game_running = False; break

            #if event.key == pygame.K_g and candrawlinegrid: candrawlinegrid = False
            #elif event.key == pygame.K_g and not candrawlinegrid: candrawlinegrid = True

            match event.key:
                case pygame.K_1: currenttool = Tools.PENCIL#; print(f'current tool switched to "{currenttool}"'); ct_timer = 35
                case pygame.K_2: currenttool = Tools.BUCKET#; print(f'current tool switched to "{currenttool}"'); ct_timer = 35
                case pygame.K_3: currenttool = Tools.LINE#; print(f'current tool switched to "{currenttool}"'); ct_timer = 35
                case pygame.K_4: currenttool = Tools.SHAPETOOL#; print(f'current tool switched to "{currenttool}"'); ct_timer = 35

            if event.key == pygame.K_g and candrawcheckergrid: candrawcheckergrid = False
            elif event.key == pygame.K_g and not candrawcheckergrid: candrawcheckergrid = True

            if event.key == pygame.K_b and whitebackground: whitebackground = False
            elif event.key == pygame.K_b and not whitebackground: whitebackground = True

            if event.key == pygame.K_m and mousemode: mousemode = False
            elif event.key == pygame.K_m and not mousemode: mousemode = True

            if event.key == pygame.K_p and selectingpalette: selectingpalette = False
            elif event.key == pygame.K_p and not selectingpalette: selectingpalette = True

            #if event.key == pygame.K_r and canshowrgb: canshowrgb = False
            #elif event.key == pygame.K_r and not canshowrgb: canshowrgb = True

            #if event.key == pygame.K_c and colordisplay: colordisplay = False
            #elif event.key == pygame.K_c and not colordisplay: colordisplay = True

            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT): holding_shift = True

            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL): holding_control = True

            '''
            if event.key == pygame.K_UP:
                if ccolor[icolor] < 255:
                    add = 5 if holding_shift else 1
                    if ccolor[icolor] + add > 255: ccolor[icolor] = 255
                    else: ccolor[icolor] += add
                else: ccolor[icolor] = 255

            if event.key == pygame.K_DOWN:
                if ccolor[icolor] > 0:
                    sub = 5 if holding_shift else 1
                    if ccolor[icolor] - sub < 0: ccolor[icolor] = 0
                    else: ccolor[icolor] -= sub
                else: ccolor[icolor] = 0
            
            if event.key == pygame.K_RIGHT:
                if ccolor[icolor] < 255:
                    add = 50 if holding_shift else 10
                    if ccolor[icolor] + add > 255: ccolor[icolor] = 255
                    else: ccolor[icolor] += add
                else: ccolor[icolor] = 255

            if event.key == pygame.K_LEFT:
                if ccolor[icolor] > 0:
                    sub = 50 if holding_shift else 10
                    if ccolor[icolor] - sub < 0: ccolor[icolor] = 0
                    else: ccolor[icolor] -= sub
                else: ccolor[icolor] = 0
            '''
            
            if event.key == pygame.K_RIGHT:
                icolor[0] = clamp(icolor[0] + 1, 0, len(currentpalette[icolor[1]]) - 1); cp_timer = 35
                
            if event.key == pygame.K_LEFT:
                icolor[0] = clamp(icolor[0] - 1, 0, len(currentpalette[icolor[1]]) - 1); cp_timer = 35
            
            if event.key == pygame.K_UP:
                icolor[1] = clamp(icolor[1] - 1, 0, len(currentpalette) - 1); cp_timer = 35

            if event.key == pygame.K_DOWN:
                icolor[1] = clamp(icolor[1] + 1, 0, len(currentpalette) - 1); cp_timer = 35
        
            if event.key == pygame.K_w and not mousemode:
                if pixindex[0] > 0: pixindex[0] -= 1
            
            if event.key == pygame.K_s and not mousemode:
                if pixindex[0] < len(canvas): pixindex[0] += 1
            
            if event.key == pygame.K_a and not mousemode:
                if pixindex[1] > 0: pixindex[1] -= 1
            
            if event.key == pygame.K_d and not mousemode:
                if pixindex[1] < len(canvas[0]): pixindex[1] += 1
            
            if event.key == pygame.K_SPACE and not mousemode:
                match currenttool:
                    case Tools.PENCIL: canvas[pixindex[0]][pixindex[1]] = currentpalette[icolor[1]][icolor[0]]
                    case x: print(f'unknown tool "{currenttool}"')
            
            if event.key == pygame.K_q and not mousemode:
                icolor = colorpick(canvas[pixindex[0]][pixindex[1]])
            
            if event.key == pygame.K_BACKSPACE and not mousemode:
                canvas[pixindex[0]][pixindex[1]] = (0, 0, 0)
            
            if event.key == pygame.K_s and holding_control: isexporting = True

            #if event.key == pygame.K_COMMA: pixelstart += 1#shift_by_one_left()
            #if event.key == pygame.K_PERIOD: pixelstart -= 1#shift_by_one_right()
        
        if event.type == pygame.MOUSEWHEEL and mousemode:
            '''if (is_inside_rect((4, 10, 38, 20), mouse_x, mouse_y) or
                is_inside_rect((49, 10, 38, 20), mouse_x, mouse_y) or
                is_inside_rect((94, 10, 38, 20), mouse_x, mouse_y)):
                if ccolor[icolor] - event.dict['y'] <= 0: ccolor[icolor] = 0
                elif ccolor[icolor] - event.dict['y'] >= 255: ccolor[icolor] = 255
                else: ccolor[icolor] -= event.dict['y']
            else:'''
            if holding_shift:
                pixelstart[0] -= event.dict['x']
            elif holding_control:
                pixelstart[1] -= event.dict['y']
            else:
                if pixelscale - event.dict['y'] < 1: pixelscale = 1
                else: pixelscale -= event.dict['y']
        
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT): holding_shift = False
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL): holding_control = False
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    m_left, m_middle, m_right = pygame.mouse.get_pressed()

    if m_left and mousemode and can_use_left == 0:
        match currenttool:
            case Tools.PENCIL: canvas[pixindex[0]][pixindex[1]] = currentpalette[icolor[1]][icolor[0]]
            case x: print(f'unknown tool "{currenttool}"')
        can_use_left = 2
    
    if m_right and mousemode and can_use_right == 0:
        canvas[pixindex[0]][pixindex[1]] = 0, 0, 0
        can_use_right = 2
    
    if m_middle and mousemode and can_use_middle == 0:
        icolor = colorpick(canvas[pixindex[0]][pixindex[1]])
        can_use_middle = 2

    #showtext(50, 100)

    #red: (4, 10, 38, 20)
    #blue: (49, 10, 38, 20)
    #green: (94, 10, 38, 20)

    #print(mouse_x, mouse_y)

    #print(is_inside_rect((4, 10, 38, 20), mouse_x, mouse_y))

    '''
    if is_inside_rect((4, 10, 38, 20), mouse_x, mouse_y) and mousemode:
        icolor = 0
    if is_inside_rect((49, 10, 38, 20), mouse_x, mouse_y) and mousemode:
        icolor = 1
    if is_inside_rect((94, 10, 38, 20), mouse_x, mouse_y) and mousemode:
        icolor = 2
    '''

    if mousemode:
        mx = clamp((mouse_x - pixelstart[0]) // pixelscale, 0, len(canvas[0]) - 1)
        my = clamp((mouse_y - pixelstart[1]) // pixelscale, 0, len(canvas) - 1)
        #if (mx > 0 and mx < len(canvas[0])) and (my > 0 and my < len(canvas)):
        pixindex = [my, mx]

    #if candrawlinegrid: drawlinegrid()
    if candrawcheckergrid: drawcheckergrid()

    drawpixels()

    #drawborderLs()

    #print(pixelstart, holding_shift)

    drawcursor()
    
    if cp_timer: draw_cpalette(5, 5, 20)
    if ct_timer: showcurrenttool(5, screenxy[1] - 40)

    #drawrgbhitbox()

    #if canshowrgb: showrgb(5, 5, (255, 255, 255))
    #if colordisplay: showcolor(5, 47)

    clock.tick(60)

    pygame.display.update()