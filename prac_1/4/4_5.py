import math
import tkinter as tk


def draw(shader, width, height):
    image = bytearray((0, 0, 0) * width * height)
    for py in range(height):
        for px in range(width):
            pos = (width * py + px) * 3
            x = px / width
            y = py / height
            color = shader(x, y)
            r, g, b = [max(0, min(255, int(c * 255))) for c in color]
            image[pos:pos + 3] = (r, g, b)
    header = bytes(f'P6\n{width} {height}\n255\n', 'ascii')
    return header + image


def fade(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def noise(x: int, y: int) -> float:
    n = x + y * 1000
    n = (n << 13) ^ n
    res = 1.0 - ((n * (n * n * 60493 + 19990303) + 1376312589)
                 & 0x7fffffff) / 1073741824.0
    return 0.5 * (res + 1.0)


def val_noise(x, y):
    x0 = math.floor(x)
    y0 = math.floor(y)
    x1 = x0 + 1
    y1 = y0 + 1

    tx = x - x0
    ty = y - y0

    c00 = noise(x0, y0)
    c10 = noise(x1, y0)
    c01 = noise(x0, y1)
    c11 = noise(x1, y1)

    u = fade(tx)
    v = fade(ty)

    nx0 = lerp(c00, c10, u)
    nx1 = lerp(c01, c11, u)
    return lerp(nx0, nx1, v)


def shader(x, y):
    scale = 8.0
    v = val_noise(x * scale, y * scale)
    return (v, v, v)


def main(shader):
    root = tk.Tk()
    root.title("Value Noise (ЧБ)")
    width, height = 256, 256
    data = draw(shader, width, height)
    img = tk.PhotoImage(data=data).zoom(2, 2)
    label = tk.Label(root, image=img)
    label.pack()
    root.mainloop()


main(shader)