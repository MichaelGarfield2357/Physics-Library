import pygame as pg
import numpy as np
from numba import jit
import time

# ------------------ CONFIG ------------------
WIDTH, HEIGHT = 800, 600
MAX_ITER = 128
ZOOM_SPEED = 1.2

# ------------------ PALETTE ------------------
def make_palette(max_iter):
    palette = np.zeros((max_iter + 1, 3), dtype=np.uint8)
    for i in range(max_iter + 1):
        t = i / max_iter
        palette[i] = (0, 0, int(255 * t))
    return palette

PALETTE = make_palette(MAX_ITER)

# ------------------ MANDELBROT ------------------
@jit(nopython=True, parallel=True)
def mandelbrot(cx, cy, zoom):
    img = np.zeros((HEIGHT, WIDTH), dtype=np.int32)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            zx = 0.0
            zy = 0.0

            x0 = (x - WIDTH / 2) / zoom + cx
            y0 = (y - HEIGHT / 2) / zoom + cy

            for i in range(MAX_ITER):
                zx2 = zx*zx - zy*zy + x0
                zy = 2*zx*zy + y0
                zx = zx2

                if zx*zx + zy*zy > 4:
                    img[y, x] = i
                    break
    return img

# ------------------ DRAW ------------------
def draw(screen, data):
    rgb = PALETTE[data]
    rgb = np.transpose(rgb, (1, 0, 2))
    pg.surfarray.blit_array(screen, rgb)

# ------------------ MAIN ------------------
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    cx, cy = -0.5, 0.0
    zoom = 250

    running = True
    redraw = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEWHEEL:
                mx, my = pg.mouse.get_pos()

                # Convert mouse to complex plane
                zx = (mx - WIDTH / 2) / zoom + cx
                zy = (my - HEIGHT / 2) / zoom + cy

                if event.y > 0:
                    zoom *= ZOOM_SPEED
                else:
                    zoom /= ZOOM_SPEED

                # Keep zoom centered on mouse
                cx = zx - (mx - WIDTH / 2) / zoom
                cy = zy - (my - HEIGHT / 2) / zoom

                redraw = True

        if redraw:
            t0 = time.time()
            data = mandelbrot(cx, cy, zoom)
            dt = time.time() - t0
            print(f"Rendering time: {dt}s")
            draw(screen, data)
            pg.display.flip()
            redraw = False

        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
