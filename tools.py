# tools.py

from pygame import *
from math import *
from random import *

def pencil(screen, canvas, old_pos, x, y, colour):
    old_pos.append((x,y))
    if len(old_pos)>2:
        del old_pos[0]
        draw.line(canvas,colour,old_pos[0],(x,y),1)

def eraser(screen, canvas, old_pos, x, y, size):
    old_pos.append((x,y))
    if len(old_pos)>2:
        del old_pos[0]
        draw.line(canvas,(255,255,255),old_pos[0],(x,y),int(size))
        draw.circle(canvas,(255,255,255),(x,y),int(size/2))

def brush(screen, canvas, old_pos, x, y, size, colour):
    old_pos.append((x,y))
    if len(old_pos)>2:
        del old_pos[0]
        draw.line(canvas,colour,old_pos[0],(x,y),int(size))
        draw.circle(canvas,colour,(x,y),int(size/2))

def spray(canvas, x, y, size, colour):
    for i in range(15):
        spray_x = x - randint(-(int(size/2)), int(size/2))  # get posible x, y poits to draw
        spray_y = y - randint(-(int(size/2)), int(size/2))
        radius = int(size/2)
        if sqrt((spray_x-x)**2 + (spray_y-y)**2) <= radius:  # check if the points are within the radius of the circle
            canvas.set_at((spray_x, spray_y), colour)

def flood_fill(screen, canvas, can_rect, mpos, x, y, size, colour):
    loc = [mpos]
    screen.set_clip(can_rect)
    sel_col = tuple(screen.get_at((x,y)))
    if sel_col != colour:
        while len(loc) > 0:
            cx, cy = loc.pop()
            if screen.get_at((cx, cy)) == sel_col and can_rect.collidepoint((cx, cy)):
                screen.set_at((cx, cy), colour)  # fill current point
                loc.append((cx+1, cy))  # check the points all around the current point
                loc.append((cx-1, cy))
                loc.append((cx, cy+1))
                loc.append((cx, cy-1))

def polygonPoints(canvas, x, y, size, colour, been):
    been.append((x,y))
    draw.circle(canvas,colour,(x,y),int(size/2))

    return been

def polygonShape(canvas, been, size, colour):
    if len(been)>1:
        for i in range(len(been)-1):
            draw.line(canvas,colour,been[i],been[i+1],int(size))
        draw.line(canvas,colour,been[0],been[len(been)-1],int(size))

def line(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, x, y, size, colour):
    screen.blit(copy,(can_off_x,can_off_y))
    draw.line(canvas,colour,(x,y),(init_x-can_off_x,init_y-can_off_y),int(size))
    draw.circle(canvas,colour,(init_x-can_off_x,init_y-can_off_y),int(size/2))
    draw.circle(canvas,colour,(x,y),int(size/2))

def square(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, size, colour, filled):
    screen.blit(copy,(can_off_x,can_off_y))
    if filled == False:
        if init_x-mx>=init_y-my:
            draw.rect(canvas,colour,(init_x-can_off_x,init_y-can_off_y,-(init_x-mx),-(init_x-mx)),int(size))

            # draw corner rectangles to complete shape
            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2),init_y-can_off_y-int(size/2),int(size),int(size)))
            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2)+(mx-init_x),init_y-can_off_y-int(size/2)+(mx-init_x),int(size),int(size)))
            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2)+(mx-init_x),init_y-can_off_y-int(size/2),int(size),int(size)))
            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2),init_y-can_off_y-int(size/2)+(mx-init_x),int(size),int(size)))
        elif init_x-mx<=init_y-my:
            draw.rect(canvas,colour,(init_x-can_off_x,init_y-can_off_y,-(init_y-my),-(init_y-my)),int(size))

            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2),init_y-can_off_y-int(size/2),int(size),int(size)))
            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2)+(my-init_y),init_y-can_off_y-int(size/2)+(my-init_y),int(size),int(size)))
            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2)+(my-init_y),init_y-can_off_y-int(size/2),int(size),int(size)))
            draw.rect(canvas,colour,(init_x-can_off_x-int(size/2),init_y-can_off_y-int(size/2)+(my-init_y),int(size),int(size)))

    if filled:
        if init_x-mx>=init_y-my:
            draw.rect(canvas,colour,(init_x-can_off_x,init_y-can_off_y,-(init_x-mx),-(init_x-mx)))

        elif init_x-mx<=init_y-my:
            draw.rect(canvas,colour,(init_x-can_off_x,init_y-can_off_y,-(init_y-my),-(init_y-my)))

def rectangle(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, size, colour, filled):
    screen.blit(copy,(can_off_x,can_off_y))
    if filled == False:
        draw.rect(canvas,colour,(init_x-can_off_x,init_y-can_off_y,-(init_x-mx),-(init_y-my)),int(size))

        draw.rect(canvas, colour, (init_x-can_off_x-int(size/2), init_y-can_off_y-int(size/2), int(size), int(size)))
        draw.rect(canvas, colour, (init_x-can_off_x-int(size/2)+(mx-init_x), init_y-can_off_y-int(size/2)+(my-init_y), int(size), int(size)))
        draw.rect(canvas, colour, (init_x-can_off_x-int(size/2)+(mx-init_x), init_y-can_off_y-int(size/2), int(size), int(size)))
        draw.rect(canvas, colour, (init_x-can_off_x-int(size/2),init_y-can_off_y-int(size/2)+(my-init_y), int(size), int(size)))
    if filled:
        screen.blit(copy,(can_off_x,can_off_y))
        draw.rect(canvas,colour,(init_x-can_off_x,init_y-can_off_y,-(init_x-mx),-(init_y-my)))

def circle(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, size, colour, filled):
    screen.blit(copy,(can_off_x,can_off_y))
    if filled == False:
        radius = sqrt((init_x-mx)**2 + (init_y-my)**2)
        if size<2:
            size = 2
        draw.circle(canvas,colour,(init_x-can_off_x,init_y-can_off_y),int(radius+size/2),int(size/2))
    if filled:
        radius = sqrt((init_x-mx)**2 + (init_y-my)**2)
        if size<2:
            size = 2
        draw.circle(canvas,colour,(init_x-can_off_x,init_y-can_off_y),int(radius+size/2))

def ellipse(screen, canvas, copy, can_off_x, can_off_y, init_x, init_y, mx, my, can_x, can_y, size, colour, filled):
    screen.blit(copy,(can_off_x,can_off_y))
    try:
        if init_x <= mx and init_y <= my:
            draw.ellipse(canvas,colour,(init_x-can_off_x,init_y-can_off_y,(mx-init_x),(my-init_y)))
        elif init_x > mx and init_y > my:
            draw.ellipse(canvas,colour,(can_x,can_y,(mx-init_x),(my-init_y)))
    except Exception:
        pass

def eyeDrop(canvas, x, y):
    colour = canvas.get_at((x,y))

    return colour