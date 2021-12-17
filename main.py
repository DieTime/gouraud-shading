from crystal import Crystal
import cv2
import numpy as np
from PIL import Image

crystals = [
    {
        "title": "Glazkov crystal 1",
        "filepath": "glazkov1.obj",
        "size": 200,
        "points": 130,
        "scale": 15
    },
    {
        "title": "Glazkov crystal 2",
        "filepath": "glazkov2.obj",
        "size": 200,
        "points": 130,
        "scale": 35
    },
    {
        "title": "Saveliev crystal 1",
        "filepath": "saveliev1.obj",
        "size": 200,
        "points": 130,
        "scale": 65
    },
    {
        "title": "Saveliev crystal 2",
        "filepath": "saveliev2.obj",
        "size": 200,
        "points": 130,
        "scale": 65
    },
    {
        "title": "Tolochny crystal 1",
        "filepath": "tolochny1.obj",
        "size": 200,
        "points": 130,
        "scale": 65
    },
    {
        "title": "Tolochny crystal 2",
        "filepath": "tolochny2.obj",
        "size": 200,
        "points": 130,
        "scale": 65
    },
    {
        "title": "Nikiforov crystal 1",
        "filepath": "nikiforov1.obj",
        "size": 200,
        "points": 130,
        "scale": 65
    },
    {
        "title": "Nikiforov crystal 2",
        "filepath": "nikiforov2.obj",
        "size": 200,
        "points": 130,
        "scale": 65
    },
]

keys = {
    "left": 65361,
    "top": 65362,
    "right": 65363,
    "bottom": 65364,
    "z": 122,
    "x": 120,
    "enter": 13,
    "space": 32,
}

def loadcrystal(index):
    index = index % len(crystals)

    crystal = Crystal(crystals[index]["filepath"])
    crystal.scale(crystals[index]["scale"])

    title = crystals[index]["title"]
    size = crystals[index]["size"]
    points = crystals[index]["points"]

    return crystal, title, size, points

def main():
    print("Rotate X: UP and DOWN keys")
    print("Rotate Y: LEFT and RIGHT keys")
    print("Rotate Z: Z and X keys")
    print("Switch: SPACE key\n")
    print("For exit press ENTER...")

    current = 0
    crystal, title, size, points = loadcrystal(current)

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
        cv2.imshow(title, np.asarray(image))

        key = cv2.waitKeyEx(1000)

        if keys["enter"] == key:
            break

        if keys["space"] == key:
            cv2.destroyWindow(title)

            current += 1
            crystal, title, size, points = loadcrystal(current)

        crystal.rotateX(-5 if keys["bottom"] == key else 5 if keys["top"] == key else 0)
        crystal.rotateY(-5 if keys["right"] == key else 5 if keys["left"] == key else 0)
        crystal.rotateZ(-5 if keys["x"] == key else 5 if keys["z"] == key else 0)

if __name__ == "__main__":
    main()
