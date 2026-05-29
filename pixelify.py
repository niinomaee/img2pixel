#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from PIL import Image

PALETTES = {
    "gameboy": [
        (15, 56, 15),
        (48, 98, 48),
        (139, 172, 15),
        (155, 188, 15),
    ],
    "nes": [
        (0, 0, 0), (252, 252, 252), (248, 0, 0), (0, 248, 0),
        (0, 0, 252), (252, 252, 0), (252, 0, 252), (0, 252, 252),
        (188, 0, 0), (0, 188, 0), (0, 0, 188), (188, 188, 0),
        (188, 0, 188), (0, 188, 188), (128, 128, 128), (188, 188, 188),
        (252, 120, 48), (252, 168, 0), (0, 120, 252), (60, 188, 252),
    ],
    "grayscale": [(v, v, v) for v in range(0, 256, 16)],
    "cga": [
        (0, 0, 0), (85, 255, 255), (255, 85, 255), (255, 255, 255),
    ],
    "commodore": [
        (0, 0, 0), (255, 255, 255), (136, 0, 0), (170, 255, 238),
        (204, 68, 204), (0, 204, 85), (0, 0, 170), (238, 238, 119),
        (221, 136, 85), (102, 68, 0), (255, 119, 119), (51, 51, 51),
        (119, 119, 119), (170, 255, 102), (0, 136, 255), (187, 187, 187),
    ],
}


def closest_color(pixel, palette):
    r, g, b = pixel[:3]
    return min(palette, key=lambda c: (r - c[0])**2 + (g - c[1])**2 + (b - c[2])**2)


def apply_palette(img, palette):
    img = img.convert("RGB")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            pixels[x, y] = closest_color(pixels[x, y], palette)
    return img


def pixelify(input_path, output_path, block_size, palette_name, output_width, scale):
    img = Image.open(input_path).convert("RGB")
    src_w, src_h = img.size

    if scale:
        final_w = round(src_w * scale)
        final_h = round(src_h * scale)
    elif output_width:
        final_w = output_width
        final_h = round((output_width / src_w) * src_h)
    else:
        final_w, final_h = src_w, src_h

    pixel_w = max(1, round(final_w / block_size))
    pixel_h = max(1, round(final_h / block_size))

    print(f"input:  {src_w}x{src_h}  ({input_path})")
    print(f"output: {final_w}x{final_h}  →  pixel grid {pixel_w}x{pixel_h}")
    print(f"block:  {block_size}px  |  palette: {palette_name}")

    small = img.resize((pixel_w, pixel_h), Image.NEAREST)

    if palette_name != "none":
        small = apply_palette(small, PALETTES[palette_name])

    result = small.resize((final_w, final_h), Image.NEAREST)
    result.save(output_path)
    print(f"\n✓ saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        prog="pixelify",
        description="Convert image to pixel art PNG",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""examples:
  pixelify foto.jpg
  pixelify foto.jpg -s 16
  pixelify foto.jpg -s 12 -p gameboy -o out.png
  pixelify foto.jpg -w 800 -s 8
  pixelify foto.jpg --scale 2 -s 10 -p commodore

palettes: none, gameboy, nes, grayscale, cga, commodore"""
    )
    parser.add_argument("input", help="input image file")
    parser.add_argument("-o", "--output", help="output file (default: <input>-pixel.png)")
    parser.add_argument("-s", "--block-size", type=int, default=8, metavar="SIZE",
                        help="pixel block size in px (default: 8)")
    parser.add_argument("-p", "--palette", default="none",
                        choices=["none", "gameboy", "nes", "grayscale", "cga", "commodore"],
                        help="color palette (default: none)")
    parser.add_argument("-w", "--width", type=int, metavar="PX",
                        help="output width in pixels")
    parser.add_argument("--scale", type=float, metavar="FACTOR",
                        help="scale factor (e.g. 2.0 = double size)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}-pixel.png"

    pixelify(input_path, output_path, args.block_size, args.palette, args.width, args.scale)


if __name__ == "__main__":
    main()