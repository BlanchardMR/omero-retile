import numpy as np
import ezomero as ez
from utils import get_tile, roiTiler, tileMultiple, getProjectPixels, dimensionGridList,getProjectImages, makeTileRGB
from ezomero import rois
from math import ceil

TILE_DIM = 2048#dimension of resulting tiles
PROJECT_ID = 9152

def main():
    conn = ez.connect(config_path=".")
    image_ids = ez.get_image_ids(conn, dataset=18352)
    imagelist = getProjectImages(conn, image_ids)
    imagedict = dimensionGridList(imagelist, TILE_DIM)
    for k,v in imagedict.items():
        print("k: " + str(k) + "  v: " + str(v))
        ez.post_roi(conn, k, roiTiler(TILE_DIM, v[2], v[1]))
        for y in range(v[2]):
            for x in range(v[1]):   
                tile = makeTileRGB(v[0], x, y, TILE_DIM)
                print(ez.post_image(conn, image=tile, image_name=str(k) +"_tile_" + str(x) 
                +"_" + str(y), source_image_id=k, channel_list=[0,1,2] ))



    # image = conn.getObject("Image", 1654601)
    # pixels = image.getPrimaryPixels()
    # tile_arr = pixels.getTile(0,0,0,(0,0,5000,5000))
    # d1 = int(image.getSizeX())
    # d2 = int(image.getSizeY())
    # col, row = tileMultiple(TILE_DIM, d1, d2)
    # rect_list = roiTiler(TILE_DIM, row, col)
    # ez.post_roi(conn,1654601, rect_list, "test roi1")
    # ##row, col = tileMultiple(TILE_DIMENSION, d1, d2)

    conn.close()



if __name__ == "__main__":
    main()
