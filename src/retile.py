
import sys, getopt
import ezomero as ez
from utils import tileSingleImage,getProjectImages, test


def main():
    project_id = ''
    image_id = ''
    dataset = ''
    tile_dim = 2048
    conn = ez.connect(group= "Neurobiology Imaging Facility",config_path=".")  #config path is lo
    ##need to setup combined argument outcomes ex. : -p + -d + -i

    try:
        opts, args = getopt.getopt(sys.argv[1:],"t:p:d:i:",["tile_dim=","project_id=", "dataset=","image_id="])
    except getopt.GetoptError:
      print('retile.py -p <project id> | -d <dataset id> | -d <dataset id> -i <image id> |  -i <image id> ')
      sys.exit(2)

    options, arguments = zip(*opts)

    if('-p' in options):
        print("Tiling all images in project...")
        project_id = arguments[options.index('-p')]
        project = conn.getObject("Project", project_id)
        for dataset in project.listChildren():
          image_list = getProjectImages(conn, ez.get_image_ids(conn, dataset=dataset.getId()))
          for image in image_list:
            tileSingleImage(conn, image, tile_dim, dataset.getId())
        conn.close()
        sys.exit(0)
                
    if('-d' in options and '-i' in options):
        print("Running single image only and placing into dataset...")
        image_id = arguments[options.index('-i')]
        dataset = int(arguments[options.index('-d')])
        image = conn.getObject("Image", str(image_id))
        tileSingleImage(conn, image, tile_dim, dataset )
        conn.close()
        sys.exit(0)

    if ('-i' in options):
        print("Running image only. Image will be orphaned...")
        image_id = arguments[options.index('-i')]
        image = conn.getObject("Image", image_id)
        #test(conn, image)
        tileSingleImage(conn, image, tile_dim)
        conn.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
