# main.py
# Dilpreet Chana

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from pygame import *
from random import *
from math import *
from tools import *
init()

screen = display.set_mode((1280, 900))
display.set_caption("Star Trek Paint")  # Set title of window

# load colour palette and title images
colour_palette = image.load("colour_palette.jpg")
star_trek_logo = image.load("title.jpg")
star_trek_logo = transform.smoothscale(star_trek_logo,(218,100))

#---------------------initialize screen---------------------------
screen.fill((0, 0, 0))

screen.blit(colour_palette, (10, 650))
screen.blit(star_trek_logo,(900,5))

mixer.music.load("Star Trek.mp3")
mixer.music.play(-1,0.0)

root = Tk()
root.withdraw()

#--------------create Rects---------------------------
can_rect = Rect(383, 80, 828, 550)  # canvas Rect
tool_area_rect = Rect(0, 80, 220, 450)  # Rect of area of selectable tools
music_rect = Rect(175, 595, 45, 45)  # music pause/play button Rect
colour_area = Rect(10, 650, 200, 200)  # Rect of area of colour palette
tab_rect = Rect(0, 0, 383, 80)  # Rect of area of tabs
discrip_rect = Rect(383, 0, 517, 80)  # Rect for area with tool discriptions
undo_rect = Rect(120, 540, 45, 45)  # undo button Rect
redo_rect = Rect(120, 595, 45, 45)  # redo button Rect
clear_rect = Rect(175, 540, 45, 45)  # clear button Rect
save_rect = Rect(1216, 80, 60, 60)  # save button Rect
load_rect = Rect(1216, 150, 60, 60)  # load button Rect

# list of images to be on the background
back_images = [transform.scale(image.load("cap kirk back.png"), (280, 500)), transform.scale(image.load("spock_back.png"), (209, 270)), transform.scale(image.load("starship back.png"), (366, 207))]

# display backround images
screen.blit(back_images[0], (160, 10))
screen.blit(back_images[1], (1071, 630))
screen.blit(back_images[2], (383, 630))

# create subsurfaces
canvas = screen.subsurface(can_rect)
tool_area = screen.subsurface(tool_area_rect)
discrip_area = screen.subsurface(discrip_rect)

canvas.fill((255, 255, 255))

# draw visual representation of buttons
draw.rect(screen, (214, 182, 54), undo_rect)
draw.rect(screen, (214, 182, 54), redo_rect)
draw.rect(screen, (214, 182, 54), clear_rect)
draw.rect(screen, (214, 182, 54), music_rect)
draw.rect(screen, (214, 182, 54), save_rect)
draw.rect(screen, (214, 182, 54), load_rect)

# create font object
display_font = font.SysFont("kaiti", 20)

clock = time.Clock()

# lists
tools = ["pencil","eraser","brush","spray","fill","polygon","line","square","rectangle","circle","ellipse","eye drop", "text"]
undo = [canvas.copy()]
redo = []
tool_rect = []
old_pos = []
been = []
checked = []
tabs = []

# image lists
symbols = [image.load("Symbols/command insigna.png"), image.load("Symbols/medical insigna.png"), image.load("Symbols/operations insigna.png"),
           image.load("Symbols/science insigna.png"), image.load("Symbols/united federation of planets.png"), image.load("Starship/starship 1.png"),
           image.load("Starship/starship 2.png"), image.load("Starship/starship 3.png")]

stamp_display = [image.load("Symbols/command insigna.png"),image.load("Symbols/medical insigna.png"),image.load("Symbols/operations insigna.png"),
                image.load("Symbols/science insigna.png"),image.load("Symbols/united federation of planets.png"),image.load("Starship/starship 1.png"),
                image.load("Starship/starship 2.png"),image.load("Starship/starship 3.png")]

