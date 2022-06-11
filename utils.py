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
    pixels : <omero.gateway._PixelsWrapper>
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
    list[<omero.gateway._PixelsWrapper>] 
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
    list[<Omero.Image>]
    """
    imagelist = []
    for id in id_list:
        imagelist.append(conn.getObject("Image", id))
    return imagelist


def dimensionGridList(image_list, tile_dim) -> dict:
    """ build dictionary of key: image id, value: (<primaryPixels>,columns, rows)
    
    Parameters
    ----------
    id_list = [<Omero.Image>]??? not sure is correct
    tile_dim = int
    
    Returns
    --------
    dict{key: int val: tuple(int,int)}
    """
    imagedict = {}
    for image in image_list:
        print(str(image.getSizeX()) + " " + str(image.getSizeY()))
        col, row = tileMultiple(tile_dim, image.getSizeX(), image.getSizeY())
        if col < 1 or row < 1: continue
        key_val = {image.getId():(image.getPrimaryPixels(),col,row)}
        imagedict.update(key_val)
    return imagedict
    

def makeTileRGB(primary_pixels, x, y, tile_dim) -> np.ndarray:
    """ from pixels create tile for each channel of RGB image and build new 
    
    Parameters
    ----------
    primary_pixels = _PixelsWrapper
    x = int
    y = int
    tile_dim = int
    Returns
    --------
    nd.array [x,y,z,c,t]
    """
    print("STARTING makeTileRGB")
    tileR = get_tile(primary_pixels, y, x, tile_dim, c=0)
    tileG = get_tile(primary_pixels, y, x, tile_dim, c=1)
    tileB = get_tile(primary_pixels, y, x, tile_dim, c=2)
    tileR = np.expand_dims(tileR, axis=(2,3,4))
    tileG = np.expand_dims(tileG, axis=(2,3,4))
    tileB = np.expand_dims(tileB, axis=(2,3,4))
    tileR = np.append(tileR, tileG, axis=3)
    tileR = np.append(tileR, tileB, axis=3)
    return tileR

def makeTileGScale(primary_pixels, x, y, tile_dim, size_c) -> np.ndarray:
    """ from pixels create tile for each channel of multichannel image and build new 
    
    Parameters
    ----------
    primary_pixels = [int]
    x = int
    y = int
    tile_dim = int
    size_c = int (number of channels)
    Returns
    --------
    nd.array [x,y,z,c,t]
    """
    tile_r = np.empty(shape=5)
    for c in range(size_c):
        tile = get_tile(primary_pixels, y, x, tile_dim, c)
        tile = np.expand_dims(tile, axis=(2,3,4))
        np.append(tile_r, tile)
    return tile_r


def breakUpImage(conn, imagedict, tile_dim):
    for key, value in imagedict.items():
        image = conn.getObject("Image", key)
        for y in range(value[1]):
            for x in range(value[0]):
                tile = get_tile(image.getPrimaryPixels(), x, y, tile_dim)
                tile = np.expand_dims(tile, axis=(2,3,4))
                ez.post_image(conn, tile, "%s row: %d col: %d" % (key, y, x), key, channel_list=[0] )
