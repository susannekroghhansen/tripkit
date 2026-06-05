from PIL import Image, ImageDraw

TEAL = (0x13, 0x8B, 0x93)
SKY  = (0x2C, 0x9C, 0xD8)
WHITE = (255, 255, 255)

def gradient(size):
    img = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        r = int(TEAL[0] + (SKY[0] - TEAL[0]) * t)
        g = int(TEAL[1] + (SKY[1] - TEAL[1]) * t)
        b = int(TEAL[2] + (SKY[2] - TEAL[2]) * t)
        d.line([(0, y), (size, y)], fill=(r, g, b))
    return img

def draw_suitcase(img, scale):
    """Draw a clean white suitcase centred on img, sized by `scale` (fraction of canvas)."""
    size = img.size[0]
    d = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2
    w = size * scale            # body width
    h = w * 0.80                # body height
    lw = max(3, int(size * 0.022))
    # nudge body down a touch to leave room for the handle
    bx0, by0 = cx - w / 2, cy - h / 2 + h * 0.10
    bx1, by1 = cx + w / 2, cy + h / 2 + h * 0.10
    rad = w * 0.16
    # handle: a rounded-rect outline above the body (body will cover its lower half)
    hw, hh = w * 0.36, h * 0.30
    hx0, hx1 = cx - hw / 2, cx + hw / 2
    hy0 = by0 - hh * 0.62
    hy1 = by0 + hh * 0.38
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=hh * 0.5, outline=WHITE, width=lw)
    # body (covers the handle's lower half, leaving an arch)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=rad, fill=WHITE)
    # seam + two latches, drawn in the gradient's mid colour so they read as cut-outs
    seam = (0x1E, 0x94, 0xB5)
    sy = cy + h * 0.10
    d.line([(bx0 + w * 0.02, sy), (bx1 - w * 0.02, sy)], fill=seam, width=lw)
    latch_w = w * 0.14
    for lx in (cx - w * 0.20, cx + w * 0.20):
        d.rounded_rectangle([lx - latch_w / 2, sy - lw, lx + latch_w / 2, sy + lw],
                            radius=lw, fill=seam)
    return img

def make(size, scale, path):
    img = gradient(size)
    draw_suitcase(img, scale)
    img.save(path)
    print("wrote", path)

# Full-bleed icons (iOS rounds the corners itself; Android "any")
make(512, 0.58, "icons/icon-512.png")
make(192, 0.58, "icons/icon-192.png")
make(180, 0.58, "icons/apple-touch-icon.png")
# Maskable: smaller artwork inside the safe zone so Android's mask won't clip it
make(512, 0.42, "icons/icon-maskable-512.png")
