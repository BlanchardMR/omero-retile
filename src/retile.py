
import sys, getopt
import numpy as np
import ezomero as ez
from utils import get_tile, roiTiler, tileMultiple, getProjectPixels, dimensionGridList,getProjectImages, makeTileRGB
from ezomero import rois
from math import ceil
import omero


PROJECT_ID = 9152

def main(argv):
    project_id = ''
    image_id = ''
    tile_dim = 2048
    try:
        opts, args = getopt.getopt(argv,"tp:di",["tile_dim=","project_id=", "dataset=","image_id="])
    except getopt.GetoptError:
      print('retile.py -p <project_id>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-d':
         print ('dimension set to', arg)
      elif opt == '-p':
        project_id = arg
      elif opt == '-i':
         image_id = arg

    conn = ez.connect(config_path=".")  #config path is location of .ezomero file
    image_ids = ez.get_image_ids(conn, dataset=18352)
    imagelist = getProjectImages(conn, image_ids)
    imagedict = dimensionGridList(imagelist, tile_dim)

    #below will be turned into upload function
    for k,v in imagedict.items():
        print("k: " + str(k) + "  v: " + str(v))
        ez.post_roi(conn, k, roiTiler(tile_dim, v[2], v[1]))
        for y in range(v[2]):
            for x in range(v[1]):   
                tile = makeTileRGB(v[0], x, y, tile_dim)
                print(ez.post_image(conn, image=np.flipud(np.rot90(tile, k=1, axes=(0,1))), image_name=str(k) +"_tile_" + str(y) +"_" + str(x), source_image_id=k, channel_list=[0,1,2], dim_order="xyzct" ))


    conn.close()



if __name__ == "__main__":
    main(sys.argv[1:])
