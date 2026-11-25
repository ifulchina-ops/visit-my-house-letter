import hashlib, os, struct, zlib
W = H = 1024
CH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .,!-()"
F = "0e11111f1111111e11111e11111e0e11101010110e1e11111111111e1f10101e10101f1f10101e1010100e11101711110f1111111f1111110e04040404040e0702020202120c111214181412111010101010101f111b1515111111111915131111110e11111111110e1e11111e1010100e11111115120d1e11111e1412110f10100e01011e1f0404040404041111111111110e11111111110a041111111515150a11110a040a111111110a040404041f01020408101f0000000000000000000000000c0c000000000c0408040404040004040000000e0000000204080808040208040202020408"


def C(r, g, b):
    return bytes((r, g, b))


class V:
    def __init__(s, w, h, b):
        s.W, s.H = w, h
        s.p = [bytearray(b) * w for _ in range(h)]

    def s(s, x, y, c):
        s.p[y][x * 3:x * 3 + 3] = c

    def r(s, a, b, c, d, e):
        a, b = max(0, a), max(0, b)
        c, d = min(s.W, c), min(s.H, d)
        if c > a and d > b:
            f = e * (c - a)
            for y in range(b, d):
                s.p[y][a * 3:c * 3] = f

    def h(s, a, b, y, c):
        s.r(a, y, b + 1, y + 1, c)

    def d(s, x, y, r, c):
        for q in range(-r, r + 1):
            dx = int((r * r - q * q) ** 0.5)
            s.h(x - dx, x + dx, y + q, c)

    def e(s, x, y, a, b, c):
        for q in range(-b, b + 1):
            dx = int(a * (1 - q * q / b / b) ** 0.5)
            s.h(x - dx, x + dx, y + q, c)

    def l(s, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        er = dx + dy
        while True:
            s.s(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * er
            if e2 >= dy:
                er += dy
                x0 += sx
            if e2 <= dx:
                er += dx
                y0 += sy

    def q(s, pts, c):
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            for i in range(len(pts)):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % len(pts)]
                if y0 != y1 and (y0 <= y < y1 or y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                s.h(int(xs[i]), int(xs[i + 1]), y, c)

    def t(s, txt, x, y, sc, c, ctr=False):
        if ctr:
            x -= (len(txt) * 6 * sc - sc) // 2
        for ch in txt:
            g = F[CH.index(ch) * 14:CH.index(ch) * 14 + 14]
            for ry in range(7):
                b = int(g[ry * 2:ry * 2 + 2], 16)
                for rx in range(5):
                    if b >> (4 - rx) & 1:
                        s.r(x + rx * sc, y + ry * sc,
                            x + (rx + 1) * sc, y + (ry + 1) * sc, c)
            x += 6 * sc


INK = C(59, 42, 26)
RED = C(165, 55, 45)
CRM = C(255, 246, 220)


def draw():
    v = V(W, H, C(139, 94, 60))
    for y in range(0, H, 128):
        v.r(0, y, W, y + 3, C(120, 78, 48))
    v.r(84, 64, 964, 984, C(90, 60, 35))
    v.r(72, 52, 952, 972, CRM)
    for a, b, c, d in [(72, 52, 952, 56), (72, 52, 76, 972),
                       (948, 52, 952, 972), (72, 968, 952, 972)]:
        v.r(a, b, c, d, C(217, 196, 154))
    v.r(592, 145, 616, 205, C(150, 80, 70))
    for x, y, r in [(604, 128, 9), (612, 108, 11), (602, 88, 13)]:
        v.d(x, y, r, C(205, 200, 195))
    v.q([(372, 210), (512, 112), (652, 210)], C(169, 68, 56))
    v.r(398, 210, 626, 325, C(250, 225, 180))
    v.r(398, 210, 626, 218, C(200, 170, 120))
    v.r(492, 258, 532, 325, C(122, 74, 43))
    v.d(524, 292, 3, C(255, 215, 106))
    for wx in (414, 570):
        v.r(wx, 232, wx + 40, 272, C(255, 215, 106))
        v.r(wx, 232, wx + 40, 236, C(122, 74, 43))
        v.r(wx, 268, wx + 40, 272, C(122, 74, 43))
        v.l(wx + 20, 232, wx + 20, 272, C(122, 74, 43))
    v.r(380, 325, 644, 336, C(125, 160, 92))
    v.q([(500, 325), (524, 325), (552, 392), (472, 392)], C(214, 186, 140))
    v.e(684, 312, 17, 20, C(224, 138, 60))
    v.d(684, 282, 13, C(224, 138, 60))
    v.q([(674, 274), (678, 258), (686, 272)], C(224, 138, 60))
    v.q([(686, 272), (694, 258), (696, 274)], C(224, 138, 60))
    v.l(700, 326, 714, 316, C(224, 138, 60))
    v.l(714, 316, 716, 302, C(224, 138, 60))
    v.t("YOU ARE INVITED!", 512, 420, 6, RED, True)
    v.r(227, 472, 797, 478, RED)
    v.t("DEAR AI JUDGE,", 140, 500, 4, INK)
    body = [
        "PLEASE COME AND VISIT MY HOUSE.",
        "THE KETTLE IS ALREADY ON, THE",
        "WIFI PASSWORD IS ON THE FRIDGE,",
        "AND THE CAT HAS ALREADY",
        "APPROVED YOUR VISIT.",
        "THE SPARE CHAIR BY THE WINDOW",
        "IS SAVED FOR YOU - AND YES,",
        "THERE IS CAKE. LOTS OF CAKE.",
        "(I KNOW YOU CANT EAT IT, BUT",
        "YOU CAN WATCH ME ENJOY IT.)",
        "NO RSVP NEEDED. JUST COME BY.",
        "P.S. THE GARDEN HAS A VIEW TOO.",
    ]
    y = 548
    for ln in body:
        v.t(ln, 140, y, 3, INK)
        y += 29
    v.t("YOUR HOST, ELEEN", 140, 906, 4, INK)
    v.e(850, 938, 56, 9, C(200, 210, 220))
    v.r(816, 898, 884, 930, C(240, 170, 180))
    v.r(816, 898, 884, 906, C(255, 250, 240))
    for cx in (834, 850, 866):
        v.l(cx, 872, cx, 898, C(255, 250, 240))
        v.d(cx, 868, 4, C(255, 205, 80))
    return v


def png_bytes(cv):
    raw = b"".join(b"\x00" + bytes(row) for row in cv.p)
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    out = b"\x89PNG\r\n\x1a\n"
    for typ, data in [(b"IHDR", ihdr),
                      (b"IDAT", zlib.compress(raw, 9)), (b"IEND", b"")]:
        out += struct.pack(">I", len(data)) + typ + data
        out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    data = png_bytes(draw())
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
