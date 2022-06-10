import numpy as np
import ezomero as ez
from utils import get_tile, roiTiler, breakUpImage,tileMultiple, getProjectPixels, dimensionGridList,getProjectImages
from ezomero import rois
from math import ceil

TILE_DIM = 2048#dimension of resulting tiles
PROJECT_ID = 9152
IMAGE_ID = 1662905


conn = ez.connect(group="Neurobiology Imaging Facility",config_path=".")
image = conn.getObject("Image", IMAGE_ID)

d1 = image.getSizeX()
print("dimension1: " + str(d1))
d2 = image.getSizeY()
print("dimension2: " + str(d2))
cols, rows = tileMultiple(TILE_DIM, d1, d2)

for y in range(rows):
    for x in range(cols):
        print("x: " + str(x) + " y:" + str(y))
        pixels = image.getPrimaryPixels()
        print(type(pixels))
        tileR = get_tile(pixels, y, x, TILE_DIM, c=0)
        tileG = get_tile(pixels, y, x, TILE_DIM, c=1)
        tileB = get_tile(pixels, y, x, TILE_DIM, c=2)
        print(tileR)
        print(tileG)
        print(tileB)
        tileR = np.expand_dims(tileR, axis=(2,3,4))
        tileG = np.expand_dims(tileG, axis=(2,3,4))
        tileB = np.expand_dims(tileB, axis=(2,3,4))
        np.append(tileR, tileG)
        np.append(tileR, tileB)
        print(ez.post_image(conn, image=tileR, image_name="my test images", source_image_id=IMAGE_ID, channel_list=[0,1,2] ))

conn.close()
