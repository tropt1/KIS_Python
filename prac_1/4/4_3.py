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
    radius = 0.4
    dx, dy = x - cx, y - cy

    if dx * dx + dy * dy > radius * radius:
        return 0, 0, 0  # фон
    eye_dx, eye_dy = x - 0.6, y - 0.25
    if eye_dx * eye_dx + eye_dy * eye_dy < 0.07 * 0.07:
        return 0, 0, 0  # глаз

    angle_deg = math.degrees(math.atan2(dy, dx))
    if -30 <= angle_deg <= 30:
        return 0, 0, 0  # рот

    return 1, 1, 0


def main(shader):
    label = tk.Label()
    img = tk.PhotoImage(data=draw(shader, 256, 256)).zoom(2, 2)
    label.pack()
    label.config(image=img)
    tk.mainloop()

    
main(shader)