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


def val_noise(x, y):
    scale = 10
    u = x * scale
    v = y * scale
    ix = math.floor(u) % scale
    iy = math.floor(v) % scale
    fx = u - math.floor(u)
    fy = v - math.floor(v)
    n00 = noise(ix, iy)
    n01 = noise(ix, (iy + 1) % scale)
    n10 = noise((ix + 1) % scale, iy)
    n11 = noise((ix + 1) % scale, (iy + 1) % scale)
    n0 = n00 * (1 - fx) + n10 * fx
    n1 = n01 * (1 - fx) + n11 * fx
    n = n0 * (1 - fy) + n1 * fy
    return n


def fbm_noise(x, y, octaves=3):
    result = 0
    amplitude = 1
    frequency = 1
    total_amp = 0
    for _ in range(octaves):
        result += amplitude * val_noise(x * frequency, y * frequency)
        total_amp += amplitude
        amplitude *= 0.5
        frequency *= 2
    return result / total_amp


def shader(x, y):
    n = fbm_noise(x, y)
    return n, n, n


def main(shader):
    label = tk.Label()
    img = tk.PhotoImage(data=draw(shader, 256, 256)).zoom(2, 2)
    label.pack()
    label.config(image=img)
    tk.mainloop()


main(shader)
