import numpy as np
import ezomero as ez
from ezomero import rois
from math import ceil
TILE_DIM = 5000 #dimension of resulting tiles

def main():
    conn = ez.connect(group="Neurobiology Imaging Facility")
    image = conn.getObject("Image", 1654601)

    pixels = image.getPrimaryPixels()
    d1 = int(image.getSizeX())
    d2 = int(image.getSizeY())
    col, row = nearestMultipleOf(TILE_DIM, d1, d2)
    rect_list = roiTiler(TILE_DIM, row, col)
    ez.post_roi(conn,1654601, rect_list, "test roi1")
    

    ##row, col = nearestMultipleOf(TILE_DIMENSION, d1, d2)

    conn.close()


def nearestMultipleOf(tile_dim, dim1, dim2):
    return int(ceil(dim1/tile_dim)), int(ceil(dim2/tile_dim))

def roiTiler(tile_dim, row, col):
    rect_list = []
    for y in range(0, row):
        for x in range(0, col):
            rect_list.append(rois.Rectangle(x*TILE_DIM, y*TILE_DIM, TILE_DIM, TILE_DIM, label="row: %d col: %d" % (y, x)))
    return rect_list


if __name__ == "__main__":
    main()
