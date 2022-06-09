import numpy as np
from math import ceil
from ezomero import rois
import ezomero as ez
import time

def nearestMultipleOf(tile_dim, col, row) -> tuple:
    return int(ceil(col/tile_dim)), int(ceil(row/tile_dim))

def roiTiler(tile_dim, row, col,) -> list:
    rect_list = []
    for y in range(0, row):
        for x in range(0, col):
            rect_list.append(rois.Rectangle(x*tile_dim, y*tile_dim, tile_dim, tile_dim, label="row: %d col: %d" % (y, x)))
    return rect_list

#get tile segment of image
def get_tile(pixels, row, col, tile_dim) -> np.array:
    return pixels.getTile(0,0,0,(col*tile_dim,row*tile_dim,tile_dim,tile_dim))

#get all pixel objects from project images
def getProjectPixels(conn, id_list) -> list:
    pixellist = []
    for id in id_list:
        image = conn.getObject("Image", id)
        pixellist.append(image.getPrimaryPixels())
    return pixellist

#get all images from project
def getProjectImages(conn, id_list) -> list:
    imagelist = []
    for id in id_list:
        imagelist.append(conn.getObject("Image", id))
    return imagelist

#buid a dict of all images with required rows and columns 
def getDimensionMap(id_list, tile_dim) -> dict:
    imagedict = {}
    for id in id_list:
        col, row = nearestMultipleOf(tile_dim, id.getSizeX(), id.getSizeY())
        key_val = {id.getId():(col,row)}
        imagedict.update(key_val)
    return imagedict
    
def breakUpImage(conn, imagedict, tile_dim):
    for key, value in imagedict.items():
        image = conn.getObject("Image", key)
        for y in range(value[1]):
            for x in range(value[0]):
                tile = get_tile(image.getPrimaryPixels(), x, y, tile_dim)
                tile = np.expand_dims(tile, axis=(2,3,4))
                ez.post_image(conn, tile, "%s row: %d col: %d" % (key, y, x), key, channel_list=[0] )
