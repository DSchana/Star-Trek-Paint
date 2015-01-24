 # real_paint.py

from pygame import *
from random import *
from math import *
from tools import *
init()

'''
TODO:
* resize stamps
* fix ellipse
* blur
* invert
* greyshift
* greyscale near colour palette
* crop
* layers
* text tool
'''

screen = display.set_mode((1280, 900))
display.set_caption("Star Trek Paint")

colour_palette = image.load("colour_palette.jpg")
star_trek_logo = image.load("title.jpg")
star_trek_logo = transform.smoothscale(star_trek_logo,(218,100))

# initialize screen
screen.fill((0, 0, 0))

screen.blit(colour_palette, (10, 650))
screen.blit(star_trek_logo,(683,5))

mixer.music.load("Star Trek.mp3")
mixer.music.play(-2,0.0)

can_rect = Rect(383, 80, 828, 550)
tool_area_rect = Rect(0, 80, 383, 390)
undo_rect = Rect(120, 540, 45, 45)
redo_rect = Rect(120, 595, 45, 45)
clear_rect = Rect(175, 540, 45, 45)
music_rect = Rect(175, 595, 45, 45)
colour_area = Rect(10, 650, 200, 200)
tab_rect = Rect(0, 0, 383, 80)
new_layer = Rect(1151, 645, 60, 60)
delete_layer = Rect(1151, 715, 60, 60)

canvas = screen.subsurface(can_rect)
tool_area = screen.subsurface(tool_area_rect)
canvas.fill((255, 255, 255))

draw.rect(screen, (214, 182, 54), undo_rect)
draw.rect(screen, (214, 182, 54), redo_rect)
draw.rect(screen, (214, 182, 54), clear_rect)
draw.rect(screen, (214, 182, 54), music_rect)
draw.rect(screen, (214, 182, 54), new_layer)
draw.rect(screen, (214, 182, 54), delete_layer)

clock = time.Clock()

# lists
tools = ["pencil","eraser","brush","spray","fill","polygon","line","square","rectangle","circle","ellipse","eye drop", "select"]
undo = []
redo = []
tool_rect = []
old_pos = []
been = []
checked = []
tabs = []
effect_rects = []
layers = [screen.subsurface(can_rect)]  # holds all layers added by user

# image lists
symbols = [image.load("Symbols/command insigna.png"),image.load("Symbols/medical insigna.png"),image.load("Symbols/operations insigna.png"),
           image.load("Symbols/science insigna.png"),image.load("Symbols/united federation of planets.png"),image.load("Starship/starship 1.png"),
           image.load("Starship/starship 2.png"),image.load("Starship/starship 3.png")]
stamp_display = [image.load("Symbols/command insigna.png"),image.load("Symbols/medical insigna.png"),image.load("Symbols/operations insigna.png"),
                image.load("Symbols/science insigna.png"),image.load("Symbols/united federation of planets.png"),image.load("Starship/starship 1.png"),
                image.load("Starship/starship 2.png"),image.load("Starship/starship 3.png")]

tool_images = [image.load("tool icon/pencil icon.png"), image.load("tool icon/eraser icon.png"), image.load("tool icon/brush icon.png"), image.load("tool icon/spray icon.png"),
			   image.load("tool icon/fill icon.png"), image.load("tool icon/polygon icon.png"), image.load("tool icon/eye drop icon.png"), image.load("tool icon/clear icon.png"),
			   image.load("tool icon/cut icon.png"), image.load("tool icon/load icon.png"), image.load("tool icon/save icon.png"), image.load("tool icon/text icon.png"), 
			   image.load("tool icon/tool tab icon.png"), image.load("tool icon/stamp tab icon.png"), image.load("tool icon/undo icon.png"), image.load("tool icon/redo icon.png")]

for i in range(len(symbols)-1):
    transform.scale(symbols[i],(70,100))

# Create Rects for images
symbol_rect = [Rect(10,10,70,100),Rect(90,10,70,100),Rect(170,10,70,100),Rect(10,120,70,100),Rect(90,120,100,100)]

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
current_layer = layers[0]
#star_trek_font = font.SysFont("Comic Sans MS",20)

