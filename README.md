# img2pixel

Convert any image to pixel art PNG from the command line.

```
foto.jpg  →  foto-pixel.png
```

## install

```bash
pip install Pillow
```

then just download `pixelify.py` and run it.

optionally, make it executable:

```bash
chmod +x pixelify.py
./pixelify.py foto.jpg
```

or add an alias to your shell:

```bash
alias pixelify="python3 /path/to/pixelify.py"
```

## usage

```
pixelify <input> [options]

options:
  -s, --block-size SIZE   pixel block size in px (default: 8)
  -p, --palette NAME      color palette (default: none)
  -o, --output FILE       output file (default: <input>-pixel.png)
  -w, --width PX          output width in pixels
      --scale FACTOR      scale factor (e.g. 2.0 = double size)
```

## examples

```bash
# basic, block size 8
python3 pixelify.py foto.jpg

# chunkier pixels
python3 pixelify.py foto.jpg -s 16

# gameboy palette, custom output
python3 pixelify.py foto.jpg -s 12 -p gameboy -o out.png

# 2x upscale with commodore 64 palette
python3 pixelify.py foto.jpg --scale 2 -s 10 -p commodore

# resize output width and apply nes palette
python3 pixelify.py foto.jpg -w 800 -s 8 -p nes
```

## palettes

| name | colors | based on |
|------|--------|----------|
| `none` | full color | — |
| `gameboy` | 4 | Nintendo Game Boy |
| `nes` | 20 | Nintendo NES |
| `cga` | 4 | IBM CGA mode 4 |
| `commodore` | 16 | Commodore 64 |
| `grayscale` | 16 | evenly spaced grays |

## how it works

1. downscale image to `(width / block_size) × (height / block_size)` using nearest neighbor
2. optionally quantize each pixel to the closest color in the chosen palette (euclidean distance in RGB space)
3. upscale back to original (or target) dimensions using nearest neighbor → blocky pixel art effect

## requirements

- Python 3.7+
- [Pillow](https://pillow.readthedocs.io)

## license

MIT