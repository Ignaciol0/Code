import cairosvg
import os

def convert_svg_to_png(svg_path, png_path):
    cairosvg.svg2png(url=svg_path, write_to=png_path)

# Example usage
svg_file = 'svg.svg'
if 'svg.png' in os.listdir():
    png_file = 'svg-2.png'
else:
    png_file = 'svg.png'
convert_svg_to_png(svg_file, png_file)
os.remove("svg.svg")