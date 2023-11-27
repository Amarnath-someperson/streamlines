from PIL import Image
import math

# consider all particles of volume 1, mass 1, to generate a pressure field in the system

# the pressure exerted by one volume of water due to its velocity on a body is ρv²/2

# TODO: to define a function that can detect pressure changes due to the presence of a rigid body in the flow path of the fluid
# note that pressure always acts normally on the surface


# BEGINNER EXAMPLE : A RIGID CIRCLE
def circle():
    pressure_field = {}
    radius = 40
    PRESSURE_INITIAL = 0
    PRESSURE_SURFACE = 9999 # maximum pressure exerted on the surface (magnitude)
    width, height = 2000, 2000
    center_x, center_y = width//2, height//2
    
    PRESSURE_CHANGE_X = PRESSURE_SURFACE/(center_x-radius) # from center, the pressure change
    PRESSURE_CHANGE_Y = PRESSURE_SURFACE/(center_y-radius) # from center, consider a square image for now
    im = Image.new('RGB',(width, height))


    # The range of pressure is [-10000, 10000] as in percentage
    # Consider a circle with center at the middle of the image, with radius 20px, wherein its inside has a pressure 1000 (arbitrary unit)
    
    for x in range(-radius, radius, 1):
        for y in range(-radius, radius, 1):
            if int(math.sqrt(x*x + y*y)) <= radius:
                pressure_field[(center_x + x, center_y + y)] =  (175, 180, 134)
    
    for x in range(width):
        for y in range(height):
            # (center_x-x)^2 + (center_y-y)^2 = radius^2
            if (((center_x-x)**2 + (center_y-y)**2) >= radius**2):
                
                distance = math.sqrt((abs(center_x-x)**2 + (center_y-y) ** 2)) - radius
                angle = 0
                try:
                    angle = math.atan((center_x-x)/(center_y-y))
                except ZeroDivisionError:
                    angle = math.inf
                if angle != math.inf:
                    y_dist = distance * math.sin(angle)
                    x_dist = distance * math.cos(angle)
                    
                    # pressure_field[(x, y)] = (PRESSURE_SURFACE- (PRESSURE_CHANGE_X * (center_x -x)), PRESSURE_SURFACE-(PRESSURE_CHANGE_Y * (center_y-y)))
                    pressure_field[((x, y))] = (0, int(255/10000 * math.sqrt((PRESSURE_SURFACE - (PRESSURE_CHANGE_X * (math.cos(angle) * (center_x-x_dist))))**2 + (PRESSURE_SURFACE - (PRESSURE_CHANGE_Y * (math.sin(angle) * (center_y-y_dist))))**2)), 0)
                else:
                    pressure_field[((x, y))] = (0, int(255/10000 * (PRESSURE_SURFACE - (PRESSURE_CHANGE_Y * (center_y-y_dist)))), 0)
                
        
    # TODO: Greatly improve efficiency
    for i in pressure_field:
        #im.putpixel(i, (int(255/10000 * pressure_field[i][0]), 0, int(255/10000 * pressure_field[i][1])))
        im.putpixel(i, pressure_field[i])
        
    #im = im.resize((width // 2, height // 2), resample=Image.LANCZOS)
    im.save('out.png')
    
    
if __name__ == "__main__":
    circle()