# create tool Rects
for i in range(5):
    for j in range(3):
        tool_rect.append(Rect(10 + 70 * j, 70 * i, 60, 60))

# create effect Rects
for i in range(3):
    effect_rects.append(Rect(10, 70 * i, 150, 80))

# create tab Rects
for i in range(4):
    tabs.append(Rect(10+70*i,10,60,60))

screen.blit(tool_images[7], (180, 545))
screen.blit(tool_images[14], (125, 545))
screen.blit(tool_images[15], (125, 600))

running = True

#---------------------------------------------------------------------------------------------------------------------------------------------------
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            copy = canvas.copy()
            init_x,init_y = mouse.get_pos()
            undo.append(copy)

            if e.button == 4 and selected_tab == "basic tools":
                brush_size += 0.7
            if e.button == 5 and selected_tab == "basic tools":
                brush_size -= 0.7

            #-------------Tools with MOUSEDOWN---------------------------
            if can_rect.collidepoint((mx,my)) and tool == "polygon" and e.button == 1:
                been = polygonPoints(canvas, can_x, can_y, brush_size, brush_colour, been)

            if e.button == 4 and selected_tab == "stamps":
                display_image = transform.smoothscale(symbols[stamp_num], (int(symbols[stamp_num].get_width() + brush_size * 5), int(symbols[stamp_num].get_height() + brush_size * 5)))
                screen.blit(copy, (can_off_x, can_off_y))
            elif e.button == 5 and selected_tab == "stamps":
                display_image = transform.smoothscale(symbols[stamp_num], (int(symbols[stamp_num].get_width() - brush_size * 5), int(symbols[stamp_num].get_height() - brush_size * 5)))
                screen.blit(copy, (can_off_x, can_off_y))
            elif e.button == 1 and selected_tab == "stamps":
                canvas.blit(display_image,(can_x-display_image.get_width()//2,can_y-display_image.get_height()//2))

            #-----------------------undo, redo, clear-------------------------------------
            if clear_rect.collidepoint((mx,my)):
                canvas.fill((255,255,255))
            if undo_rect.collidepoint((mx,my)) and len(undo_rect) > 1:
                screen.blit(undo[len(undo)-1],(can_off_x,can_off_y))
                redo.append(undo[len(undo)-1])
                del undo[len(undo)-1]
            if redo_rect.collidepoint((mx,my)) and len(redo_rect) > 0:
                screen.blit(redo[len(redo)-1],(can_off_x,can_off_y))
                undo.append(redo[len(redo)-1])
                del redo[len(redo)-1]

            #--------------toggle music----------------------------------
            if music and music_rect.collidepoint((mx,my)):
                music = False
                mixer.music.fadeout(100)
                draw.rect(screen, (255, 0, 0), music_rect)
            elif music == False and music_rect.collidepoint((mx,my)):
                music = True
                mixer.music.play(-1,0.0)
                draw.rect(screen, (214, 182, 54), music_rect)
                
        # Limit brush size to a range of 5-100
        if brush_size < 5:
            brush_size = 5
        if brush_size>100:
            brush_size = 100
            
    mx,my = mouse.get_pos()

    can_x = mx-can_off_x
    can_y = my-can_off_y

    tool_area_x = mx
    tool_area_y = my-80

    mb = mouse.get_pressed()

    #--------------do stuff--------------------------------------
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
	        ellipse(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, brush_size, brush_colour, filled)

	    if mb[0] == 1 and tool == "eye drop":
	        brush_colour = eyeDrop(canvas, can_x, can_y)

	    '''
	    if tool == "select":
	    	if mb[0] == 1 and copied == False:
	    		selected_copy = selectCopy(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, mb, brush_size, brush_colour)
	    	if 1 not in mb and copied == False:
	    		copied = True
	    '''

	    if 1 not in mb:
	        old_pos = []

    #--------------------display stamps-------------------------------------------------
    if selected_tab == "stamps":
        if can_rect.collidepoint((mx,my)):
            screen.blit(copy, (can_off_x,can_off_y))
            canvas.blit(display_image,(can_x-width//2,can_y-height//2))
        else:
            screen.blit(copy, (can_off_x,can_off_y))

        width = symbols[stamp_num].get_width()
        height = symbols[stamp_num].get_height()

        

    if tool_area_rect.collidepoint((mx,my)) or tab_rect.collidepoint((mx,my)):
        #--------------display tabs----------------------------------
        if selected_tab == "basic tools":
            draw.rect(screen, (0, 255, 0), tabs[0])
        else:
            draw.rect(screen, (214, 182, 54), tabs[0])

        if selected_tab == "stamps":
            draw.rect(screen, (0, 255, 0), tabs[1])
        else:
            draw.rect(screen, (214, 182, 54), tabs[1])

        if selected_tab == "effect":
            draw.rect(screen, (0, 255, 0), tabs[2])
        else:
            draw.rect(screen, (214, 183, 54), tabs[2])

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

            if tool == "select":
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

            draw.line(tool_area, (0, 0, 0), (16, 145), (64, 193), 2)
            draw.rect(tool_area, (0, 0, 0), (86, 145, 48, 48))
            draw.rect(tool_area, (0, 0, 0), (156, 150, 48, 38))
            draw.ellipse(tool_area, (0, 0, 0), (16, 215, 48, 48))
            draw.ellipse(tool_area, (0, 0, 0), (86, 220, 48, 38))
            draw.rect(tool_area, (0, 0, 0), (86, 285, 48, 48))
            draw.rect(tool_area, (0, 0, 0), (156, 285, 48, 48), 3)

        #------------------display effects--------------------------------------------------
        if selected_tab == "effects":
            if effect == "blur":
                draw.rect(tool_area, (0, 255, 0), effect_rects[0])
            else:
                draw.rect(tool_area, (214, 182, 54), effect_rects[0])

            if effect == "invert":
                draw.rect(tool_area, (0, 255, 0), effect_rects[1])
            else:
                draw.rect(tool_area, (214, 182, 54), effect_rects[1])

            if effect == "gray":
                draw.rect(tool_area, (0, 255, 0), effect_rects[2])
            else:
                draw.rect(tool_area, (214, 182, 54), effect_rects[2])


        #--------------------display status-------------------------------------------------
     #   disp_tool = star_trek_font.render(tool, True, (214, 182, 54))
     #   screen.blit(disp_tool,(10,430))


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

        print(tool,mx,my)

        #------------------stamp change-----------------------------------------------------
        if selected_tab == "stamps":
            tool_area.blit(stamp_display[0],(10,10))
            tool_area.blit(stamp_display[1],(90,10))
            tool_area.blit(stamp_display[2],(170,10))
            tool_area.blit(stamp_display[3],(10,120))
            tool_area.blit(stamp_display[4],(90,120))

            for i in range(len(symbol_rect)):
                if symbol_rect[i].collidepoint((tool_area_x,tool_area_y)) and mb[0] == 1:
                    stamp_num = i

            display_image = transform.smoothscale(symbols[stamp_num], (symbols[stamp_num].get_width(), symbols[stamp_num].get_height()))

        #------------------effect change----------------------------------------------------
        if mb[0] == 1 and selected_tab == "effect_rects":
            if effect_rects[0].collidepoint((mx,my)):
                effect = "blur"
            if effect_rects[1].collidepoint((mx,my)):
                effect = "invert"
            if effect_rects[2].collidepoint((mx,my)):
                effect = "gray"

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
        if tabs[2].collidepoint((mx,my)):
            tool_area.fill((0,0,0))
            selected_tab = "effect"

    #---------------------------colour change-------------------------------------------
    draw.rect(screen, (255,255,255), (10, 540, 100, 100))
    draw.circle(screen,brush_colour,(60,590),int(brush_size/2))
    if colour_area.collidepoint((mx, my)) and mb[0] == 1:
        brush_colour = screen.get_at((mx, my))
        screen.blit(colour_palette, (10, 650))
        draw.circle(screen, (0, 0, 0), (mx, my), 3, 1)


    display.set_caption("Star Trek Paint fps: " + str(round(clock.get_fps(),2)))
    clock.tick(60)
    display.flip()

#font.quit()
mixer.quit()
quit()