tool_images = [image.load("tool icon/pencil icon.png"), image.load("tool icon/eraser icon.png"), image.load("tool icon/brush icon.png"), image.load("tool icon/spray icon.png"),
               image.load("tool icon/fill icon.png"), image.load("tool icon/polygon icon.png"), image.load("tool icon/eye drop icon.png"), image.load("tool icon/clear icon.png"),
               image.load("tool icon/cut icon.png"), image.load("tool icon/load icon.png"), image.load("tool icon/save icon.png"), image.load("tool icon/text icon.png"), 
               image.load("tool icon/tool tab icon.png"), image.load("tool icon/stamp tab icon.png"), image.load("tool icon/undo icon.png"), image.load("tool icon/redo icon.png"),
               image.load("tool icon/play icon.png")]

# tool descriptions
description = ["Pencil: Take notes on any new planets", "Eraser: Blast away your mistakes", "Brush: Paint with a brush", "Spray: Spray can tool", "Fill: Click to fill closed areas", 
               "Polygon: Right click to draw points, left to connect", "Line: Draw straight lines", "Square: Drag to draw squares", "Rectangle: Drag to draw rectangles",
               "Circle: Drag to draw circles", "Ellipse: Draw oval shapes", "Eye Drop: Select any colour from the canvas", "Text: Click to start typing, press enter when done"]


for i in range(len(symbols)-1):
    transform.scale(symbols[i],(70,100))

# Create Rects for images
symbol_rect = [Rect(10, 10, 70, 100), Rect(90, 10, 70, 100), Rect(10, 120, 70, 100), Rect(90, 120, 70, 100), 
               Rect(10, 230, 70, 51), Rect(90, 230, 112, 68), Rect(10, 340, 100, 64), Rect(90, 340, 112, 68)]

# initialize variables
tool = tools[0]
brush_size = 1
brush_colour = (0,0,0)
can_off_x = 383
can_off_y = 80
filled = True
selected_tab = "basic tools"
music = True
stamp = "command"
stamp_num = 0
text = ""
typing = False
effect = "blur"
copy = canvas.copy()

# create tool Rects
for i in range(5):
    for j in range(3):
        tool_rect.append(Rect(10 + 70 * j, 70 * i, 60, 60))

# create tab Rects
for i in range(2):
    tabs.append(Rect(10+70*i, 10, 60, 60))

# Draw undo/redo/play/clear images
screen.blit(tool_images[7], (180, 545))
screen.blit(tool_images[16], (180, 600))
screen.blit(tool_images[14], (125, 545))
screen.blit(tool_images[15], (125, 600))

running = True

