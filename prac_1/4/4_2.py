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
    radius = 0.5

    dx, dy = x - cx, y - cy
    dist = math.sqrt(dx * dx + dy * dy)

    if dist > radius:
        return (0, 0, 0)

    ratio = (x - cx) / radius  # = (x-0.5)/0.5

    if ratio < 0:
        t = ratio + 1
        r_col = 0 + (1 - 0) * t
        g_col = 1 + (1 - 1) * t
        b_col = 0
    else:
        t = ratio
        r_col = 1 + (1 - 1) * t
        g_col = 1 + (0 - 1) * t
        b_col = 0

    brightness = 1 - dist / radius
    brightness = max(0, min(1, brightness))

    return (r_col * brightness, g_col * brightness, b_col * brightness)


def main(shader):
    label = tk.Label()
    img = tk.PhotoImage(data=draw(shader, 256, 256)).zoom(2, 2)
    label.pack()
    label.config(image=img)
    tk.mainloop()


main(shader)