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


def noise(x, y):
    n = x * 15485863 + y * 32416190071
    n = (n * n * n) % 1000000007
    return (n % 10000) / 10000.0


def fade(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


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


def fbm_noise(x: float, y: float, octaves=6, lacunarity=2.0, gain=0.5) -> float:
    freq = 1.0
    amp = 1.0
    total = 0.0
    for _ in range(octaves):
        total += val_noise(x * freq, y * freq) * amp
        freq *= lacunarity
        amp *= gain
    return total


def shader(x: float, y: float):
    scale = 3.0
    n = fbm_noise(x * scale, y * scale, octaves=6, lacunarity=2.0, gain=0.5)
    t = max(0.0, min(1.0, n))

    sky = (0.6, 0.8, 1.0)
    cloud = (1.0, 1.0, 1.0)
    # Интерполяция: чем выше t, тем больше облачный (белый) цвет
    r = sky[0] + (cloud[0] - sky[0]) * t
    g = sky[1] + (cloud[1] - sky[1]) * t
    b = sky[2] + (cloud[2] - sky[2]) * t
    return r, g, b


def main(shader):
    label = tk.Label()
    img = tk.PhotoImage(data=draw(shader, 256, 256)).zoom(2, 2)
    label.pack()
    label.config(image=img)
    tk.mainloop()


main(shader)
