import numpy as np
from numba import jit


class Crystal:
    def __init__(self, filepath):
        self.vertexes = []
        self.normals = []
        self.faces = []

        for line in open(filepath):
            if line.startswith("v "):
                _, x, y, z = line.split()
                self.vertexes.append([float(x), float(y), float(z)])
                continue

            if line.startswith("vn "):
                _, x, y, z = line.split()
                self.normals.append([float(x), float(y), float(z)])
                continue

            if line.startswith("f "):
                _, x, y, z = line.split()
                x = x.split("/")[0]
                y = y.split("/")[0]
                z = z.split("/")[0]
                self.faces.append([int(x), int(y), int(z)])
                continue

        while (len(self.normals) != len(self.faces)):
            self.normals.append([0.001, 0.001, 0.001])

        self.vertexes = np.array(self.vertexes)
        self.normals = np.array(self.normals)
        self.faces = np.array(self.faces)

    def rotateVertexes(self, rotMatrix):
        for i, vertex in enumerate(self.vertexes):
            self.vertexes[i] = vertex.dot(rotMatrix)

    def rotateNormals(self, rotMatrix):
        for i, normal in enumerate(self.normals):
            self.normals[i] = normal.dot(rotMatrix)

    def rotateX(self, angle):
        sinX = np.sin(angle * np.pi / 180)
        cosX = np.cos(angle * np.pi / 180)
        rotX = np.matrix([[1,    0,     0],
                          [0, cosX, -sinX],
                          [0, sinX, cosX]])

        self.rotateVertexes(rotX)
        self.rotateNormals(rotX)

    def rotateY(self, angle):
        sinY = np.sin(angle * np.pi / 180)
        cosY = np.cos(angle * np.pi / 180)
        rotY = np.matrix([[cosY,  0, sinY],
                          [0,     1,    0],
                          [-sinY, 0, cosY]])

        self.rotateVertexes(rotY)
        self.rotateNormals(rotY)

    def rotateZ(self, angle):
        sinZ = np.sin(angle * np.pi / 180)
        cosZ = np.cos(angle * np.pi / 180)
        rotZ = np.matrix([[cosZ, -sinZ, 0],
                          [sinZ,  cosZ, 0],
                          [0,        0, 1]])

        self.rotateVertexes(rotZ)
        self.rotateNormals(rotZ)

    def scale(self, factor):
        for i, vertex in enumerate(self.vertexes):
            self.vertexes[i] = vertex * factor

        for i, normal in enumerate(self.normals):
            self.normals[i] = normal * factor

    @staticmethod
    @jit(fastmath=True)
    def render(vertexes, normals, faces, size, points, light=np.array([1, -1, -1]), AMB=70, DIRECT=120):
        image = []
        zbuffer = np.ones(size * size) * 1e6

        for face in faces:
            v1 = vertexes[face[0] - 1]
            v2 = vertexes[face[1] - 1]
            v3 = vertexes[face[2] - 1]

            dv2 = v2 - v1
            dv3 = v3 - v1

            n1 = normals[face[0] - 1]
            n2 = normals[face[1] - 1]
            n3 = normals[face[2] - 1]

            ang1 = (np.sum(light * n1)) / (np.sqrt(np.sum(n1 ** 2)) * np.sqrt(np.sum(light ** 2)))
            ang2 = (np.sum(light * n2)) / (np.sqrt(np.sum(n2 ** 2)) * np.sqrt(np.sum(light ** 2)))
            ang3 = (np.sum(light * n3)) / (np.sqrt(np.sum(n3 ** 2)) * np.sqrt(np.sum(light ** 2)))

            c1 = int(max(AMB, AMB + DIRECT * ang1))
            c2 = int(max(AMB, AMB + DIRECT * ang2))
            c3 = int(max(AMB, AMB + DIRECT * ang3))

            dc2 = c2 - c1
            dc3 = c3 - c1

            for p in range(points):
                va = v1 + dv2 * p / points
                vb = v1 + dv3 * p / points
                c = c1 + np.array([dc2, dc3]) * p / points

                for point in range(points):
                    f1 = point / points
                    f2 = 1 - f1

                    x, y, z = f1 * va + f2 * vb
                    d = (200 - z) / 200  # apply some linear perspective by Z

                    pixelx = int(d * x + size / 2)
                    pixely = int(d * y + size / 2)

                    if pixelx < 0 or pixely < 0 or pixelx > size - 1 or pixely > size - 1:
                        continue

                    color = int(c[0] * f1 + c[1] * f2)

                    zindex = pixely * size + pixelx
                    if z < zbuffer[zindex]:
                        zbuffer[zindex] = z
                        image.append([pixelx, pixely, color])

        return image
