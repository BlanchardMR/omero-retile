import numpy as np
from math import ceil
from ezomero import rois
import ezomero as ez
import time

def tileMultiple(tile_dim, pixel_x, pixel_y) -> tuple:
    """ Function used to calcualte the number of rows and columns in parent image
    
    Parameters
    ----------
    tile_dim : int
    pixel_x : int
    pixel_y : int

    Returns
    --------
    tuple (int x, int y) 

    """
    return int(pixel_x/tile_dim), int(pixel_y/tile_dim)

def roiTiler(tile_dim, row, col,) -> list:
    """ Function to create rectangle roi list for visual mapping of tiles in omero db
    
    Parameters
    ----------
    tile_dim : int
    row : int
    col : int

    Returns
    --------
    list(<ezomero.rois.Rectangle>) 
    """
    rect_list = []
    for y in range(0, row):
        for x in range(0, col):
            rect_list.append(rois.Rectangle(x*tile_dim, y*tile_dim, tile_dim, tile_dim, label="row: %d col: %d" % (y, x)))
    return rect_list


def get_tile(pixels, row, col, tile_dim, z=0,c=0, t=0) -> np.array:
    """ wrapper function find and return tile by col, row location at given tile dimension
    
    Parameters
    ----------
    pixels : <Omero.Pixel> ??? need to correct this
    row : int
    col : int
    tile_dim: int
    z = int
    c = int
    t = int

    Returns
    --------
    numpy.ndArray : 2 Dimensions regardless of color space
    """
    return pixels.getTile(z, c, t,(col*tile_dim,row*tile_dim,tile_dim,tile_dim))


def getProjectPixels(conn, id_list) -> list:
    """ wrapper function find and return tile by col, row location at given tile dimension
    
    Parameters
    ----------
    conn = <Blitzgateway.connection>
    id_list = [int]
    
    Returns
    --------
    list[<Omero.pixels>] ??? double check this object type
    """
    pixellist = []
    for id in id_list:
        image = conn.getObject("Image", id)
        pixellist.append(image.getPrimaryPixels())
    return pixellist

def getProjectImages(conn, id_list) -> list:
    """ builds list of all image id numbers in project
    
    Parameters
    ----------
    conn = <Blitzgateway.connection>
    id_list = [int]
    
    Returns
    --------
    lis[int]
    """
    imagelist = []
    for id in id_list:
        imagelist.append(conn.getObject("Image", id))
    return imagelist


def dimensionGridList(id_list, tile_dim) -> dict:
    """ build dictionary of key: image id, value: (columns, rows)
    
    Parameters
    ----------
    id_list = [int]
    tile_dim = int
    
    Returns
    --------
    dict{key: int val: tuple(int,int)}
    """
    imagedict = {}
    for id in id_list:
        col, row = tileMultiple(tile_dim, id.getSizeX(), id.getSizeY())
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
