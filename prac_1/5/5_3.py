import math
import tkinter as tk


def draw(shader, width, height):
    image = bytearray((0, 0, 0) * width * height)
    for y in range(height):
        for x in range(width):
            pos = (width * y + x) * 3
            color = shader(x / width, y / height)
            normalized = [max(min(int(c * 255), 255), 0) for c in color]
            image[pos:pos + 3] = normalized
    header = bytes(f'P6\n{width} {height}\n255\n', 'ascii')
    return header + image


def box(x, y, s):
    qx = abs(x) - s / 2
    qy = abs(y) - s / 2
    outside = math.sqrt(max(qx, 0) ** 2 + max(qy, 0) ** 2)
    inside = min(max(qx, qy), 0)
    return outside + inside


def circle(x, y, r):
    return math.sqrt(x ** 2 + y ** 2) - r


def union(a, b):
    return min(a, b)


def intersect(a, b):
    return max(a, b)


def difference(a, b):
    return max(a, -b)


def sdf_func(x, y):
    return difference(box(x, y, 0.6), circle(x, y, 0.25))


def shader(x, y):
    d = sdf_func(x - 0.5, y - 0.5)
    return d > 0, abs(d) * 3, 0


def main(shader):
    label = tk.Label()
    img = tk.PhotoImage(data=draw(shader, 256, 256)).zoom(2, 2)
    label.pack()
    label.config(image=img)
    tk.mainloop()


main(shader)