#---------------------------------------------------------------------------------------------------------------------------------------------------
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            init_x,init_y = mouse.get_pos()  # used in rectengle type tools to find topleft corner

            if can_rect.collidepoint((mx,my)):  # set redo blank if the user clicks on the canvas
                redo = []

            if e.button == 4:
                brush_size += 1  # increase brush size when user scrolls up

            if e.button == 5:
                brush_size -= 1  # increase brush size when user scrolls up

            #-------------Tools with MOUSEDOWN---------------------------
            if can_rect.collidepoint((mx,my)) and tool == "polygon" and e.button == 1:
                been = polygonPoints(canvas, can_x, can_y, brush_size, brush_colour, been)  # add the points of a polygon to a list

            if e.button == 4 and selected_tab == "stamps":
                try:
                    # Increase image size when scroll up
                    display_image = transform.scale(symbols[stamp_num], (int(symbols[stamp_num].get_width() + brush_size * 5), int(symbols[stamp_num].get_height() + brush_size * 5)))
                    screen.blit(copy, (can_off_x, can_off_y))
                except Exception:
                    pass
            elif e.button == 5 and selected_tab == "stamps":
                try:
                    # Decrease image size when scroll down
                    display_image = transform.scale(symbols[stamp_num], (int(symbols[stamp_num].get_width() - brush_size * 5), int(symbols[stamp_num].get_height() - brush_size * 5)))
                    screen.blit(copy, (can_off_x, can_off_y))
                except Exception:
                    pass

            elif e.button == 1 and selected_tab == "stamps":
                # Draw image to canvas when user clicks
                canvas.blit(display_image,(can_x-display_image.get_width()//2,can_y-display_image.get_height()//2))

            #-----------------------undo, redo, clear-------------------------------------
            if clear_rect.collidepoint((mx,my)):  # clear canvas
                canvas.fill((255,255,255))

            if undo_rect.collidepoint((mx,my)) and len(undo_rect) > 1:  # undo
                try:
                    screen.blit(undo[-2],(can_off_x,can_off_y))
                    redo.append(undo[-1])
                    del undo[-1]
                except Exception:
                    pass

            if redo_rect.collidepoint((mx,my)) and len(redo_rect) > 0:  # redo
                try:
                    screen.blit(redo[-1],(can_off_x,can_off_y))
                    undo.append(redo[-1])
                    del redo[-1]
                except Exception:
                    pass

            #--------------toggle music----------------------------------
            if music and music_rect.collidepoint((mx,my)):  # turn music off
                music = False
                mixer.music.fadeout(100)
                draw.rect(screen, (255, 0, 0), music_rect)
            elif music == False and music_rect.collidepoint((mx,my)):  # turn music on
                music = True
                mixer.music.play(-1,0.0)
                draw.rect(screen, (214, 182, 54), music_rect)

            #----------------save annd load-----------------------------
            if save_rect.collidepoint((mx,my)) and e.button == 1:
                fileName = asksaveasfilename(parent=root,title="Save the image as...")
                if fileName[len(fileName)-1:len(fileName)-5:-1] != ".png" or fileName[len(fileName)-1:len(fileName)-5:-1] != ".jpg":  # Check if file has propor extension if not add .png
                    fileName += ".png"
                image.save(canvas, fileName)

            if load_rect.collidepoint((mx,my)) and e.button == 1:
                fileName = askopenfilename(parent=root,title="Open Image:")
                screen.blit(image.load(fileName), (can_off_x, can_off_y))

        if e.type == MOUSEBUTTONUP and can_rect.collidepoint((mx,my)):
            copy = canvas.copy()
            undo.append(copy)


        if tool == "text":
            if e.type == MOUSEBUTTONDOWN and e.button == 1 and can_rect.collidepoint((mx,my)):
                canvas_text = canvas.copy()
                text_pos = (can_x, can_y)
                typing = True
            if typing:
                if e.type == MOUSEBUTTONDOWN:
                    screen.blit(copy, (can_off_x, can_off_y))
                if e.type == KEYDOWN:
                    if e.key == K_BACKSPACE:
                        text = text[:-1]
                    elif e.key == K_RETURN:
                        typing = False
                    elif  e.unicode:
                        text += e.unicode
            elif typing == False:
                text = ""
                
        # Limit brush size to a range of 5-100
        if brush_size <= 5:
            brush_size = 5
        if brush_size >= 100:
            brush_size = 100
            
    mx,my = mouse.get_pos()

    can_x = mx-can_off_x  # x, y of mouse on canvas
    can_y = my-can_off_y

    tool_area_x = mx
    tool_area_y = my-80

    mb = mouse.get_pressed()

    texttool_font = font.SysFont("kaiti", int(brush_size))  # font for the text tool

    # display brush size and tool information
    discrip_area.fill((0, 0, 0))
    display_size = display_font.render(str(int(brush_size)), True, (214, 182, 54))
    display_text = display_font.render(description[tools.index(tool)], True, (214, 182, 54))
    discrip_area.blit(display_text, (0, 40))
    discrip_area.blit(display_size, (0, 20))

    #--------------tools do stuff--------------------------------------
    if can_rect.collidepoint((mx,my)):
        if mb[0] == 1 and tool == "pencil":
            pencil(screen, canvas, old_pos, can_x, can_y, brush_colour)

        if mb[0] == 1 and tool == "eraser":
            eraser(screen, canvas, old_pos, can_x, can_y, brush_size)

        if mb[0] == 1 and tool == "brush":
            brush(screen, canvas, old_pos, can_x, can_y, brush_size, brush_colour)

        if mb[0] == 1 and tool == "spray":
            spray(canvas, can_x, can_y, brush_size, brush_colour)

        if mb[0] == 1 and tool == "fill":
            flood_fill(screen, canvas, can_rect, mouse.get_pos(), mx, my, brush_size, brush_colour)

        if mb[2] == 1 and tool == "polygon":
            polygonShape(canvas, been, brush_size, brush_colour)
            been = []

        if mb[0] == 1 and tool == "line":
            line(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, can_x, can_y, brush_size, brush_colour)

        if mb[0] == 1 and tool == "square":
            square(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, brush_size, brush_colour, filled)

        if mb[0] == 1 and tool == "rectangle":
            rectangle(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, brush_size, brush_colour, filled)

        if mb[0] == 1 and tool == "circle":
            circle(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, brush_size, brush_colour, filled)

        if mb[0] == 1 and tool == "ellipse":
            ellipse(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, can_x, can_y, brush_size, brush_colour, filled)

        if mb[0] == 1 and tool == "eye drop":
            brush_colour = eyeDrop(canvas, can_x, can_y)

        if tool == "text" and typing:
            typing_text_pic = texttool_font.render(text, True, brush_colour)
            canvas.blit(canvas_text,(0,0))
            canvas.blit(typing_text_pic, text_pos)

        if 1 not in mb:
            old_pos = []

    #--------------------display stamps-------------------------------------------------
    if selected_tab == "stamps":
        if can_rect.collidepoint((mx,my)):
            screen.blit(copy, (can_off_x,can_off_y))
            canvas.blit(display_image,(can_x-width//2,can_y-height//2))  # center image on mouse
        else:
            screen.blit(copy, (can_off_x,can_off_y))

        width = symbols[stamp_num].get_width()
        height = symbols[stamp_num].get_height()

    #---------------------------colour change-------------------------------------------
    draw.rect(screen, brush_colour, (10, 540, 100, 100))
    if colour_area.collidepoint((mx, my)) and mb[0] == 1:
        brush_colour = screen.get_at((mx, my))
        screen.blit(colour_palette, (10, 650))
        draw.circle(screen, (0, 0, 0), (mx, my), 3, 1)


    if can_rect.collidepoint((mx,my)) == False:  # things to do off of the canvas

        #--------------display tabs----------------------------------
        if selected_tab == "basic tools":
            draw.rect(screen, (0, 255, 0), tabs[0])
        else:
            draw.rect(screen, (214, 182, 54), tabs[0])

        if selected_tab == "stamps":
            draw.rect(screen, (0, 255, 0), tabs[1])
        else:
            draw.rect(screen, (214, 182, 54), tabs[1])

        #--------------display basic tools---------------------------
        if selected_tab == "basic tools":
            if tool == "pencil":
                draw.rect(tool_area, (0, 255, 0), tool_rect[0])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[0])

            if tool == "eraser":
                draw.rect(tool_area, (0, 255, 0), tool_rect[1])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[1])

            if tool == "brush":
                draw.rect(tool_area, (0, 255, 0), tool_rect[2])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[2])

            if tool == "spray":
                draw.rect(tool_area, (0, 255, 0), tool_rect[3])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[3])

            if tool == "fill":
                draw.rect(tool_area, (0, 255, 0), tool_rect[4])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[4])

            if tool == "polygon":
                draw.rect(tool_area, (0, 255, 0), tool_rect[5])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[5])

            if tool == "line":
                draw.rect(tool_area, (0, 255, 0), tool_rect[6])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[6])

            if tool == "square":
                draw.rect(tool_area, (0, 255, 0), tool_rect[7])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[7])

            if tool == "rectangle":
                draw.rect(tool_area, (0, 255, 0), tool_rect[8])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[8])

            if tool == "circle":
                draw.rect(tool_area, (0, 255, 0), tool_rect[9])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[9])

            if tool == "ellipse":
                draw.rect(tool_area, (0, 255, 0), tool_rect[10])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[10])

            if tool == "eye drop":
                draw.rect(tool_area, (0, 255, 0), tool_rect[11])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[11])

            if tool == "text":
                draw.rect(tool_area, (0, 255, 0), tool_rect[12])
            else:
                draw.rect(tool_area, (214, 182, 54), tool_rect[12])

            if filled == False:
                draw.rect(tool_area, (214, 182, 54), tool_rect[13])
                draw.rect(tool_area, (0, 255, 0), tool_rect[14])
            if filled:
                draw.rect(tool_area, (214, 182, 54), tool_rect[14])
                draw.rect(tool_area, (0, 255, 0), tool_rect[13])

            # draw icons
            tool_area.blit(tool_images[0], (16, 4))
            tool_area.blit(tool_images[1], (86, 4))
            tool_area.blit(tool_images[2], (156, 4))
            tool_area.blit(tool_images[3], (16, 74))
            tool_area.blit(tool_images[4], (86, 74))
            tool_area.blit(tool_images[5], (156, 74))
            tool_area.blit(tool_images[6], (156, 215))
            tool_area.blit(tool_images[11], (16, 285))

            screen.blit(tool_images[10], (1221, 85))
            screen.blit(tool_images[9], (1221, 155))

            draw.line(tool_area, (0, 0, 0), (16, 145), (64, 193), 2)
            draw.rect(tool_area, (0, 0, 0), (86, 145, 48, 48))
            draw.rect(tool_area, (0, 0, 0), (156, 150, 48, 38))
            draw.ellipse(tool_area, (0, 0, 0), (16, 215, 48, 48))
            draw.ellipse(tool_area, (0, 0, 0), (86, 220, 48, 38))
            draw.rect(tool_area, (0, 0, 0), (86, 285, 48, 48))
            draw.rect(tool_area, (0, 0, 0), (156, 285, 48, 48), 3)


        #-------------------tool change-----------------------------------------------------
        if mb[0] == 1 and selected_tab == "basic tools":
            if tool_rect[0].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[0]
            if tool_rect[1].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[1]
            if tool_rect[2].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[2]
            if tool_rect[3].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[3]
            if tool_rect[4].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[4]
            if tool_rect[5].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[5]
            if tool_rect[6].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[6]
            if tool_rect[7].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[7]
            if tool_rect[8].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[8]
            if tool_rect[9].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[9]
            if tool_rect[10].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[10]
            if tool_rect[11].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[11]
            if tool_rect[12].collidepoint((tool_area_x, tool_area_y)):
                tool = tools[12]               
            if tool_rect[13].collidepoint((tool_area_x, tool_area_y)):
                filled = True
            if tool_rect[14].collidepoint((tool_area_x, tool_area_y)):
                filled = False

        #------------------stamp change-----------------------------------------------------
        if selected_tab == "stamps":
            tool_area.blit(stamp_display[0],(10,10))
            tool_area.blit(stamp_display[1],(90,10))
            tool_area.blit(stamp_display[2],(10,120))
            tool_area.blit(stamp_display[3],(90,120))
            tool_area.blit(stamp_display[4],(10,230))
            tool_area.blit(transform.scale(stamp_display[5], (112, 68)), (90, 230))
            tool_area.blit(transform.scale(stamp_display[6], (100, 64)), (10, 340))
            tool_area.blit(transform.scale(stamp_display[7], (112, 68)), (90, 340))

            for i in range(len(symbol_rect)):
                if symbol_rect[i].collidepoint((tool_area_x,tool_area_y)) and mb[0] == 1:
                    stamp_num = i

            display_image = transform.scale(symbols[stamp_num], (symbols[stamp_num].get_width(), symbols[stamp_num].get_height()))

        # display tab icons
        screen.blit(tool_images[12], (12, 12))
        screen.blit(tool_images[13], (82, 12))

    #-------------------tab change------------------------------------------------------
    if mb[0] == 1:
        if tabs[0].collidepoint((mx,my)):
            tool_area.fill((0,0,0))
            selected_tab = "basic tools"
        if tabs[1].collidepoint((mx,my)):
            tool_area.fill((0,0,0))
            selected_tab = "stamps"

    clock.tick(60)
    display.flip()

mixer.quit()
quit()
