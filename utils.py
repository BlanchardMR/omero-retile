import numpy as np
from math import ceil
from ezomero import rois

def nearestMultipleOf(tile_dim, dim1, dim2) -> tuple:
    return int(ceil(dim1/tile_dim)), int(ceil(dim2/tile_dim))

def roiTiler(tile_dim, row, col,) -> list:
    rect_list = []
    for y in range(0, row):
        for x in range(0, col):
            rect_list.append(rois.Rectangle(x*tile_dim, y*tile_dim, tile_dim, tile_dim, label="row: %d col: %d" % (y, x)))
    return rect_list

def getTile(pixels, row, col, tile_dim) -> np.array:
    return pixels.getTile(0,0,0,(col*tile_dim,row*tile_dim,tile_dim,tile_dim))
