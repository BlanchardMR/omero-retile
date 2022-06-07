import numpy as np
import ezomero as ez


conn = ez.connect()
image = conn.getObject("Image", 1654601)

pixels = image.getPrimaryPixels()
d1 = int(image.getSizeX())
d2 = int(image.getSizeY())

TILE_DIMENSION = 5000

def nearestMultipleOf(tile_dim, dim1, dim2):
    return int(dim1/tile_dim), int(dim2/tile_dim)

row, col = nearestMultipleOf(TILE_DIMENSION, d1, d2)

##plane = pixels.getPlane(0,0,0)

def arrayBreak2d(tile_dim, arr, row, col):
    array_list = []
    for y in range(0, row):
        for x in range(0, col):
            if x != 0:
                array_list.append(arr[:tile_dim,:tile_dim])
            else:
                array_list.append(arr[x*tile_dim:(x+1)*tile_dim,y*tile_dim:(y+1)*tile_dim])
    return array_list

##y
#array_list = arrayBreak2d(TILE_DIMENSION, plane, row, col)

conn.close()
