
import numpy as np
import ezomero as ez
from ezomero import rois
import time


def tileMultiple(image, tile_dim) -> tuple:
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
    pixel_x = image.getSizeX()
    pixel_y = image.getSizeY()
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


def get_tile(image, row, col, tile_dim, z=0,c=0, t=0) -> np.array:
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
    pixels = image.getPrimaryPixels()
    return pixels.getTile(z, c, t,(col*tile_dim,row*tile_dim,tile_dim,tile_dim))


def getProjectPixels(conn, id_list) -> list:
    """ wrapper function find and return tile by col, row location at given tile dimension
    This function is now useless but I'm keeping it around JIC
    
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
        col, row = tileMultiple(image, tile_dim)
        if col < 1 or row < 1: continue
        key_val = {image.getId():(image,col,row)}
        imagedict.update(key_val)
    return imagedict
    

def makeTilesRGB(image, x, y, tile_dim) -> np.ndarray:
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
    print(("creating tile x:%d, y:%d") %(x, y))
    start_time = time.time()
    size_c = image.getSizeC()
    tile_list = []
    expanded_tile_list = []
    for c in range(size_c):
        tile_list.append(get_tile(image, y, x, tile_dim, c=c))
    print("getTile() time: %s" % (time.time() - start_time))
    expanded_tile_list = list(map(lambda x: np.expand_dims(x, axis=(2,3,4)), tile_list))
    print("expand_dims time: %s" % (time.time() - start_time))
    out_tile = expanded_tile_list.pop(0)
    for tile in expanded_tile_list:
        out_tile = np.append(out_tile, tile, axis=3)
    print("append time: %s" % (time.time() - start_time))
    return out_tile

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

def tileSingleImage(conn, image, tile_dim=2048, dataset=None):
    """ create single tileset and write to dataset or orphaned images
    
    Parameters
    ----------
    conn = Omero.Blitzgateway
    image = Omero._ImageWrapper
    tile_dim = int
    dataset = int

    """
    start_time = time.time()
    id = image.getId()
    col_x, col_y = tileMultiple(image, tile_dim)
    print("tileMultiple time: %s" % (time.time() - start_time))
    for y in range(col_y):
        for x in range(col_x):
            tile = makeTilesRGB(image, x, y, tile_dim)
            ez.post_image(
                  conn=conn
                , image=np.flipud(np.rot90(tile, k=1, axes=(0,1)))
                , image_name=image.getName() +"_tile_" + str(y) +"_" + str(x)
                , source_image_id=id
                , dataset_id=dataset
                , channel_list=[0,1,2]
                , dim_order="xyzct" 
                )
            print("postImage: %s" % (time.time() - start_time))
 
## TEST TO SHOW TRANSPOSITION ISSUE
def test(conn, image):
    pixels = image.getPrimaryPixels()
    tile = pixels.getTile(0, 1, 0,(2048,0,2048,2048))
    tile = np.expand_dims(tile, axis=(2,3,4))
    ez.post_image(conn, tile, "test", dim_order="xyzct")
