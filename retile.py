import numpy as np
import ezomero as ez
from utils import getTile, roiTiler, nearestMultipleOf
from ezomero import rois
from math import ceil

TILE_DIM = 5000 #dimension of resulting tiles

def main():
    conn = ez.connect(config_path=".")
    image = conn.getObject("Image", 1654601)
    pixels = image.getPrimaryPixels()
    tile_arr = pixels.getTile(0,0,0,(0,0,5000,5000))
    d1 = int(image.getSizeX())
    d2 = int(image.getSizeY())
    col, row = nearestMultipleOf(TILE_DIM, d1, d2)
    rect_list = roiTiler(TILE_DIM, row, col)
    ez.post_roi(conn,1654601, rect_list, "test roi1")
    

    ##row, col = nearestMultipleOf(TILE_DIMENSION, d1, d2)

    conn.close()



if __name__ == "__main__":
    main()
