from crystal import Crystal
import cv2
import numpy as np
from PIL import Image
import sys

crystals = {
    "glazkov1": { "filepath": "glazkov1.obj", "size": 200, "points": 120, "scale": 15 }
}

def usage():
    print('Allowed crystals:')
    for crystal in crystals.keys():
        print(f'  - {crystal}')
    exit(1)

def main():
    if len(sys.argv) < 2:
        print('Enter crystal name in arguments!')
        usage()

    try:
        params = crystals[sys.argv[1]]

        crystal = Crystal(params["filepath"])
        crystal.scale(params["scale"])
        size = params["size"]
        points = params["points"]
    except:
        print(f'Crystal with name "{sys.argv[1]}" not exist!')
        usage()


    while True:
        image = Image.new("RGB", (size, size))

        # render crystal as pixels array
        imagedata = crystal.render(crystal.vertexes,
                                crystal.normals,
                                crystal.faces,
                                size=size,
                                points=points)

        # convert to pillow image
        for pixelx, pixely, color in imagedata:
            image.putpixel((pixelx, pixely), (color, color, color))

        # show image frame
        cv2.imshow(params["filepath"], np.asarray(image))
        cv2.waitKey(1)

        # update crystal
        crystal.rotateX(2)
        crystal.rotateY(5)
        crystal.rotateZ(5)

if __name__ == "__main__":
    main()
