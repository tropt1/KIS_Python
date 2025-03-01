import tkinter as tk


def noise(i: int, j: int) -> float:
    n = i + j * 150
    n = (n << 13) ^ n
    res = 1.0 - ((n * (n * n * 60493 + 19990303) + 1376312589)
                 & 0x7fffffff) / 1073741824.0
    return 0.5 * (res + 1.0)


def draw_noise(width: int, height: int) -> bytes:
    image = bytearray((0, 0, 0) * width * height)
    for j in range(height):
        for i in range(width):
            pos = (j * width + i) * 3
            v = noise(i, j)
            v = max(0.0, min(1.0, v))
            col = int(v * 255)
            image[pos:pos + 3] = (col, col, col)
    header = bytes(f"P6\n{width} {height}\n255\n", "ascii")
    return header + image


def main():
    root = tk.Tk()
    root.title("Визуализация функции noise")
    width, height = 256, 256
    data = draw_noise(width, height)
    img = tk.PhotoImage(data=data).zoom(2, 2)
    label = tk.Label(root, image=img)
    label.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
