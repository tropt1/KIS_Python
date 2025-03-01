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


def shader(x, y):
    cx, cy = 0.5, 0.5
    r = 0.4
    d = math.sqrt((x - cx)**2 + (y - cy)**2)
    if d < r:
        z = math.sqrt(r**2 - d**2)
        intensity = z / r
        return intensity, intensity, intensity
    return 0, 0, 0


def main(shader):
    label = tk.Label()
    img = tk.PhotoImage(data=draw(shader, 256, 256)).zoom(2, 2)
    label.pack()
    label.config(image=img)
    tk.mainloop()


main(shader)