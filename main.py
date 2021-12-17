from crystal import Crystal
import cv2
import numpy as np
from PIL import Image
import sys

crystals = {
    "glazkov1": { "filepath": "glazkov1.obj", "size": 200, "points": 130, "scale": 16 }
}

keys = {
    "left": 65361,
    "top": 65362,
    "right": 65363,
    "bottom": 65364,
    "enter": 13,
    "z": 122,
    "x": 120
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

    print("Rotate X: UP and DOWN keys")
    print("Rotate Y: LEFT and RIGHT keys")
    print("Rotate Z: Z and X keys\n")
    print("For exit press ENTER...")

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

        key = cv2.waitKeyEx()

        if (keys["enter"] == key):
            break

        crystal.rotateX(-5 if keys["bottom"] == key else 5 if keys["top"] == key else 0)
        crystal.rotateY(-5 if keys["right"] == key else 5 if keys["left"] == key else 0)
        crystal.rotateZ(-5 if keys["x"] == key else 5 if keys["z"] == key else 0)

if __name__ == "__main__":
    main()
